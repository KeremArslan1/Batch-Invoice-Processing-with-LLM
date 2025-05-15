# This file contains the code to create a client for the Gemini API.
from google import genai
from google.genai import types
import os

api_key = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key='GEMINI_API_KEY')

