import re
from typing import Dict, Any

def format_feedback(raw_feedback: str) -> str:
    """
    Format the raw feedback into a more structured and readable format.
    
    Args:
        raw_feedback (str): The raw feedback from the OWL system
        
    Returns:
        str: Formatted feedback with Markdown formatting
    """
    # Check if the feedback is already well-structured with headers
    if "## Strengths" in raw_feedback or "### Strengths" in raw_feedback:
        return raw_feedback
    
    # Extract key sections using regex patterns
    content_match = re.search(r"(?:Content relevance|Content|Relevance)(.*?)(?:Technical|Communication|Strengths|Areas|$)", raw_feedback, re.DOTALL)
    technical_match = re.search(r"(?:Technical accuracy|Technical)(.*?)(?:Communication|Strengths|Areas|$)", raw_feedback, re.DOTALL)
    communication_match = re.search(r"(?:Communication clarity|Communication)(.*?)(?:Strengths|Areas|$)", raw_feedback, re.DOTALL)
    strengths_match = re.search(r"(?:Strengths)(.*?)(?:Areas|Improvement|$)", raw_feedback, re.DOTALL)
    improvement_match = re.search(r"(?:Areas for improvement|Improvement|Weaknesses|Areas)(.*?)(?:$)", raw_feedback, re.DOTALL)
    
    # Format the feedback with Markdown
    formatted_feedback = "# Interview Response Feedback\n\n"
    
    if content_match:
        formatted_feedback += "## Content Relevance and Completeness\n"
        formatted_feedback += content_match.group(1).strip() + "\n\n"
    
    if technical_match:
        formatted_feedback += "## Technical Accuracy\n"
        formatted_feedback += technical_match.group(1).strip() + "\n\n"
    
    if communication_match:
        formatted_feedback += "## Communication Clarity\n"
        formatted_feedback += communication_match.group(1).strip() + "\n\n"
    
    if strengths_match:
        formatted_feedback += "## Strengths\n"
        formatted_feedback += strengths_match.group(1).strip() + "\n\n"
    
    if improvement_match:
        formatted_feedback += "## Areas for Improvement\n"
        formatted_feedback += improvement_match.group(1).strip() + "\n\n"
        
    # If no sections were matched, just return the raw feedback with a header
    if formatted_feedback == "# Interview Response Feedback\n\n":
        return f"# Interview Response Feedback\n\n{raw_feedback}"
    
    return formatted_feedback