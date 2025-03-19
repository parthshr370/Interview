# Interview Coach using OWL Framework

An intelligent interviewing system built on the OWL (Optimized Workforce Learning) framework that simulates job interviews and provides real-time feedback.

## Overview

The Interview Coach is a web-based application that simulates job interviews across various industries using OWL's multi-agent architecture to provide real-time feedback from different perspectives.

## Features

- Support for various industries and job roles
- Real-time feedback on interview responses
- Comprehensive final reports
- Web interface with Streamlit
- Customizable question sets

## Installation

### Prerequisites

- Python 3.8+
- OpenRouter API key (for access to Gemini model)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/interview-coach.git
cd interview-coach
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.template .env
```

Edit the `.env` file and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Running the Application

Run the application using:

```bash
# Set up data directories and sample questions
python main.py setup

# Start the application with Streamlit UI
python main.py run
```

Alternatively, you can run the Streamlit app directly:

```bash
streamlit run web/app.py
```

## Usage

1. Select the industry and job role in the sidebar
2. Set the number of questions for the interview
3. Click "Start New Interview" to begin
4. Answer each question in the text area and submit
5. Review feedback for each answer
6. At the end of the interview, download the comprehensive feedback report

## Customizing Questions

You can add your own questions by creating or modifying files in the `data/questions/` directory. Each file should be named after the job role (e.g., `software_engineer.txt`) and contain one question per line.

## Using with Gemini via OpenRouter

This project uses the Gemini model via OpenRouter for the interview simulation. To use this:

1. Create an account on [OpenRouter](https://openrouter.ai/)
2. Generate an API key
3. Add the API key to your `.env` file

The code is preconfigured to use Gemini Pro through OpenRouter. You can modify the model selection in `interview/agent_manager.py` if needed.

## Project Structure

```
interview_coach/
├── config/               # Configuration for the system
│   ├── __init__.py
│   └── prompts.py        # System prompts for agents
├── data/
│   └── questions/        # Question files by job role
│       ├── software_engineer.txt
│       ├── data_scientist.txt
│       └── product_manager.txt
├── interview/            # Core interview functionality
│   ├── __init__.py
│   ├── coach.py          # Main interview coach class
│   ├── agent_manager.py  # OWL agent setup
│   └── feedback.py       # Feedback formatting
├── utils/                # Utility functions
│   ├── __init__.py
│   └── helpers.py
├── web/                  # Web interface
│   ├── __init__.py
│   ├── app.py            # Streamlit application
│   └── components.py     # UI components
├── output/               # Directory for saved reports
├── main.py               # Main entry point
├── .env.template         # Template for environment variables
└── requirements.txt      # Dependencies
```

## How It Works

The Interview Coach uses OWL's multi-agent architecture to create a simulated interview environment:

1. The **Coordinator Agent** manages the overall interview process
2. The **Interviewer Agent** asks questions and evaluates responses
3. The system processes the user's responses using the OWL framework
4. Detailed feedback is generated for each response
5. A comprehensive report is created at the end of the interview

## License

MIT License