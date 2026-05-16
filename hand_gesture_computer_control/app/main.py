import cv2
import time

from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from computer_controller import ComputerController
from gesture_logger import GestureLogger
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
        self.last_logged_gesture = None

        self.last_click_time = 0
        self.click_cooldown = 1.0

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

            if landmarks:
                index_tip = landmarks[8]
                hand_x = index_tip[1]
                hand_y = index_tip[2]

                if gesture == "open_palm":
                    self.controller.resume_control()
                    self.controller.move_mouse(
                        hand_x,
                        hand_y,
                        CAMERA_WIDTH,
                        CAMERA_HEIGHT
                    )

                elif gesture == "pinch":
                    current_time = time.time()

                    if current_time - self.last_click_time > self.click_cooldown:
                        self.controller.left_click()
                        self.last_click_time = current_time

                elif gesture == "peace":
                    current_time = time.time()

                    if current_time - self.last_click_time > self.click_cooldown:
                        self.controller.right_click()
                        self.last_click_time = current_time

                elif gesture == "fist":
                    self.controller.pause_control()

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
                "q: quit | p: pause | r: resume",
                (30, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            cv2.imshow("Hand Gesture Computer Control", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if key == ord("p"):
                self.controller.pause_control()
                print("Control paused.")

            if key == ord("r"):
                self.controller.resume_control()
                print("Control resumed.")

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = HandGestureApp()
    app.run()