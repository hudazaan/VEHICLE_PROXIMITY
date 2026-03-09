import winsound
import threading

class Alerter:
    def __init__(self):
        self.is_beeping = False

    def _play_beep(self):
        # Frequency 1000Hz, Duration 100ms
        winsound.Beep(1000, 100)
        self.is_beeping = False

    def trigger_collision_warning(self):
        """
        Play system beep in a separate thread so it 
        doesn't freeze the camera feed.
        """
        if not self.is_beeping:
            self.is_beeping = True
            threading.Thread(target=self._play_beep, daemon=True).start()