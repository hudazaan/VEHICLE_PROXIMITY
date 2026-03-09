import csv
import os
import time

class DataLogger:
    def __init__(self, filename="logs/session_data.csv"):
        self.filename = filename
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Inference_Time_ms", "Collision_Alert"])

    def log_frame(self, latency, alert_status):
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), f"{latency:.2f}", alert_status])