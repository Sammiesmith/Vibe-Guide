import pygame
import time
from user_input import playlist

# plays audio files in order

# Initialize pygame mixer
pygame.mixer.init()

# intro------------------------------------------
print(f"Now playing: radio_host0.mp3")
pygame.mixer.music.load("radio_host0.mp3")
pygame.mixer.music.play()

# Wait until the song finishes playing
while pygame.mixer.music.get_busy():
    time.sleep(1)  # Prevents high CPU usage

# songs ---------------------------------------------

for i in range(len(playlist)):
    filename = "radio_host" + str(i + 1) + ".mp3"
    print(f"Now playing: {filename}")
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait until the song finishes playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)  # Prevents high CPU usage

print("All songs finished playing!")

# outro -----------------------------------------------
filename = "radio_host" + str(len(playlist)) + ".mp3"
print(f"Now playing: {filename}")
pygame.mixer.music.load(filename)
pygame.mixer.music.play()

# Wait until the song finishes playing
while pygame.mixer.music.get_busy():
    time.sleep(1)  # Prevents high CPU usage







