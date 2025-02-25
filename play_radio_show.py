from playsound import playsound
from create_radio_show import playlist

# plays audio files in order

# intro
playsound("radio_host0.mp3")

# songs
for index in playlist:
    filename = "radio_host" + str(index + 1) + ".mp3"
    playsound(filename)
    playsound(playlist[index][2])

# outro
filename = "radio_host" + str(len(playlist)) + ".mp3"
playsound(filename)
