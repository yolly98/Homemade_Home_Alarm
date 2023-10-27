
from pydub import AudioSegment
from pydub.playback import play
import threading

alarm = AudioSegment.from_file("alarm.mp3")

while True:
    play(alarm)
