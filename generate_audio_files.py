import requests
import os
from dotenv import load_dotenv
from playsound import playsound

# Load the .env file
load_dotenv()

# Set up API key and voiceover settings

# Fetch the API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")



VOICE_ID = "pNInz6obpgDQGcFmaJgB" # Example Voice ID (Choose a Southern/Country-style voice)

# function that creates the audio files: one for the intro, one for each song, one for the outro

def create_script_audio(script):
    # ElevenLabs API endpoint
    url = "https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    audio_files = []


    # API request headers and data
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    for index in range(len(script)):

        data = {
            "text": script[index],
            "model_id": "eleven_multilingual_v1",
            "voice_settings": {
                "stability": 0.5,  # Adjust for more expressive speech
                "similarity_boost": 0.8
            }
        }

        # Make the request

        response = requests.post(url.format(VOICE_ID=VOICE_ID), headers=headers, json=data)

        # Save the audio file
        file_name = "radio_host" + str(index) + ".mp3"

        if response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(response.content)
            print("🎙️ Radio host voiceover saved as 'radio_host.mp3'")
            audio_files.append(file_name)
            

        else:
            print("❌ Error:", response.json())

    return audio_files


import ast
from get_radio_script import radio_script

# Convert string to list
radio_script = ast.literal_eval(radio_script)

audio_file_names = create_script_audio(radio_script)



