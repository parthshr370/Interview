import os
import logging
import time
from typing import Dict, Any, List, Tuple
from pathlib import Path
import sys

# Add parent directory to path for OWL imports
sys.path.append('../')

from dotenv import load_dotenv
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.toolkits import (
    SearchToolkit, 
    BrowserToolkit, 
    CodeExecutionToolkit, 
    FileWriteToolkit
)
from camel.societies import RolePlaying
from owl.utils import run_society

# Import prompt templates
from config.prompts import (
    get_system_prompt, 
    get_company_research_prompt, 
    get_question_generator_prompt,
    get_preparation_plan_prompt
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create the output directory for interview preparation materials
INTERVIEW_PREP_DIR = "./interview_prep"
os.makedirs(INTERVIEW_PREP_DIR, exist_ok=True)

def construct_interview_assistant(
    job_description: str, 
    company_name: str,
    detailed: bool = False,
    limited_searches: bool = True
) -> RolePlaying:
    """
    Construct a specialized interview preparation assistant using OWL.
    
    Args:
        job_description (str): The job description or role name
        company_name (str): The target company name
        detailed (bool): Whether to use all available tools (slower but more comprehensive)
        limited_searches (bool): Whether to limit the number of searches to conserve tokens
    
    Returns:
        RolePlaying: A configured society of agents ready to help with interview preparation
    """
    # Determine which API key and model to use based on available environment variables
    if os.environ.get("OPENROUTER_API_KEY"):
        logger.info("Using OpenRouter with Gemini model")
        model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
            api_key=os.environ.get("OPENROUTER_API_KEY"),
            model_type="google/gemini-pro",
            url="https://openrouter.ai/api/v1",
            model_config_dict={
                "temperature": 0.3,  # Lower temperature for more focused outputs
                "max_tokens": 4000
            }
        )
    elif os.environ.get("OPENAI_API_KEY"):
        logger.info("Using OpenAI model")
        model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
            model_config_dict={"temperature": 0.3}  # Lower temperature for more focused outputs
        )
    else:
        raise ValueError("Either OPENAI_API_KEY or OPENROUTER_API_KEY must be set in environment variables")
    
    # Configure toolkits - use different sets based on detailed flag
    essential_tools = [
        SearchToolkit().search_duckduckgo,
        SearchToolkit().search_wiki,
        *FileWriteToolkit(output_dir=INTERVIEW_PREP_DIR).get_tools(),
    ]
    
    # Add Google search if API key is available
    if os.environ.get("GOOGLE_API_KEY") and os.environ.get("SEARCH_ENGINE_ID"):
        essential_tools.append(SearchToolkit().search_google)
    
    if detailed:
        # Full set of tools for comprehensive tasks
        tools = [
            *essential_tools,
            *BrowserToolkit(
                headless=True,  # Set to True for headless mode in production
                web_agent_model=model,
                planning_agent_model=model,
            ).get_tools(),
            *CodeExecutionToolkit(sandbox="subprocess", verbose=True).get_tools(),
        ]
        logger.info("Using full toolset for comprehensive results")
    else:
        # Limited set of tools for faster operation
        tools = essential_tools
        logger.info("Using essential toolset for faster results")
    
    # Configure agent roles and parameters
    user_agent_kwargs = {"model": model}
    assistant_agent_kwargs = {"model": model, "tools": tools}
    
    # Get base system prompt and enhance with specifics
    base_prompt = get_system_prompt()
    
    # Add specific instructions to limit searches if needed
    search_limit_instruction = ""
    if limited_searches:
        search_limit_instruction = """
IMPORTANT CONSTRAINT: 
To conserve tokens and API usage, you must limit your research to a MAXIMUM OF 3-4 SEARCHES total.
Focus on the most important information and be concise in your responses.
Do not use web browsing unless absolutely necessary.
Prioritize quality over quantity in your information gathering.
"""
    
    enhanced_prompt = f"""{base_prompt}

Task: Help me prepare for an interview at {company_name} for the position of {job_description}.

Requirements:
1. Research thoroughly and provide substantial, useful information
2. Create well-structured content that is easy to understand
3. Save all generated materials in the '{INTERVIEW_PREP_DIR}' directory
4. Focus on actionable insights and practical advice
5. Format the output with clear sections and subsections
6. Ensure all information is specific to {company_name} and the {job_description} role

{search_limit_instruction}
"""
    
    # Configure task parameters
    task_kwargs = {
        "task_prompt": enhanced_prompt,
        "with_task_specify": False,
    }
    
    # Create and return the society
    society = RolePlaying(
        **task_kwargs,
        user_role_name="job_seeker",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="interview_coach",
        assistant_agent_kwargs=assistant_agent_kwargs,
    )
    
    return society

def research_company(company_name: str, detailed: bool = False, limited_searches: bool = True) -> Dict[str, Any]:
    """
    Research a company using the OWL system.
    
    Args:
        company_name (str): The name of the company to research
        detailed (bool): Whether to use the full toolset for detailed results
        limited_searches (bool): Whether to limit the number of searches
        
    Returns:
        Dict[str, Any]: Company research results
    """
    start_time = time.time()
    logging.info(f"Beginning company research for {company_name}")
    
    # Get enhanced prompt with specific requirements
    base_prompt = get_company_research_prompt(company_name)
    
    # Add search limiting instructions if needed
    search_limit_text = ""
    if limited_searches:
        search_limit_text = """
IMPORTANT: You must limit your research to a MAXIMUM OF 3-4 SEARCHES total.
Focus on the most crucial information that a candidate would need for an interview.
Prioritize quality over quantity in your information gathering.
"""
    
    enhanced_prompt = f"""{base_prompt}

Additional Requirements:
1. Format the research as a professional report with clear sections
2. Include direct quotes and statistics where available
3. Analyze the company culture and interview process
4. Save the research as a well-formatted markdown file
5. Focus on information that would be directly useful in an interview

{search_limit_text}

The file must include these key sections:
- Company Overview & History
- Products and Services
- Company Culture & Values
- Recent News & Developments
- Interview Process & Known Questions
- Key Talking Points for Interview

Remember to synthesize your findings into a cohesive document.
"""
    
    society = construct_interview_assistant("", company_name, detailed=detailed, limited_searches=limited_searches)
    society.task_prompt = enhanced_prompt
    
    logging.info(f"Running research with {'detailed' if detailed else 'basic'} mode")
    
    answer, chat_history, token_count = run_society(society)
    
    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Completed company research for {company_name} in {duration:.2f} seconds")
    logging.info(f"Token usage: {token_count}")
    
    # List generated files
    generated_files = []
    for file in Path(INTERVIEW_PREP_DIR).glob("*"):
        if file.is_file():
            generated_files.append(str(file))
            logging.info(f"Generated file: {file}")
    
    return {
        "answer": answer,
        "chat_history": chat_history,
        "token_count": token_count,
        "generated_files": generated_files,
        "duration_seconds": duration
    }

def generate_interview_questions(job_role: str, company_name: str, detailed: bool = False, limited_searches: bool = True) -> Dict[str, Any]:
    """
    Generate interview questions tailored for a specific job and company.
    
    Args:
        job_role (str): The job role or title
        company_name (str): The target company name
        detailed (bool): Whether to use the full toolset for detailed results
        limited_searches (bool): Whether to limit the number of searches
        
    Returns:
        Dict[str, Any]: Generated interview questions and resources
    """
    start_time = time.time()
    logging.info(f"Starting question generation for {job_role} at {company_name}")
    
    # Get enhanced prompt with specific requirements
    base_prompt = get_question_generator_prompt(job_role, company_name)
    
    # Add search limiting instructions if needed
    search_limit_text = ""
    if limited_searches:
        search_limit_text = """
IMPORTANT: You must limit your research to a MAXIMUM OF 3-4 SEARCHES total.
Focus on creating high-quality, relevant questions rather than an exhaustive list.
Prioritize questions that are most likely to be asked based on minimal research.
"""

    enhanced_prompt = f"""{base_prompt}

Additional Requirements:
1. Generate high-quality questions with sample answers
2. Format the content with clear categories
3. Include a section on "How to Prepare" for each category
4. For technical questions, include practical scenarios
5. Create a separate "Quick Reference" file with just the questions for practice

{search_limit_text}

The questions should be organized into these categories:
- Technical Skills (specific to {job_role})
- Behavioral/Soft Skills
- Company-Specific Knowledge
- Role-Specific Scenarios
- Questions to Ask the Interviewer

Research and create questions that are specifically tailored to {company_name}'s interview process 
and the {job_role} position.
"""
    
    society = construct_interview_assistant(job_role, company_name, detailed=detailed, limited_searches=limited_searches)
    society.task_prompt = enhanced_prompt
    
    logging.info(f"Running question generation with {'detailed' if detailed else 'basic'} mode")
    
    answer, chat_history, token_count = run_society(society)
    
    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Completed question generation for {job_role} at {company_name} in {duration:.2f} seconds")
    logging.info(f"Token usage: {token_count}")
    
    # List generated files
    generated_files = []
    for file in Path(INTERVIEW_PREP_DIR).glob("*"):
        if file.is_file():
            generated_files.append(str(file))
            logging.info(f"Generated file: {file}")
    
    return {
        "answer": answer,
        "chat_history": chat_history,
        "token_count": token_count,
        "generated_files": generated_files,
        "duration_seconds": duration
    }

def create_interview_prep_plan(job_role: str, company_name: str, detailed: bool = False, limited_searches: bool = True) -> Dict[str, Any]:
    """
    Create a comprehensive interview preparation plan.
    
    Args:
        job_role (str): The job role or title
        company_name (str): The target company name
        detailed (bool): Whether to use the full toolset for detailed results
        limited_searches (bool): Whether to limit the number of searches
        
    Returns:
        Dict[str, Any]: Interview preparation plan and resources
    """
    start_time = time.time()
    logging.info(f"Starting preparation plan creation for {job_role} at {company_name}")
    
    # Get enhanced prompt with specific requirements
    base_prompt = get_preparation_plan_prompt(job_role, company_name)
    
    # Add search limiting instructions if needed
    search_limit_text = ""
    if limited_searches:
        search_limit_text = """
IMPORTANT: You must limit your research to a MAXIMUM OF 3-4 SEARCHES total.
Focus on creating a practical, concise plan that is realistic for the candidate to implement.
Prioritize the most important preparation activities based on minimal research.
"""
    
    enhanced_prompt = f"""{base_prompt}

Additional Requirements:
1. Create a practical preparation plan that can be implemented in 7-10 days
2. Include specific daily tasks with reasonable time allocations
3. Provide a brief "Interview Day Checklist"
4. Create a separate "Key Talking Points" reference for quick review
5. Focus on the most important technical topics to review

{search_limit_text}

The preparation plan should include these components:
- Daily Schedule with specific activities
- Technical Skills Review Guide
- Company Knowledge Preparation
- Behavioral Questions Preparation
- Interview Day Preparation

The plan should be tailored specifically to {company_name}'s interview process and the {job_role} position.
"""
    
    society = construct_interview_assistant(job_role, company_name, detailed=detailed, limited_searches=limited_searches)
    society.task_prompt = enhanced_prompt
    
    logging.info(f"Running preparation plan creation with {'detailed' if detailed else 'basic'} mode")
    
    answer, chat_history, token_count = run_society(society)
    
    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Completed preparation plan creation in {duration:.2f} seconds")
    logging.info(f"Token usage: {token_count}")
    
    # List generated files
    generated_files = []
    for file in Path(INTERVIEW_PREP_DIR).glob("*"):
        if file.is_file():
            generated_files.append(str(file))
            logging.info(f"Generated file: {file}")
    
    return {
        "answer": answer,
        "chat_history": chat_history,
        "token_count": token_count,
        "generated_files": generated_files,
        "duration_seconds": duration
    }

# Example usage
if __name__ == "__main__":
    job_role = "Machine Learning Engineer"
    company_name = "Google"
    
    # Use limited searches by default
    result = create_interview_prep_plan(job_role, company_name, limited_searches=True)
    print(f"Answer: {result['answer']}")
    print(f"Generated files: {result['generated_files']}")
    print(f"Execution time: {result['duration_seconds']:.2f} seconds")