# main.py
import os
import argparse
import typer
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

# Use absolute imports to work within OWL repository
from interview_coach.utils.helpers import ensure_data_directory

app = typer.Typer()
console = Console()

@app.command()
def run(ui: str = "streamlit"):
    """
    Run the Interview Coach application with the specified UI framework.
    
    Args:
        ui (str): UI framework to use ('streamlit' or 'gradio')
    """
    # Load environment variables
    load_dotenv()
    
    # Ensure the data directory structure exists
    ensure_data_directory()
    
    # Check for API keys
    if not os.environ.get("OPENROUTER_API_KEY") and not os.environ.get("OPENAI_API_KEY"):
        console.print(Panel(
            "[bold red]⚠️ API key not found![/]\n\n"
            "Please set up your OpenRouter API key by creating a .env file with:\n"
            "[green]OPENROUTER_API_KEY=your_api_key_here[/]\n\n"
            "You can get a key from: [link=https://openrouter.ai/]https://openrouter.ai/[/]",
            title="API Key Required"
        ))
    
    # Launch the selected UI
    if ui.lower() == "streamlit":
        console.print("[bold blue]Starting Streamlit UI...[/]")
        # Use the correct module path within the OWL repository
        os.system(f"streamlit run {os.path.join(os.path.dirname(__file__), 'web', 'app.py')}")
    else:
        console.print("[bold red]Only Streamlit UI is currently implemented.[/]")

@app.command()
def setup():
    """Set up the Interview Coach application."""
    # Load environment variables
    load_dotenv()
    
    # Ensure the data directory structure exists
    ensure_data_directory()
    
    console.print(Panel(
        "✅ Data directories created\n"
        "✅ Sample questions generated\n\n"
        "Next steps:\n"
        "1. Create a .env file with your OpenRouter API key\n"
        "2. Run the application with 'python -m interview_coach.main run'",
        title="Setup Complete"
    ))

def main():
    """Main entry point for the application using Typer CLI."""
    app()

if __name__ == "__main__":
    main()