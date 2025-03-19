"""OWL utilities for running multi-agent societies."""

from typing import Dict, List, Tuple, Any
from camel.societies import RolePlaying

def run_society(society: RolePlaying, prompt: str = None) -> Tuple[str, List[Dict[str, str]], Dict[str, int]]:
    """
    Run a multi-agent society conversation with the provided prompt.
    
    Args:
        society (RolePlaying): The society to run
        prompt (str, optional): Initial prompt to start the conversation
        
    Returns:
        Tuple[str, List[Dict[str, str]], Dict[str, int]]: 
            - Final answer
            - Chat history
            - Token count information
    """
    # Initialize the chat with the prompt
    if prompt:
        init_msg = society.init_chat(prompt)
    else:
        init_msg = society.init_chat()
    
    # Maximum number of conversation rounds
    max_rounds = 15
    chat_history = []
    overall_token_count = {"prompt_tokens": 0, "completion_tokens": 0}
    
    # Run the conversation for multiple rounds
    for round_idx in range(max_rounds):
        # Get responses from both agents
        assistant_response, user_response = society.step(init_msg)
        
        # Update token count if available
        if hasattr(assistant_response, "info") and assistant_response.info.get("usage"):
            overall_token_count["prompt_tokens"] += assistant_response.info["usage"].get("prompt_tokens", 0)
            overall_token_count["completion_tokens"] += assistant_response.info["usage"].get("completion_tokens", 0)
        
        if hasattr(user_response, "info") and user_response.info.get("usage"):
            overall_token_count["prompt_tokens"] += user_response.info["usage"].get("prompt_tokens", 0)
            overall_token_count["completion_tokens"] += user_response.info["usage"].get("completion_tokens", 0)
        
        # Add to chat history
        chat_history.append({
            "user": user_response.msg.content if hasattr(user_response, "msg") and user_response.msg else "",
            "assistant": assistant_response.msg.content if hasattr(assistant_response, "msg") and assistant_response.msg else "",
        })
        
        # Check if conversation is terminated
        if assistant_response.terminated or user_response.terminated:
            break
        
        # Set up next round
        init_msg = assistant_response.msg
    
    # Get the final answer (last assistant message)
    final_answer = ""
    for entry in reversed(chat_history):
        if entry.get("assistant"):
            final_answer = entry["assistant"]
            break
    
    return final_answer, chat_history, overall_token_count