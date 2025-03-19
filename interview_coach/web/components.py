import os
import streamlit as st

def render_sidebar(industries, job_roles):
    """
    Render the sidebar with interview configuration options.
    
    Args:
        industries (list): List of available industries
        job_roles (list): List of available job roles
        
    Returns:
        tuple: Selected industry, job role, and question count
    """
    st.sidebar.header("Interview Settings")
    
    # Industry selection
    industry = st.sidebar.selectbox(
        "Industry", 
        industries,
        key="industry"
    )
    
    # Job role selection
    job_role = st.sidebar.selectbox(
        "Job Role",
        job_roles,
        key="job_role"
    )
    
    # Question count
    question_count = st.sidebar.slider(
        "Number of Questions",
        min_value=3,
        max_value=10,
        value=5,
        key="question_count"
    )
    
    # Initialize button
    start_button = st.sidebar.button(
        "Start New Interview",
        key="start_button"
    )
    
    return industry, job_role, question_count, start_button

def render_welcome():
    """Render the welcome screen with sample questions."""
    st.write("## Welcome to Interview Coach!")
    st.write("Configure your interview settings in the sidebar and click 'Start New Interview' to begin.")
    
    # Sample questions preview
    with st.expander("Sample Questions Preview"):
        st.write("Here are some sample questions for different roles:")
        st.write("### Software Engineer")
        st.write("- Explain the concept of object-oriented programming and its principles.")
        st.write("- What is the difference between a thread and a process?")
        
        st.write("### Data Scientist")
        st.write("- Explain the difference between supervised and unsupervised learning.")
        st.write("- How would you handle imbalanced datasets in classification problems?")
        
        st.write("### Product Manager")
        st.write("- How do you prioritize features in a product roadmap?")
        st.write("- What methodologies do you use for product development?")

def render_interview(question_idx, question):
    """
    Render the current interview question and response input.
    
    Args:
        question_idx (int): Index of the current question
        question (str): Text of the current question
        
    Returns:
        str: User's response to the question
    """
    st.write(f"## Question {question_idx + 1}:")
    st.write(question)
    
    # Response input
    response = st.text_area(
        "Your Answer",
        key="response",
        height=150
    )
    
    # Submit button
    submit_button = st.button(
        "Submit Answer",
        key="submit_button"
    )
    
    return response, submit_button

def render_feedback(feedback):
    """
    Render feedback for the previous response.
    
    Args:
        feedback (dict): Feedback dictionary with formatted_feedback
    """
    with st.container():
        st.write("## Feedback on Previous Answer:")
        st.markdown(feedback["formatted_feedback"])

def render_final_report(report, report_path):
    """
    Render the final interview report.
    
    Args:
        report (dict): Report dictionary with report text and metadata
        report_path (str): Path to the saved report file
    """
    st.write("## 🎉 Interview Complete!")
    st.write("Here's your comprehensive feedback report:")
    
    with st.container():
        st.markdown(report["report"])
    
    # Download button for report
    if report_path:
        with open(report_path, "r") as f:
            report_content = f.read()
        
        st.download_button(
            label="Download Full Report",
            data=report_content,
            file_name=os.path.basename(report_path),
            mime="text/plain"
        )
    
    # Option to start a new interview
    new_interview = st.button(
        "Start a New Interview",
        key="new_interview_button"
    )
    
    return new_interview

def render_api_setup_guide():
    """Render a guide for setting up API keys."""
    with st.sidebar.expander("API Key Setup"):
        st.markdown("""
        ### Setting up OpenRouter API Key for Gemini
        
        1. Create an account on [OpenRouter](https://openrouter.ai/)
        2. Generate an API key
        3. Create a `.env` file in the project root
        4. Add your API key: `OPENROUTER_API_KEY=your_key_here`
        5. Restart the application
        
        Alternatively, you can set it as an environment variable before running the app.
        """)