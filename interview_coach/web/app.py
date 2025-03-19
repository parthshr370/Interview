import streamlit as st
import os
import sys
import json
import datetime
from dotenv import load_dotenv

# Add the OWL repository root to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from interview_coach.interview.coach import InterviewCoach
from interview_coach.web.components import (
    render_sidebar, 
    render_welcome, 
    render_interview, 
    render_feedback, 
    render_final_report,
    render_api_setup_guide
)
from interview_coach.utils.helpers import ensure_data_directory

# Load environment variables for API keys
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Interview Coach",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state variables if they don't exist
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.coach = None
    st.session_state.current_question_idx = None
    st.session_state.current_question = None
    st.session_state.feedback = None
    st.session_state.interview_complete = False
    st.session_state.report = None
    st.session_state.report_path = None

def initialize_interview():
    """Initialize a new interview session"""
    industry = st.session_state.industry
    job_role = st.session_state.job_role
    question_count = st.session_state.question_count
    
    # Create a new coach
    st.session_state.coach = InterviewCoach(industry, job_role, question_count)
    
    # Get the first question
    idx, question = st.session_state.coach.get_current_question()
    st.session_state.current_question_idx = idx
    st.session_state.current_question = question
    
    # Mark as initialized
    st.session_state.initialized = True
    st.session_state.feedback = None
    st.session_state.interview_complete = False
    st.session_state.report = None
    st.session_state.report_path = None

def submit_response():
    """Submit a response to the current question"""
    if not st.session_state.initialized or st.session_state.interview_complete:
        return
    
    # Get response from session state
    response = st.session_state.response
    
    # If response is empty, show an error message
    if not response or response.strip() == "":
        st.error("Please provide an answer before submitting")
        return
    
    # Show a spinner while processing the response
    with st.spinner("Processing your response..."):
        # Process the response
        feedback = st.session_state.coach.process_response(
            st.session_state.current_question_idx, 
            response
        )
        st.session_state.feedback = feedback
        
        # Move to next question
        idx, question = st.session_state.coach.get_next_question()
        st.session_state.current_question_idx = idx
        st.session_state.current_question = question
        
        # Check if interview is complete
        if st.session_state.coach.is_interview_complete():
            st.session_state.interview_complete = True
            
            # Generate final report
            with st.spinner("Generating final report..."):
                report = st.session_state.coach.generate_final_report()
                st.session_state.report = report
                
                # Save report to file
                report_path = save_report(report)
                st.session_state.report_path = report_path

def save_report(report):
    """Save the report to a file"""
    # Create output directory if it doesn't exist
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{report['job_role']}_{report['industry']}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    
    # Save the report to a file
    with open(filepath, 'w') as f:
        f.write(f"INTERVIEW FEEDBACK REPORT\n")
        f.write(f"Job Role: {report['job_role'].replace('_', ' ').title()}\n")
        f.write(f"Industry: {report['industry'].title()}\n")
        f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(report['report'])
    
    return filepath

# Main app UI
def main():
    """Main function to run the Interview Coach application"""
    # Ensure data directory structure exists
    ensure_data_directory()
    
    st.title("💼 Interview Coach")
    st.write("Practice your interview skills and get instant feedback from AI")
    
    # Available industries and job roles
    industries = ["tech", "finance", "healthcare", "marketing", "education"]
    job_roles = ["software_engineer", "data_scientist", "product_manager", "marketing_manager", "teacher"]
    
    # Render sidebar for configuration
    industry, job_role, question_count, start_button = render_sidebar(industries, job_roles)
    
    # Check if OpenRouter API key is set
    if not os.environ.get("OPENROUTER_API_KEY") and not os.environ.get("OPENAI_API_KEY"):
        render_api_setup_guide()
        st.warning("⚠️ OpenRouter API key not found. Please set up your API key to use this application.")
    
    # Handle initialization
    if start_button:
        initialize_interview()
    
    # Main content area
    if not st.session_state.initialized:
        # Show welcome message when not initialized
        render_welcome()
    else:
        # Show the interview interface
        if not st.session_state.interview_complete:
            # Display current question and get response
            response, submit_button = render_interview(
                st.session_state.current_question_idx,
                st.session_state.current_question
            )
            
            # Process submission
            if submit_button:
                submit_response()
            
            # Display feedback if available
            if st.session_state.feedback:
                render_feedback(st.session_state.feedback)
        
        else:
            # Display final report
            new_interview = render_final_report(st.session_state.report, st.session_state.report_path)
            
            # Start a new interview if requested
            if new_interview:
                initialize_interview()

# Run the app
if __name__ == "__main__":
    main()