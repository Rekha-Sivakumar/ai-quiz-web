import os
import google.generativeai as genai

# Get API key from Render Environment Variable
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Create client/model
client = genai.GenerativeModel("gemini-pro")
