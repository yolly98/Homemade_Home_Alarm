import threading
from pydub import AudioSegment
from pydub.playback import play
import threading

class AlarmManager:

    instance = None

    def __init__(self):
        self.armed = False
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
        return (self.armed, self.status)

    def alarm_player(self):
        while True:
            with self.lock:
                if not self.armed:
                    continue
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

    def armAlarm(self):
        with self.lock:
            self.status = False
            self.armed = True
            self.detections = dict()
    
    def disarmAlarm(self):
        with self.lock:
            self.status = False
            self.armed = False
            self.detections = dict()

    def update_detections(self, node_id, detection):
        with self.lock:
            if not self.armed:
                return
            if detection:
                self.detections[node_id] = None
            else:
                self.detections.pop(node_id, None)

