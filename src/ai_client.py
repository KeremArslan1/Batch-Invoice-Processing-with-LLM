# This file contains the code to create a client for the Gemini API.
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()  # Add this line

api_key = os.getenv('GEMINI_API_KEY')

# Optional: Add error handling
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

client = genai.Client(api_key=api_key)