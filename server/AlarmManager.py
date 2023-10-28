import threading
from pydub import AudioSegment
from pydub.playback import play
import threading

class AlarmManager:

    instance = None

    def __init__(self):
        self.detections = 0
        self.lock = threading.Lock()
        self.alarm_sound = AudioSegment.from_file("alarm.mp3")

    @staticmethod
    def get_instance():
        if AlarmManager.instance is None:
            AlarmManager.instance = AlarmManager()
        return AlarmManager.instance
    
    def alarm_player(self):
        while True:
            if self.detections > 0:
                print(f'start alarm [{self.detections}]')
                play(self.alarm_sound)

    def reset(self):
        with self.lock:
            self.detections

    def update_detections(self, detection):
        with self.lock:
            if detection:
                self.detections += 1
            else:
                self.detections -= 1

