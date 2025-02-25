import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access your API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# set up OpenAI API key

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
  api_key = OPENAI_API_KEY
)


def call_llm(prompt):

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": prompt}
    ]
    )

    print(completion.choices[0].message.content);
    return completion.choices[0].message.content

#----------------------------------------------------------

import librosa
import librosa.display
import numpy as np
from mutagen.mp3 import MP3

def analyze_audio(mp3_file):
    """
    Extracts key audio features from an MP3 file.
    """
    # Load audio file
    y, sr = librosa.load(mp3_file, sr=None)  # Preserve original sample rate
    
    # Extract features
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)  # Tempo (BPM)
     # Ensure tempo is a scalar
    tempo = float(tempo) if isinstance(tempo, np.ndarray) else tempo
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))  # Brightness
    rms_energy = np.mean(librosa.feature.rms(y=y))  # Energy level
    duration = MP3(mp3_file).info.length  # Duration in seconds

    # Classify vibe based on tempo and energy
    if tempo > 120 and rms_energy > 0.05:
        mood = "High-energy, party, or dance track"
    elif tempo > 90:
        mood = "Upbeat and fun"
    elif tempo > 60:
        mood = "Laid-back, storytelling"
    else:
        mood = "Slow, emotional ballad"

    return {
        "tempo": round(tempo),
        "spectral_brightness": round(spectral_centroid),
        "energy": round(float(rms_energy), 3),
        "duration": round(duration, 2),
        "mood": mood
    }

# Example usage
mp3_file = "Fortunate_Son.mp3"  
features = analyze_audio(mp3_file)
print(features)



def generate_radio_script(playlist):
    """
    Generates a radio show script for a given playlist of songs.
    
    :param playlist: A list of songs, where each song is a list in the format [title, artist, mp3file].
    :return: A formatted radio show script.
    """
    
    # Construct the list of song details
    song_details = []
    for song in playlist:
        title, artist, mp3file = song
        song_features = analyze_audio(mp3file)  # Extract vibe from the MP3 file
        mood = song_features["mood"]
        tempo = song_features["tempo"]
        
        song_details.append(f"- '{title}' by {artist}, a **{mood}** song with a tempo of {tempo} BPM.")
    
    # Format the list of songs into a readable string
    song_list_str = "\n".join(song_details)
    
    # GPT-4o Prompt
    prompt = f"""
    You are a charismatic and engaging country radio host. You are hosting a **full radio show** where you introduce 
    a playlist of songs. Your goal is to create an **energetic and natural** radio script that includes:
    
    1️⃣ **A lively, fun introduction** that welcomes listeners and sets the mood for the show.  
    2️⃣ **Individual song introductions** that match the song's vibe.  
    3️⃣ **A smooth outro** that thanks the listeners and wraps up the show.

    🎶 Here’s the playlist you’ll introduce today:
    {song_list_str}

    **Tone Guidelines:**
    - If the song is **high-energy (tempo > 120 BPM)**, sound excited and hyped up!
    - If the song is **laid-back (tempo 60-90 BPM)**, be smooth and chill.
    - If the song is **emotional and slow**, speak with warmth and nostalgia.
    - Use  **natural DJ-style banter** to make it engaging.
    - Idenfity the genre of the playlist and use a tone of voice to match the vibe.
    - Include SPECIFIC and NICHE fun facts about the song and lyrics
    - you do not need to say the bpm for each song. Make your response variable and fluid like a real radio host.

    

    Now, generate a **full** radio script that follows this format! Remember, ONLY alphanumerics and punctuation in the response. NO EMOJIS. Return a list where each element is a string of the intro, description of each song, and outro."""
    
    return prompt


#-----------------------------------------------------------------------------


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



#---------------------------------------------------------------------------------------

# playlist is a 2D Array of songs where the inner list has format matching: ["title", "artist", "filename.mp3"]
playlist = [["Fortunate Son", "Creedence Clearwater Revival", "Fortunate_Son.mp3"],["Edgeof Seventeen", "Stevie Nicks", "Edge_of_Seventeen.mp3"], ["Mary Jane's Last Dance", "Tom Petty and the Heartbreakers", "Mary_Janes_Last_Dance.mp3"]]

# prompt for the radio host script based on analysis of song features
prompt = generate_radio_script(playlist)

# generates radio host script
response = call_llm(prompt)

# generates radio host audio
audio_files = create_script_audio(response)


