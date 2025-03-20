import os
import streamlit as st
import pandas as pd
from pathlib import Path
import logging
import queue
import threading
import time
import sys
import io
import re

# Add parent directory to path for OWL imports if needed
sys.path.append('../')

# Create a StringIO object to capture logs
log_capture_string = io.StringIO()

# Create a custom handler that writes to both the StringIO and session state
class CaptureHandler(logging.Handler):
    def __init__(self, string_io):
        super().__init__()
        self.string_io = string_io
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
    def emit(self, record):
        log_entry = self.format(record)
        
        # Write to StringIO
        self.string_io.write(log_entry + '\n')
        
        # Add to session state if available
        if 'log_entries' in st.session_state:
            st.session_state.log_entries.append(log_entry)

# Initialize session state for logs if it doesn't exist
if 'log_entries' not in st.session_state:
    st.session_state.log_entries = []

# Set up logging
logging.basicConfig(level=logging.INFO)
root_logger = logging.getLogger()

# Remove existing handlers to avoid duplicates
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Add console handler so logs are printed to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
root_logger.addHandler(console_handler)

# Add our capture handler
capture_handler = CaptureHandler(log_capture_string)
root_logger.addHandler(capture_handler)

# Generate initial log messages
logging.info("🚀 Logging system initialized")
logging.info("📋 OWL Interview Assistant starting")

# Try to import the necessary functions
try:
    from main import research_company, generate_interview_questions, create_interview_prep_plan
except ImportError as e:
    st.error(f"Error importing functions: {e}")
    st.stop()

# Function to sanitize logs to avoid exposing sensitive information
def sanitize_log(log_message):
    """
    Sanitize log messages to avoid exposing sensitive information like IPs.
    """
    # Simple IP address pattern matching
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    sanitized = re.sub(ip_pattern, '[REDACTED_IP]', log_message)
    
    # Redact API keys (common patterns)
    api_key_pattern = r'(api[_-]?key|apikey|key|token)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9]{20,})["\']?'
    sanitized = re.sub(api_key_pattern, r'\1: [REDACTED_API_KEY]', sanitized, flags=re.IGNORECASE)
    
    # Redact URLs with authentication information
    url_auth_pattern = r'(https?://)([^:@/]+:[^@/]+@)([^\s/]+)'
    sanitized = re.sub(url_auth_pattern, r'\1[REDACTED_AUTH]@\3', sanitized)
    
    return sanitized

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
    .log-container {
        background-color: #1E1E1E;
        color: #CCCCCC;
        font-family: 'Courier New', monospace;
        padding: 15px;
        border-radius: 5px;
        height: 700px;
        overflow-y: auto;
        margin-top: 10px;
        width: 100%;
    }
    .log-entry {
        margin: 2px 0;
        line-height: 1.4;
    }
    .log-info {
        color: #4CAF50;
    }
    .log-warning {
        color: #FFC107;
    }
    .log-error {
        color: #F44336;
    }
    .log-tool {
        color: #2196F3;
    }
    .log-agent {
        color: #9C27B0;
    }
    /* Add styles for specific log types */
    .emoji-agent {
        color: #E91E63;
    }
    .emoji-tool {
        color: #2196F3;
    }
    .emoji-complete {
        color: #4CAF50;
    }
    .emoji-error {
        color: #F44336;
    }
    .emoji-search {
        color: #FF9800;
    }
    .log-header {
        background-color: #333;
        color: white;
        padding: 8px 15px;
        border-radius: 5px 5px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .complete-results-box {
        background-color: #f9f9f9;
        border-left: 5px solid #4A56E2;
        padding: 20px;
        margin-top: 15px;
        border-radius: 5px;
        font-size: 0.95rem;
        line-height: 1.6;
        max-height: none;
        overflow-y: visible;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Add a log to show main function started
    logging.info("📊 Starting main application function")
    
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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Research", "Questions", "Prep Plan", "Files", "Live Logs"])
    
    # Live Logs Tab with the new implementation
    with tab5:
        st.header("Live Agent Activity Logs")
        st.write("Watch the OWL agents and tools in action as they work on your request.")
        
        # Add controls
        col1, col2 = st.columns([1, 1])
        
        with col1:
            auto_refresh = st.checkbox("Auto-refresh logs", value=True)
        
        with col2:
            if st.button("Clear logs"):
                # Clear logs from session state
                st.session_state.log_entries = []
                # Clear the StringIO
                log_capture_string.truncate(0)
                log_capture_string.seek(0)
                st.rerun()
        
        # Create log container
        logs_container = st.empty()
        
        # Process logs for display
        formatted_logs = []
        for log in st.session_state.log_entries:
            # Apply color formatting based on log content
            if "ERROR" in log:
                formatted_logs.append(f'<div class="log-entry log-error">{log}</div>')
            elif "WARNING" in log:
                formatted_logs.append(f'<div class="log-entry log-warning">{log}</div>')
            elif "🔧" in log or "🧰" in log:
                formatted_logs.append(f'<div class="log-entry emoji-tool">{log}</div>')
            elif "✅" in log or "🚀" in log:
                formatted_logs.append(f'<div class="log-entry emoji-complete">{log}</div>')
            elif "❌" in log:
                formatted_logs.append(f'<div class="log-entry emoji-error">{log}</div>')
            elif "🔍" in log:
                formatted_logs.append(f'<div class="log-entry emoji-search">{log}</div>')
            else:
                formatted_logs.append(f'<div class="log-entry log-info">{log}</div>')
        
        # Display logs
        all_logs_html = "".join(formatted_logs)
        logs_container.markdown(f'<div class="log-container">{all_logs_html}</div>', unsafe_allow_html=True)
        
        # Show log count
        st.caption(f"Total logs: {len(st.session_state.log_entries)}")
        
        # Add test button for debugging
        if st.button("Generate test log"):
            logging.info(f"🔔 Test log at {time.strftime('%H:%M:%S')}")
            st.rerun()
        
        # Auto-refresh if enabled
        if auto_refresh:
            time.sleep(1)  # Wait for 1 second
            st.rerun()
    
    # Research Tab
    with tab1:
        st.header("Company Research")
        st.write("Research information about the company to help with your interview preparation.")
        
        # Button for research
        research_btn = st.button("Research Company", key="research_btn", use_container_width=True)
        
        if research_btn:
            with st.spinner(f"Researching {company_name}..."):
                try:
                    # Log the start of research with emoji
                    logging.info(f"🔍 STARTING COMPANY RESEARCH for {company_name}")
                    
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
                    
                    # Display complete results
                    st.subheader("Complete Results")
                    st.markdown(f"<div class='complete-results-box'>{result['answer']}</div>", unsafe_allow_html=True)
                    
                    # Show generated files if any
                    if "generated_files" in result and result["generated_files"]:
                        st.success(f"Generated {len(result['generated_files'])} files")
                        with st.expander("View Generated Files"):
                            for file in result["generated_files"]:
                                st.markdown(f"📄 {os.path.basename(file)}")
                    
                    # Log completion with emoji
                    logging.info(f"✅ COMPANY RESEARCH COMPLETED for {company_name} in {duration:.2f} seconds")
                    
                    # Show execution time and token usage
                    st.markdown(f"<p class='timer'>Execution time: {duration:.2f} seconds | Token usage: {result['token_count'].get('completion_token_count', 0) + result['token_count'].get('prompt_token_count', 0)}</p>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    logging.error(f"❌ ERROR IN COMPANY RESEARCH: {str(e)}")
    
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
                    # Log start with emoji
                    logging.info(f"❓ GENERATING INTERVIEW QUESTIONS for {job_role} at {company_name}")
                    
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
                    
                    # Display complete results
                    st.subheader("Complete Results")
                    st.markdown(f"<div class='complete-results-box'>{result['answer']}</div>", unsafe_allow_html=True)
                    
                    # Show generated files if any
                    if "generated_files" in result and result["generated_files"]:
                        st.success(f"Generated {len(result['generated_files'])} files")
                        with st.expander("View Generated Files"):
                            for file in result["generated_files"]:
                                st.markdown(f"📄 {os.path.basename(file)}")
                    
                    # Log completion with emoji
                    logging.info(f"✅ QUESTION GENERATION COMPLETED for {job_role} at {company_name} in {duration:.2f} seconds")
                    
                    # Show execution time and token usage
                    st.markdown(f"<p class='timer'>Execution time: {duration:.2f} seconds | Token usage: {result['token_count'].get('completion_token_count', 0) + result['token_count'].get('prompt_token_count', 0)}</p>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    logging.error(f"❌ ERROR IN QUESTION GENERATION: {str(e)}")
    
    # Preparation Plan Tab
    with tab3:
        st.header("Comprehensive Preparation Plan")
        st.write("Create a structured plan to prepare for your interview.")
        
        # Button for plan
        plan_btn = st.button("Create Preparation Plan", key="plan_btn", use_container_width=True)
        
        if plan_btn:
            with st.spinner(f"Creating preparation plan for {job_role} at {company_name}..."):
                try:
                    # Log start with emoji
                    logging.info(f"📋 CREATING PREPARATION PLAN for {job_role} at {company_name}")
                    
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
                    
                    # Display complete results
                    st.subheader("Complete Results")
                    st.markdown(f"<div class='complete-results-box'>{result['answer']}</div>", unsafe_allow_html=True)
                    
                    # Show generated files if any
                    if "generated_files" in result and result["generated_files"]:
                        st.success(f"Generated {len(result['generated_files'])} files")
                        with st.expander("View Generated Files"):
                            for file in result["generated_files"]:
                                st.markdown(f"📄 {os.path.basename(file)}")
                    
                    # Log completion with emoji
                    logging.info(f"✅ PREPARATION PLAN COMPLETED for {job_role} at {company_name} in {duration:.2f} seconds")
                    
                    # Show execution time and token usage
                    st.markdown(f"<p class='timer'>Execution time: {duration:.2f} seconds | Token usage: {result['token_count'].get('completion_token_count', 0) + result['token_count'].get('prompt_token_count', 0)}</p>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    logging.error(f"❌ ERROR IN PREPARATION PLAN: {str(e)}")
    
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

if __name__ == "__main__":
    try:
        logging.info("🚀 STARTING OWL Interview Assistant application")
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logging.error(f"❌ APPLICATION ERROR: {str(e)}")