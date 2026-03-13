## OPENAI SETUP ##
###############################################################################################################################################
# Set up OpenAI API key 

import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
  api_key = OPENAI_API_KEY
)


# INPUT: string of prompt
# OUTPUT: clean string of LLM response
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

## AUDIO ANALYSIS ##
#############################################################################################################################################

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


## Create LLM prompt ##
####################################################################################################################################


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


## Get LLM Generated Radio Script ##
##############################################################################################################################################3

from user_input import playlist

radio_script = call_llm(generate_radio_script(playlist))
