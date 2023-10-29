import threading
from pydub import AudioSegment
from pydub.playback import play
import threading

class AlarmManager:

    instance = None

    def __init__(self):
        self.status = False
        self.detections = dict()
        self.lock = threading.Lock()
        self.alarm_sound = AudioSegment.from_file("alarm.mp3")

    @staticmethod
    def get_instance():
        if AlarmManager.instance is None:
            AlarmManager.instance = AlarmManager()
        return AlarmManager.instance
    
    def get_status(self):
        return self.status

    def alarm_player(self):
        while True:
            if len(self.detections) > 0:
                self.status = True
                print()
                print("SENSOR NODE ALERTED")
                for node_id in self.detections:
                    print(node_id)
                print()
                play(self.alarm_sound)
            else:
                self.status = False

    def reset(self):
        with self.lock:
            self.detections = dict()

    def update_detections(self, node_id, detection):
        with self.lock:
            if detection:
                self.detections[node_id] = None
            else:
                self.detections.pop(node_id, None)

