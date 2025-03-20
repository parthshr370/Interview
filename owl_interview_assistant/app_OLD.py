import os
import streamlit as st
import pandas as pd
from pathlib import Path
import logging
import queue
import threading
import time
import sys

# Add parent directory to path for OWL imports if needed
sys.path.append('../')

# Try to import the necessary functions
try:
    from main import research_company, generate_interview_questions, create_interview_prep_plan
except ImportError as e:
    st.error(f"Error importing functions: {e}")
    st.stop()

# Configure logging to capture all logs
class StreamlitLogHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue
        self.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        
    def emit(self, record):
        log_entry = self.format(record)
        self.log_queue.put(log_entry)

# Create a queue to store log messages
log_queue = queue.Queue()

# Configure root logger to use our custom handler
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Remove existing handlers to avoid duplicates
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Add StreamlitLogHandler to root logger
streamlit_handler = StreamlitLogHandler(log_queue)
root_logger.addHandler(streamlit_handler)

# Also add a console handler so logs are printed to console too
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
root_logger.addHandler(console_handler)

# Configure Streamlit page
st.set_page_config(
    page_title="OWL Interview Assistant",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Summarization function - this will condense verbose outputs
def summarize_content(content, max_words=200):
    """Create a concise summary of longer content"""
    if not content or len(content.split()) <= max_words:
        return content
        
    # Simple summarization by truncating
    words = content.split()
    summary = " ".join(words[:max_words]) + "... (see full details below)"
    return summary

# Basic CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4A56E2;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f7ff;
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .raw-output {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        margin-top: 15px;
        max-height: 400px;
        overflow-y: auto;
        font-family: monospace;
        font-size: 0.9rem;
    }
    .summary-box {
        background-color: #e8f4ff;
        border-left: 5px solid #4A56E2;
        padding: 15px;
        margin-top: 15px;
        border-radius: 5px;
    }
    .file-list {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
    }
    .timer {
        font-size: 0.9rem;
        color: #666;
        margin-top: 5px;
        font-style: italic;
    }
    .quick-mode {
        color: #4CAF50;
        font-weight: bold;
    }
    .detailed-mode {
        color: #2196F3;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("<h1 class='main-header'>🦉 OWL Interview Assistant</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
    This intelligent interview preparation system uses OWL's advanced multi-agent capabilities to help you prepare 
    for job interviews. It researches companies, generates tailored interview questions, and creates 
    comprehensive preparation materials.
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.header("Interview Configuration")
    
    # Input fields
    job_role = st.sidebar.text_input("Job Role/Title", "Machine Learning Engineer")
    company_name = st.sidebar.text_input("Company Name", "Google")
    
    # Mode selection
    st.sidebar.subheader("Processing Mode")
    mode = st.sidebar.radio(
        "Select mode:",
        ["Quick Mode (3-4 searches)", "Detailed Mode (full research)"],
        index=0,
        help="Quick mode limits searches to conserve tokens and API usage"
    )
    detailed = "Detailed" in mode
    limited_searches = not detailed
    
    if detailed:
        st.sidebar.markdown("<p class='detailed-mode'>Detailed Mode: Comprehensive results (slower, uses more tokens)</p>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<p class='quick-mode'>Quick Mode: Concise results, limited to 3-4 searches</p>", unsafe_allow_html=True)
    
    # Create tabs with simple names
    tab1, tab2, tab3, tab4 = st.tabs(["Research", "Questions", "Prep Plan", "Files"])
    
    # Research Tab
    with tab1:
        st.header("Company Research")
        st.write("Research information about the company to help with your interview preparation.")
        
        # Button for research
        research_btn = st.button("Research Company", key="research_btn", use_container_width=True)
        
        if research_btn:
            with st.spinner(f"Researching {company_name}..."):
                try:
                    # Log the start of research
                    logging.info(f"Starting company research for {company_name}")
                    
                    # Progress indicator
                    progress = st.progress(0)
                    status = st.empty()
                    status.info("Starting research...")
                    progress.progress(10)
                    
                    # Start time tracking
                    start_time = time.time()
                    
                    # Run research (with limited searches if in quick mode)
                    result = research_company(company_name, detailed=detailed, limited_searches=limited_searches)
                    
                    # Update progress
                    progress.progress(100)
                    duration = time.time() - start_time
                    status.success(f"Research completed in {duration:.1f} seconds")
                    
                    # Display results in two parts: summary and raw output
                    st.subheader("Summary")
                    summary = summarize_content(result["answer"])
                    st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
                    
                    # Show generated files if any
                    if "generated_files" in result and result["generated_files"]:
                        st.success(f"Generated {len(result['generated_files'])} files")
                        with st.expander("View Generated Files"):
                            for file in result["generated_files"]:
                                st.markdown(f"📄 {os.path.basename(file)}")
                    
                    # Show the raw output (full response)
                    with st.expander("View Raw Output"):
                        st.markdown(f"<div class='raw-output'>{result['answer']}</div>", unsafe_allow_html=True)
                    
                    # Show execution time and token usage
                    st.markdown(f"<p class='timer'>Execution time: {duration:.2f} seconds | Token usage: {result['token_count'].get('completion_token_count', 0) + result['token_count'].get('prompt_token_count', 0)}</p>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    logging.error(f"Error in research: {str(e)}")
    
    # Questions Tab
    with tab2:
        st.header("Interview Questions Generator")
        st.write("Generate tailored questions for your upcoming interview.")
        
        question_type = st.selectbox(
            "Question Type",
            ["All", "Behavioral", "Technical", "Company-Specific"]
        )
        
        # Button for questions
        questions_btn = st.button("Generate Questions", key="questions_btn", use_container_width=True)
        
        if questions_btn:
            with st.spinner(f"Generating questions for {job_role} at {company_name}..."):
                try:
                    # Log start
                    logging.info(f"Starting question generation for {job_role} at {company_name}")
                    
                    # Progress indicator
                    progress = st.progress(0)
                    status = st.empty()
                    status.info("Starting question generation...")
                    progress.progress(10)
                    
                    # Start time tracking
                    start_time = time.time()
                    
                    # Run generation with limited searches in quick mode
                    result = generate_interview_questions(job_role, company_name, detailed=detailed, limited_searches=limited_searches)
                    
                    # Update progress
                    progress.progress(100)
                    duration = time.time() - start_time
                    status.success(f"Questions generated in {duration:.1f} seconds")
                    
                    # Display results in two parts: summary and raw output
                    st.subheader("Summary")
                    summary = summarize_content(result["answer"])
                    st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
                    
                    # Show generated files if any
                    if "generated_files" in result and result["generated_files"]:
                        st.success(f"Generated {len(result['generated_files'])} files")
                        with st.expander("View Generated Files"):
                            for file in result["generated_files"]:
                                st.markdown(f"📄 {os.path.basename(file)}")
                    
                    # Show the raw output (full response)
                    with st.expander("View Raw Output"):
                        st.markdown(f"<div class='raw-output'>{result['answer']}</div>", unsafe_allow_html=True)
                    
                    # Show execution time and token usage
                    st.markdown(f"<p class='timer'>Execution time: {duration:.2f} seconds | Token usage: {result['token_count'].get('completion_token_count', 0) + result['token_count'].get('prompt_token_count', 0)}</p>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    logging.error(f"Error in question generation: {str(e)}")
    
    # Preparation Plan Tab
    with tab3:
        st.header("Comprehensive Preparation Plan")
        st.write("Create a structured plan to prepare for your interview.")
        
        # Button for plan
        plan_btn = st.button("Create Preparation Plan", key="plan_btn", use_container_width=True)
        
        if plan_btn:
            with st.spinner(f"Creating preparation plan for {job_role} at {company_name}..."):
                try:
                    # Log start
                    logging.info(f"Starting preparation plan for {job_role} at {company_name}")
                    
                    # Progress indicator
                    progress = st.progress(0)
                    status = st.empty()
                    status.info("Starting plan creation...")
                    progress.progress(10)
                    
                    # Start time tracking
                    start_time = time.time()
                    
                    # Run plan creation with limited searches in quick mode
                    result = create_interview_prep_plan(job_role, company_name, detailed=detailed, limited_searches=limited_searches)
                    
                    # Update progress
                    progress.progress(100)
                    duration = time.time() - start_time
                    status.success(f"Plan created in {duration:.1f} seconds")
                    
                    # Display results in two parts: summary and raw output
                    st.subheader("Summary")
                    summary = summarize_content(result["answer"])
                    st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
                    
                    # Show generated files if any
                    if "generated_files" in result and result["generated_files"]:
                        st.success(f"Generated {len(result['generated_files'])} files")
                        with st.expander("View Generated Files"):
                            for file in result["generated_files"]:
                                st.markdown(f"📄 {os.path.basename(file)}")
                    
                    # Show the raw output (full response)
                    with st.expander("View Raw Output"):
                        st.markdown(f"<div class='raw-output'>{result['answer']}</div>", unsafe_allow_html=True)
                    
                    # Show execution time and token usage
                    st.markdown(f"<p class='timer'>Execution time: {duration:.2f} seconds | Token usage: {result['token_count'].get('completion_token_count', 0) + result['token_count'].get('prompt_token_count', 0)}</p>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    logging.error(f"Error in preparation plan: {str(e)}")
    
    # Files Tab
    with tab4:
        st.header("Generated Files")
        st.write("View and download files created during your session.")
        
        # Display files from interview_prep directory
        interview_prep_dir = Path("./interview_prep")
        if interview_prep_dir.exists():
            files = list(interview_prep_dir.glob("*"))
            
            if files:
                # Create columns for better layout
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.subheader("Available Files")
                    file_names = [file.name for file in files]
                    selected_file = st.selectbox("Select a file", file_names)
                
                with col2:
                    # Display selected file
                    selected_file_path = next((file for file in files if file.name == selected_file), None)
                    
                    if selected_file_path:
                        st.subheader(f"File: {selected_file}")
                        
                        # Add download button
                        with open(selected_file_path, "rb") as file:
                            st.download_button(
                                label=f"Download {selected_file}",
                                data=file,
                                file_name=selected_file,
                                mime="text/plain"
                            )
                        
                        # Display file content
                        try:
                            with open(selected_file_path, "r") as f:
                                content = f.read()
                            
                            # Determine display format based on file type
                            if selected_file_path.suffix.lower() == '.py':
                                st.code(content, language="python")
                            elif selected_file_path.suffix.lower() == '.md':
                                st.markdown(content)
                            else:
                                st.text_area("Content", content, height=400)
                                
                            # Show file stats
                            file_stats = selected_file_path.stat()
                            st.caption(f"Size: {file_stats.st_size/1024:.1f} KB | Modified: {time.ctime(file_stats.st_mtime)}")
                        
                        except Exception as e:
                            st.error(f"Error reading file: {str(e)}")
            else:
                st.info("No files have been generated yet. Use the tools in other tabs to create files.")
        else:
            st.info("The interview_prep directory will be created when you generate your first document.")
            
    # Footer
    st.markdown("---")
    with st.expander("View System Logs"):
        logs_output = st.empty()
        
        # Function to get logs from queue
        def get_logs():
            logs = []
            while not log_queue.empty():
                try:
                    log = log_queue.get_nowait()
                    logs.append(log)
                except queue.Empty:
                    break
            return logs
        
        # Display logs
        logs = get_logs()
        if logs:
            logs_output.code("\n".join(logs), language="text")
        else:
            logs_output.info("No logs available yet.")
        
        # Add refresh button
        if st.button("Refresh Logs"):
            logs = get_logs()
            if logs:
                logs_output.code("\n".join(logs), language="text")
            else:
                logs_output.info("No logs available yet.")

if __name__ == "__main__":
    try:
        logging.info("Starting OWL Interview Assistant application")
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logging.error(f"Application error: {str(e)}")