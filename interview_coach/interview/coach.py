import json
from typing import Dict, List, Any, Tuple

from camel.societies import RolePlaying
# Use OWL's run_society directly - this is now available since we're inside the OWL repo
from owl.utils import run_society  

from interview_coach.interview.agent_manager import setup_interview_society
from interview_coach.interview.feedback import format_feedback
from interview_coach.utils.helpers import load_questions

class InterviewCoach:
    """
    Core class that manages the interview process and interaction with OWL.
    """
    def __init__(self, industry: str, job_role: str, question_count: int = 5):
        """
        Initialize the interview coach.
        
        Args:
            industry (str): The industry for the interview
            job_role (str): The job role for the interview
            question_count (int): Number of questions to ask
        """
        self.industry = industry
        self.job_role = job_role
        self.question_count = question_count
        
        # Initialize questions
        self.questions = load_questions(industry, job_role)[:question_count]
        self.current_question_idx = 0
        
        # Store responses and feedback
        self.responses = []
        
        # Set up OWL society
        self.society = setup_interview_society(industry, job_role)
    
    def get_current_question(self) -> Tuple[int, str]:
        """
        Get the current question.
        
        Returns:
            Tuple[int, str]: The index and text of the current question
        """
        if self.current_question_idx < len(self.questions):
            return self.current_question_idx, self.questions[self.current_question_idx]
        return -1, "Interview complete"
    
    def get_next_question(self) -> Tuple[int, str]:
        """
        Move to and return the next question.
        
        Returns:
            Tuple[int, str]: The index and text of the next question
        """
        self.current_question_idx += 1
        return self.get_current_question()
    
    def is_interview_complete(self) -> bool:
        """
        Check if all questions have been answered.
        
        Returns:
            bool: True if the interview is complete, False otherwise
        """
        return self.current_question_idx >= len(self.questions)
    
    def process_response(self, question_idx: int, response_text: str) -> Dict[str, Any]:
        """
        Process a user's response using OWL and return feedback.
        
        Args:
            question_idx (int): The index of the question being answered
            response_text (str): The user's response text
            
        Returns:
            Dict[str, Any]: A dictionary containing the raw and formatted feedback
        """
        # Get the question text
        question = self.questions[question_idx]
        
        # Prepare the query for OWL
        query = f"""
        Analyze this interview response for a {self.job_role} position in {self.industry}.
        
        Question: {question}
        
        Response: {response_text}
        
        Provide detailed feedback on:
        1. Content relevance and completeness
        2. Technical accuracy
        3. Communication clarity
        4. Strengths
        5. Areas for improvement
        
        Format your feedback with clear sections for each of the above points.
        """
        
        # Process the response with OWL
        raw_feedback, chat_history, token_count = run_society(self.society, query)
        
        # Format the feedback
        formatted_feedback = format_feedback(raw_feedback)
        
        # Store the question, response, and feedback
        self.responses.append({
            "question_idx": question_idx,
            "question": question,
            "response": response_text,
            "feedback": raw_feedback
        })
        
        return {
            "raw_feedback": raw_feedback,
            "formatted_feedback": formatted_feedback
        }
    
    def generate_final_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive feedback report based on all responses.
        
        Returns:
            Dict[str, Any]: A dictionary containing the report and related data
        """
        # Prepare the query for generating the final report
        query = f"""
        Generate a comprehensive interview feedback report for a {self.job_role} position in {self.industry}.
        
        Here are all the questions, responses, and individual feedback from the interview:
        
        {json.dumps(self.responses, indent=2)}
        
        The report should include:
        1. Overall assessment
        2. Key strengths observed
        3. Priority areas for improvement
        4. Specific technical knowledge gaps (if any)
        5. Communication style feedback
        6. Recommended preparation strategies for future interviews
        7. Resources for improvement
        
        Format the report in a professional and constructive manner with Markdown formatting.
        """
        
        # Generate the report using OWL
        report, chat_history, token_count = run_society(self.society, query)
        
        return {
            "report": report,
            "responses": self.responses,
            "job_role": self.job_role,
            "industry": self.industry
        }