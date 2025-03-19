import os
from typing import Dict, Any
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.toolkits import CodeExecutionToolkit
from camel.societies import RolePlaying
from interview_coach.config.prompts import get_system_prompt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_interview_society(industry: str, job_role: str) -> RolePlaying:
    """
    Set up the OWL agent society for the interview using OpenRouter and Gemini.
    
    Args:
        industry (str): Industry for the interview
        job_role (str): Job role for the interview
    Returns:
        RolePlaying: A configured society of agents ready to conduct the interview
    """
    # Get OpenRouter API key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY must be set in environment variables")
    
    # Create model for the agents with OpenRouter and Gemini
    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        api_key=api_key,
        model_type="google/gemini-2.0-flash-001",
        url="https://openrouter.ai/api/v1",
        model_config_dict={
            "temperature": 0.8, 
            "max_tokens": 4000}
    )
    
    # Tools configuration
    tools = [
        *CodeExecutionToolkit(sandbox="subprocess").get_tools(),
    ]
    
    # Configure all agents to use the same OpenRouter model
    common_kwargs = {
        "model": model
    }
    
    user_agent_kwargs = common_kwargs.copy()
    
    assistant_agent_kwargs = common_kwargs.copy()
    assistant_agent_kwargs["tools"] = tools
    
    # Task specify agent kwargs - crucial for the internal agent
    task_specify_agent_kwargs = common_kwargs.copy()
    
    # Create and return the society with all agents using OpenRouter
    return RolePlaying(
        task_prompt=f"Conduct an interview for a {job_role} position in the {industry} industry, "
                   f"asking relevant questions and providing detailed feedback on responses.",
        user_role_name="coordinator",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="interviewer",
        assistant_agent_kwargs=assistant_agent_kwargs,
        task_specify_agent_kwargs=task_specify_agent_kwargs,
        with_task_specify=True
    )