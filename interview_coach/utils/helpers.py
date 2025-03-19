import os
import json
import random
from typing import List, Dict, Any

def load_questions(industry: str, job_role: str) -> List[str]:
    """
    Load interview questions for a specific industry and job role.
    If the specific file doesn't exist, return generic questions.
    
    Args:
        industry (str): The industry for the interview
        job_role (str): The job role for the interview
        
    Returns:
        List[str]: A list of interview questions
    """
    # Path to the questions file - adjusted for OWL repository structure
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "questions", f"{job_role}.txt")
    
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            questions = [line.strip() for line in f.readlines() if line.strip()]
        return questions
    
    # Return generic questions if the specific file doesn't exist
    return get_generic_questions(industry, job_role)

def get_generic_questions(industry: str, job_role: str) -> List[str]:
    """
    Generate generic questions for a given industry and job role.
    
    Args:
        industry (str): The industry for the interview
        job_role (str): The job role for the interview
        
    Returns:
        List[str]: A list of generic interview questions
    """
    generic_questions = [
        f"Tell me about your experience in the {industry} industry and how it relates to this {job_role} position.",
        f"What are the most important skills for a {job_role} in the {industry} industry?",
        f"Describe a challenging project you worked on that demonstrates your qualifications for this {job_role} position.",
        f"How do you stay updated with the latest trends and technologies in the {industry} industry?",
        f"What approach do you use to solve complex problems as a {job_role}?",
        f"Describe a situation where you had to work under pressure to meet a deadline. How did you handle it?",
        f"How do you collaborate with team members to achieve project goals?",
        f"What is your greatest professional achievement as a {job_role}?",
        f"How do you handle constructive criticism of your work?",
        f"Where do you see yourself professionally in the next 5 years?",
    ]
    
    return generic_questions

def create_sample_questions_files():
    """
    Create sample question files for different job roles.
    This function is used to initialize the data directory with sample questions.
    """
    questions = {
        "software_engineer": [
            "Explain the concept of object-oriented programming and its principles.",
            "What is the difference between a thread and a process?",
            "Describe the differences between arrays and linked lists.",
            "How would you approach debugging a complex issue in a large codebase?",
            "Explain the concept of REST API and its principles.",
            "How do you ensure code quality in your projects?",
            "Describe a challenging bug you encountered and how you resolved it.",
            "What databases have you worked with, and what are the strengths and weaknesses of each?",
            "How would you design a scalable system for handling millions of users?",
            "What version control systems have you used, and how do you manage conflicts?"
        ],
        "data_scientist": [
            "Explain the difference between supervised and unsupervised learning.",
            "How would you handle imbalanced datasets in classification problems?",
            "Describe the bias-variance tradeoff in machine learning models.",
            "How would you approach a problem where you need to predict customer churn?",
            "Explain the concept of feature engineering and why it's important.",
            "What techniques do you use to validate the results of your analysis?",
            "How would you communicate complex analytical findings to non-technical stakeholders?",
            "Describe a project where you applied machine learning to solve a business problem.",
            "What is your approach to handling missing data in a dataset?",
            "How do you stay updated with the latest advancements in data science?"
        ],
        "product_manager": [
            "How do you prioritize features in a product roadmap?",
            "Describe your process for gathering and incorporating user feedback.",
            "How do you balance technical constraints with user experience considerations?",
            "Explain how you would measure the success of a new product feature.",
            "How do you collaborate with engineering, design, and other stakeholders?",
            "Describe a situation where you had to make a difficult product decision.",
            "What methodologies do you use for product development?",
            "How do you stay informed about market trends and competition?",
            "Describe how you would handle a situation where a key feature is delayed.",
            "What tools and techniques do you use to understand user needs?"
        ]
    }
    
    # Create the questions directory if it doesn't exist
    base_dir = os.path.dirname(os.path.dirname(__file__))
    os.makedirs(os.path.join(base_dir, "data", "questions"), exist_ok=True)
    
    # Create the question files
    for job_role, job_questions in questions.items():
        with open(os.path.join(base_dir, "data", "questions", f"{job_role}.txt"), "w") as f:
            for question in job_questions:
                f.write(question + "\n")
    
    print(f"Created sample question files in interview_coach/data/questions/ directory")

def ensure_data_directory():
    """
    Ensure that the data directory structure exists.
    """
    # Create directories if they don't exist
    base_dir = os.path.dirname(os.path.dirname(__file__))
    os.makedirs(os.path.join(base_dir, "data", "questions"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "output"), exist_ok=True)
    
    # Check if any question files exist, create samples if not
    question_files = os.listdir(os.path.join(base_dir, "data", "questions"))
    if not any(file.endswith(".txt") for file in question_files):
        create_sample_questions_files()