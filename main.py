import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access your API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

print(ELEVENLABS_API_KEY)  # Should print your API key if everything is set up correctly
