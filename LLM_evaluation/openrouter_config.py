import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key and Base URL
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Configure OpenAI
openai.api_key = OPENROUTER_API_KEY
openai.api_base = OPENROUTER_BASE_URL

# Function to create OpenAI API calls
def get_openai_client():
    if not OPENROUTER_API_KEY:
        raise ValueError("OpenRouter API key is missing. Please check your .env file.")
    return openai
