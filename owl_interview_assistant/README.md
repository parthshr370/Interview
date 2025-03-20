# 🦉 OWL Interview Assistant

An intelligent interview preparation system built with OWL's multi-agent capabilities, designed to help job seekers prepare comprehensively for job interviews.

## Features

- **Company Research Module**: Automated analysis of company culture, news, and industry position
- **Interview Question Generator**: Creates tailored questions for specific job roles and companies
- **Preparation Plan Creator**: Builds personalized study plans and resources
- **Streamlit Frontend**: Simple, intuitive interface for interacting with the system

## Getting Started

### Prerequisites

- Python 3.9+ installed
- API key from OpenAI or OpenRouter

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/owl-interview-assistant.git
   cd owl-interview-assistant
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright dependencies (for web browsing capabilities):
   ```bash
   playwright install-deps
   ```

5. Configure your environment variables:
   ```bash
   cp .env.template .env
   ```
   
   Then edit the `.env` file to add your API keys.

### Running the Application

1. Start the Streamlit web interface:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL displayed in your terminal (typically http://localhost:8501)

## Usage

1. **Company Research**: Select a company to get in-depth information about their culture, operations, and industry position
2. **Interview Questions**: Generate customized questions for your specific job role and target company
3. **Preparation Plan**: Create a comprehensive preparation plan with daily tasks and resources

All generated materials are saved in the `interview_prep` directory for easy access.

## System Requirements

- **Minimum**: 4GB RAM, 2-core CPU
- **Recommended**: 8GB+ RAM, 4-core CPU
- **Storage**: At least 1GB free space

## Advanced Configuration

You can customize the system by modifying:

- `config/prompts.py`: Adjust the system prompts for different functionalities
- `main.py`: Configure different OWL toolkits or change the model parameters

## Troubleshooting

- **Browser Automation Issues**: If you encounter issues with browser automation, try running with `headless=False` in the BrowserToolkit configuration.
- **API Rate Limits**: If you hit rate limits, consider implementing retry logic or using a different API key.

## Credits

This project is powered by:
- [OWL](https://github.com/camel-ai/owl) - Optimized Workforce Learning for General Multi-Agent Assistance
- [CAMEL](https://github.com/camel-ai/camel) - Communicative Agents for "Mind" Exploration
- [Streamlit](https://streamlit.io/) - Frontend framework
