import cv2
import time

from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from computer_controller import ComputerController
from gesture_logger import GestureLogger
from action_mapper import ActionMapper
from config import CAMERA_WIDTH, CAMERA_HEIGHT, PINCH_THRESHOLD, SCREEN_SMOOTHING


class HandGestureApp:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, CAMERA_WIDTH)
        self.cap.set(4, CAMERA_HEIGHT)

        self.tracker = HandTracker()
        self.detector = GestureDetector(pinch_threshold=PINCH_THRESHOLD)
        self.controller = ComputerController(smoothing=SCREEN_SMOOTHING)
        self.logger = GestureLogger()
        self.action_mapper = ActionMapper()

        self.last_logged_gesture = None
        self.last_action_time = 0
        self.action_cooldown = 3.0

    def can_run_action(self):
        current_time = time.time()
        return current_time - self.last_action_time > self.action_cooldown

    def run_gesture_action(self, gesture):
        action_gestures = [
            "one_finger",
            "two_fingers",
            "three_fingers",
            "four_fingers",
            "open_hand",
            "fist"
        ]

        if gesture in action_gestures and self.can_run_action():
            self.action_mapper.run_action(gesture)
            self.last_action_time = time.time()

    def run(self):
        while True:
            success, frame = self.cap.read()

            if not success:
                print("Could not read from webcam.")
                break

            frame = cv2.flip(frame, 1)

            frame, results = self.tracker.find_hands(frame)
            landmarks = self.tracker.get_landmarks(frame, results)
            gesture = self.detector.detect_gesture(landmarks)

            if gesture != self.last_logged_gesture:
                self.logger.log(gesture)
                self.last_logged_gesture = gesture

            self.run_gesture_action(gesture)

            cv2.putText(
                frame,
                f"Gesture: {gesture}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "1: VS Code | 2: Browser | 3: Terminal | 4: LinkedIn",
                (30, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "Open hand: Calculator | Fist: Close active window | q: Quit",
                (30, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.imshow("GestureOS Command Center", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = HandGestureApp()
    app.run()