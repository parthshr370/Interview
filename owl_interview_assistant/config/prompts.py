def get_system_prompt() -> str:
    """Get the enhanced system prompt for the interview assistant."""
    return """
    You are an advanced Interview Preparation Assistant powered by OWL multi-agent technology.
    You are designed to provide COMPREHENSIVE, DETAILED, and HIGHLY SPECIFIC interview preparation
    materials that go far beyond generic advice.
    
    Your capabilities and responsibilities include:
    
    1. IN-DEPTH RESEARCH: Thoroughly research companies, industries, job roles, and interview processes
       using search tools and web browsing. Always go beyond surface-level information.
    
    2. COMPREHENSIVE CONTENT CREATION: Generate detailed, well-structured, and actionable content
       that provides genuine value to the job seeker. Your outputs should typically be 1000-2000 words
       and extremely thorough.
    
    3. SPECIFIC RECOMMENDATIONS: Provide highly specific, tailored advice based on the exact company
       and role, not generic interview tips. Include specific examples, talking points, and strategies.
    
    4. PRACTICAL PREPARATION MATERIALS: Create concrete preparation tools like structured question lists,
       day-by-day preparation plans, cheat sheets, and practice scenarios.
    
    5. FILE MANAGEMENT: Save all important information as well-formatted files in the designated directory.
       Always use Markdown formatting with clear headings, bullet points, and structure.
    
    Always be thorough, specific, and practical. Avoid generic advice at all costs.
    When researching, dig deep for valuable insights that would truly help someone stand out in an interview.
    When creating content, focus on quality, specificity, and actionable insights.
    """

def get_company_research_prompt(company_name: str) -> str:
    """Get a specialized prompt for company research."""
    return f"""
    Conduct EXHAUSTIVE research on {company_name} and create a COMPREHENSIVE research report.
    
    Your mission is to gather and synthesize detailed information that goes FAR BEYOND basic
    facts available on the company website. Look for insider perspectives, industry analysis,
    employee reviews, and detailed information about their interview process.
    
    Your research report MUST include:
    
    1. COMPANY OVERVIEW:
       - Founding story and historical development
       - Mission, vision, values with SPECIFIC examples of how they manifest
       - Current strategic initiatives and business direction
       - Financial performance and market position (with specific metrics when available)
    
    2. PRODUCTS & SERVICES:
       - Detailed breakdown of major product lines/services
       - Recent product launches or updates (last 1-2 years)
       - Technology stack and methodologies used
       - Competitive positioning of key offerings
    
    3. LEADERSHIP & CULTURE:
       - Key executives with background and leadership styles
       - Organizational structure and reporting relationships
       - Company culture specifics (work-life balance, collaboration style, etc.)
       - Employee reviews and satisfaction insights from Glassdoor, Blind, etc.
    
    4. INDUSTRY ANALYSIS:
       - Detailed competitive landscape with major rivals
       - Industry trends affecting the company
       - Challenges and opportunities facing the organization
       - Market share and positioning data
    
    5. INTERVIEW PROCESS INSIGHTS:
       - Typical interview stages and formats
       - Common questions asked by specific teams
       - Interviewer preferences and red flags
       - Success stories from candidates who received offers
    
    6. TALKING POINTS FOR CANDIDATES:
       - Specific company challenges that interviewees can address
       - Recent news that could be mentioned to demonstrate research
       - Strategic initiatives that align with the candidate's skills
       - Thoughtful questions to ask interviewers
    
    Save this information as a structured markdown report called '{company_name}_Research.md'
    with clear section headings, bullet points, and formatting.
    
    Research THOROUGHLY using all available search tools and methods. Dig deep beyond
    superficial information and find valuable insights that would truly help a candidate
    impress interviewers with their company knowledge.
    """

def get_question_generator_prompt(job_role: str, company_name: str) -> str:
    """Get a specialized prompt for interview question generation."""
    return f"""
    Generate an EXTENSIVE and DETAILED set of interview questions for a {job_role} position at {company_name}.
    
    Your task is to create a comprehensive question bank that covers ALL possible angles of the interview,
    with special emphasis on company-specific and role-specific questions. Do not provide generic questions
    that could apply to any company - make them highly specific to {company_name} and the {job_role} role.
    
    Your question set MUST include:
    
    1. TECHNICAL QUESTIONS:
       - Core technical skills required for the {job_role} position
       - Specific technologies, tools, and methodologies used at {company_name}
       - Problem-solving scenarios relevant to their business domain
       - System design or architecture questions specific to their scale/challenges
       - Technical challenges specific to their industry
    
    2. BEHAVIORAL QUESTIONS:
       - Tailored to {company_name}'s known cultural values
       - Specific situations that evaluate fit for this particular team
       - Scenarios that test for their key soft skills priorities
       - Questions that reveal alignment with their working style
    
    3. COMPANY-SPECIFIC QUESTIONS:
       - Questions that directly reference {company_name}'s products/services
       - Scenarios involving their specific customer base or market
       - Questions relating to their current business challenges
       - Cultural fit questions based on their known work environment
    
    4. ROLE-SPECIFIC SCENARIOS:
       - Detailed day-in-the-life scenarios for this exact role
       - Problem-solving exercises mimicking actual work
       - Case studies based on real challenges they've faced
       - Project retrospective questions relevant to their work
    
    5. SAMPLE ANSWERS:
       - Detailed, concrete example answers (200+ words each)
       - Specific examples, metrics, and outcomes to mention
       - Tailored structure for answering each question type
       - Common pitfalls to avoid when answering
    
    Create TWO separate files:
    
    1. '{job_role}_at_{company_name}_Questions.md' - A comprehensive question bank with detailed
       sample answers, organized by category.
    
    2. '{job_role}_Quick_Reference.md' - A condensed list of just the questions for quick practice,
       organized by priority/importance.
    
    If the role is technical, also create:
    
    3. '{job_role}_Technical_Challenges.md' - A set of 5-10 technical challenges or coding problems
       likely to be asked, with detailed solutions.
    
    Research THOROUGHLY to find ACTUAL questions asked in {company_name} interviews for similar roles.
    Use search tools and job sites to gather real interview experiences and questions.
    """

def get_preparation_plan_prompt(job_role: str, company_name: str) -> str:
    """Get a specialized prompt for creating an interview preparation plan."""
    return f"""
    Create a COMPREHENSIVE and HIGHLY STRUCTURED interview preparation plan for a {job_role} position at {company_name}.
    
    Your task is to develop a detailed, day-by-day preparation strategy that covers ALL aspects of
    interview preparation, from initial research to post-interview follow-up. The plan should be
    highly specific to {company_name} and the {job_role} position, not generic advice.
    
    Your preparation plan MUST include:
    
    1. COMPREHENSIVE DAILY SCHEDULE:
       - A detailed 14-day preparation timeline
       - Specific activities for each day with time allocations
       - Clear goals and outcomes for each preparation session
       - Incremental progression to build confidence and knowledge
    
    2. TECHNICAL PREPARATION:
       - Specific technical topics to review based on {company_name}'s stack
       - Practice exercises and problems similar to their actual assessments
       - Resources for strengthening relevant technical skills
       - System design preparation relevant to their architecture
    
    3. COMPANY RESEARCH GUIDE:
       - Detailed breakdown of what to research about {company_name}
       - Key information to memorize about their products/services
       - Recent news and developments to be familiar with
       - Competitive landscape knowledge to demonstrate
    
    4. PRACTICAL EXERCISES:
       - Mock interview scripts tailored to {company_name}'s format
       - Role-playing scenarios for behavioral questions
       - Technical walkthroughs for coding or design challenges
       - Presentation preparation if applicable
    
    5. DETAILED CHECKLISTS:
       - Day-before preparation checklist
       - Interview day logistics and timing
       - Materials to bring and review
       - Post-interview follow-up strategy
    
    Create THREE separate files:
    
    1. 'Interview_Preparation_Plan.md' - The comprehensive day-by-day plan
       with detailed activities and resources.
    
    2. 'Interview_Cheat_Sheet.md' - A concise one-page reference with key
       talking points, questions to ask, and crucial information.
    
    3. 'Interview_Day_Checklist.md' - A detailed checklist for final preparation
       and the interview day itself.
    
    Research THOROUGHLY to understand {company_name}'s actual interview process for {job_role} positions.
    Use search tools to find real experiences and tailor the plan accordingly. Make the plan realistic,
    practical, and highly specific to this particular company and role.
    """