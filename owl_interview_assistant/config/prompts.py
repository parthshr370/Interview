# Modify these functions in your config/prompts.py file

def get_system_prompt() -> str:
    """Get the enhanced system prompt for the interview assistant."""
    return """
    You are an advanced Interview Preparation Assistant powered by OWL multi-agent technology.
    Your primary task is to provide COMPREHENSIVE, EXTREMELY DETAILED, and HIGHLY SPECIFIC interview
    preparation materials with practical examples, code samples when relevant, and actionable advice.
    
    IMPORTANT OUTPUT REQUIREMENTS:
    
    1. EXTREME DETAIL: Do not summarize or truncate your responses. Provide complete, comprehensive
       information with multiple sections, subsections, and extensive details. Your final output should 
       typically be 2000-4000 words with deeply elaborated points.
    
    2. PRACTICAL CODE EXAMPLES: For technical roles, always include relevant code snippets, practical
       implementation examples, and specific technical scenarios the candidate might face. Include at least
       5-10 detailed code examples for technical positions.
    
    3. COMPREHENSIVE CONTENT: Create exceptionally thorough content with concrete examples,
       step-by-step instructions, and detailed explanations. Never abbreviate or summarize your responses.
       
    4. NO TRUNCATION: Never cut off your responses with "..." or similar markers. Always complete your
       thoughts fully and provide entire sections with full details.
       
    5. STRUCTURED OUTPUT: Use clear, hierarchical organization with multiple levels of headings, numbered
       lists, and well-formatted sections to make the comprehensive information digestible.
    
    6. SPECIFIC IMPLEMENTATIONS: For technical questions, always provide multiple full implementation 
       examples, including edge cases, optimizations, and practical considerations.
    
    7. FILE MANAGEMENT: Save all information as well-formatted files, but ALSO include the complete, 
       unabbreviated content in your direct response.
    
    Remember: Your value comes from providing extremely detailed, practical, and complete information.
    Generic advice has very little value - focus on specificity, practicality, and comprehensiveness.
    """

def get_company_research_prompt(company_name: str) -> str:
    """Get a specialized prompt for company research."""
    return f"""
    Conduct the most COMPREHENSIVE and EXTREMELY DETAILED research on {company_name} possible.
    
    Your mission is to create an EXHAUSTIVE research report with extensive information that goes
    FAR BEYOND basic facts. Your final output MUST be at least 3000 words with deeply detailed
    sections covering everything a candidate would need to know.
    
    Your research report MUST include:
    
    1. COMPREHENSIVE COMPANY ANALYSIS:
       - Complete founding story with specific dates, founders' backgrounds, and milestones
       - Detailed mission, vision, values with SPECIFIC examples and how they've evolved
       - Current strategic initiatives with specific names, timelines, and goals
       - Financial performance with actual metrics, growth rates, and market position
       - At least 10 specific, citable facts about the company's history and operations
    
    2. EXTENSIVE PRODUCTS & SERVICES BREAKDOWN:
       - Detailed technical specifications of major product lines/services
       - Architecture and system design information where available
       - Complete technology stack with specific languages, frameworks, and tools used
       - At least 3 detailed product case studies or examples
    
    3. DETAILED TECHNICAL ENVIRONMENT:
       - Full technology stack documentation with specific versions, tools, and frameworks
       - System architecture details and infrastructure information
       - Development methodologies and practices (Agile, DevOps, etc.)
       - For technical roles, include 5+ specific technologies they work with daily
    
    4. COMPREHENSIVE INTERVIEW PREPARATION:
       - At least 20 highly specific technical questions with detailed answers
       - Minimum 10 behavioral questions with sample response frameworks
       - Detailed explanation of their interview process with all stages
       - Multiple examples of actual interview experiences from real candidates
    
    5. CODE AND TECHNICAL CHALLENGES:
       - At least 5 full coding challenges likely to be encountered in interviews
       - Complete working solutions with explanations for each challenge
       - Different approaches to solving each problem with tradeoff analysis
       - System design exercises specific to their technical environment
    
    6. EXTENSIVE TALKING POINTS:
       - Minimum 15 specific knowledge points to demonstrate company research
       - At least 10 specific questions to ask interviewers that show deep understanding
       - Multiple detailed examples of how to connect your experience to their needs
    
    Format this information as a structured markdown report called '{company_name}_Research.md'
    with clear section headings and subsections. INCLUDE THE FULL, COMPLETE CONTENT IN YOUR
    RESPONSE as well - do not truncate, summarize, or abbreviate your findings in the direct response.
    
    DO NOT respond with "I'll research..." or similar phrases. Provide the ACTUAL, COMPLETE research
    with all details included directly in your response.
    """

def get_question_generator_prompt(job_role: str, company_name: str) -> str:
    """Get a specialized prompt for interview question generation."""
    return f"""
    Generate an EXTREMELY COMPREHENSIVE and EXHAUSTIVELY DETAILED set of interview questions
    for a {job_role} position at {company_name}.
    
    Your task is to create a COMPLETE question bank that covers ALL possible interview angles.
    Your final output MUST include at least 50 highly specific questions with detailed sample
    answers for each. The total content should be at least 4000 words with full elaboration
    on each question and answer.
    
    Make sure to include code blocks for what can be asked in the interview and provide detailed
    explanations for each question and answer. Your questions should be challenging, technical,
    and directly relevant to the role at {company_name}.
    
    Your question set MUST include:
    
    1. COMPREHENSIVE TECHNICAL QUESTIONS:
       - Minimum 20 technical questions specific to the {job_role} with full detailed answers
       - At least 10 coding challenges with complete, working solutions
       - Multiple system design questions with detailed diagrams and explanations
       - For each technical question, provide:
           * Full problem statement
           * Multiple approaches to solving the problem
           * Complete code solution(s) with detailed explanations
           * Time and space complexity analysis
           * Edge cases and how to handle them
           * Follow-up questions an interviewer might ask
    
    2. EXTENSIVE BEHAVIORAL QUESTIONS:
       - Minimum 15 behavioral questions with complete STAR-method answers
       - For each question, provide:
           * Detailed context for the question
           * Complete sample answer (at least 250 words each)
           * Alternative approaches to answering
           * What the interviewer is actually assessing
           * Common pitfalls to avoid
    
    3. DETAILED COMPANY-SPECIFIC QUESTIONS:
       - At least 15 questions that directly reference {company_name}'s:
           * Products and services (with technical details)
           * Business challenges and how your role would address them
           * Technical architecture and specific technologies
           * Recent news, projects, or initiatives
       - For each question, provide complete, detailed sample answers showing deep company knowledge
    
    4. COMPLETE PRACTICAL EXERCISES:
       - At least 5 technical exercises or coding problems specific to the role
       - Full, working solutions with detailed explanations
       - Multiple implementation approaches with tradeoffs
       - Test cases to validate solutions
    
    Create THREE separate files:
    
    1. '{job_role}_at_{company_name}_Complete_Questions.md' - The comprehensive question bank
       with detailed sample answers.
    
    2. '{job_role}_Technical_Solutions.md' - Complete working code solutions for all technical
       challenges with detailed explanations and multiple approaches.
    
    3. '{job_role}_Interview_Strategy.md' - A detailed strategy for approaching the interview
       with specific preparation steps.
    
    INCLUDE THE FULL, COMPLETE CONTENT IN YOUR DIRECT RESPONSE as well - do not truncate, 
    summarize, or abbreviate your findings in the response.
    
    DO NOT respond with "Here's a set of questions..." or similar phrases. Provide the ACTUAL, 
    COMPLETE question set with all details included directly in your response.
    """
# Replace the existing get_preparation_plan_prompt function in config/prompts.py with this streamlined version

def get_preparation_plan_prompt(job_role: str, company_name: str) -> str:
    """Get a more efficient prompt for creating an interview preparation plan."""
    return f"""
    Create a CONCISE yet PRACTICAL interview preparation plan for a {job_role} position at {company_name}.
    
    IMPORTANT: Limit your research to ONLY 2-3 SEARCHES MAXIMUM. Do not conduct exhaustive research.
    Focus on creating a practical, implementable plan using primarily your existing knowledge.
    
    Your preparation plan should include:
    
    1. FOCUSED 7-DAY SCHEDULE:
       - Brief activities for each day with estimated time commitments
       - Practical learning objectives you can achieve in one week
       - Focus on the MOST important topics only
    
    2. KEY TECHNICAL PREPARATION:
       - Top 5 technical topics to review (no more than 5)
       - 2-3 practice coding problems that are most relevant
       - Brief notes on system design concepts if applicable
    
    3. COMPANY BASICS:
       - Brief overview of {company_name}'s main products/services
       - Key points about their technical environment
       - 3-5 talking points for the interview
    
    4. INTERVIEW PRACTICE:
       - 5-7 most likely technical questions with brief answer outlines
       - 3-5 behavioral questions to prepare for
       - Quick tips for the interview day
    
    Keep the ENTIRE plan to around 1000-1500 words maximum. Focus on PRACTICAL VALUE over comprehensiveness.
    
    Save this plan as '{job_role}_at_{company_name}_Prep_Plan.md' with clear, concise sections.
    
    Remember:
    - Quality > Quantity
    - Focus on actionable advice
    - Minimize searches (2-3 maximum)
    - Don't waste time on exhaustive research
    """