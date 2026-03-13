import requests
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

# Load the .env file
load_dotenv()

# Set up API key and voiceover settings

# Fetch the API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")



VOICE_ID = "pNInz6obpgDQGcFmaJgB" # Example Voice ID (Choose a Southern/Country-style voice)


# Define the script for the radio host
radio_script = [
    "Hey y'all! Welcome to the best two hours of your day right here on Country Vibe Radio! I'm your host, and I gotta say, we have an incredible lineup that’s gonna get your boots tapping and your heart racing. From timeless classics to electrifying anthems, we’re diving headfirst into the soul of rock and roll country! So buckle up, grab a cold drink, and let’s kick this party off with a bang!",
    
    "First up, we're throwing it back to the unforgettable sounds of Creedence Clearwater Revival with 'Fortunate Son.' This track is a blazing anthem filled with rebellion and energy. It’s not just a song; it’s a statement! Did you know it was released in 1969 during the height of the Vietnam War? Its biting lyrics called out privilege and inequality, making it resonate beyond its time. So let’s raise a glass and get ready to sing along!",
    
    "Next on our playlist is none other than the queen herself, Stevie Nicks, bringing us the upbeat and totally captivating 'Edge of Seventeen.' From its iconic guitar riff to Stevie’s hauntingly beautiful vocals, this song is an absolute gem! It was released in 1981 and was inspired in part by the loss of her uncle, but it transforms that sorrow into a celebration of life and spirit! You can’t help but feel uplifted when the chorus hits – let’s soak it all in!",
    
    "Now to wrap things up, we’re cranking up the energy one last time with the legendary Tom Petty and the Heartbreakers and their classic 'Mary Jane's Last Dance.' This track is a high-octane blend of rock and storytelling that captures the essence of letting go and embracing life’s adventures. Did you know that Tom wrote this song as a nod to his struggles and triumphs in the heartland of America? It really encapsulates the highs and lows we all go through, and trust me, it’ll have you dancing by the end!",
    
    "Wow, what a ride! Thank you for joining me today on Country Vibe Radio! I hope you felt the energy and the stories behind these amazing tracks as much as I did. Remember, whether you’re out on the town or just kicking back at home, keep that country spirit alive!  Until next time, keep listening to good music and living your best life!"
]

# ElevenLabs API endpoint
url = "https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"


# API request headers and data
headers = {
    "accept": "audio/mpeg",
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json"
}

for index in range(len(radio_script)):

    data = {
        "text": radio_script[index],
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
        # Load and play the MP3 file
        

    else:
        print("❌ Error:", response.json())
