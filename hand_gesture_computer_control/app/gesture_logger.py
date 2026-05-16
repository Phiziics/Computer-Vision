import csv
from datetime import datetime
from pathlib import Path


class GestureLogger:
    def __init__(self, log_path="../logs/gesture_log.csv"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.log_path.exists():
            with open(self.log_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "gesture"])

    def log(self, gesture):
        with open(self.log_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().isoformat(), gesture])