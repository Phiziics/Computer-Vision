import cv2
import time

from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from computer_controller import ComputerController
from config import CAMERA_WIDTH, CAMERA_HEIGHT, PINCH_THRESHOLD, SCREEN_SMOOTHING, CLICK_COOLDOWN


class HandGestureApp:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, CAMERA_WIDTH)
        self.cap.set(4, CAMERA_HEIGHT)

        self.tracker = HandTracker()
        self.detector = GestureDetector(pinch_threshold=PINCH_THRESHOLD)
        self.controller = ComputerController(smoothing=SCREEN_SMOOTHING)

        self.last_click_time = 0

    def run(self):
        while True:
            success, frame = self.cap.read()

            if not success:
                print("Could not read from camera.")
                break

            frame = cv2.flip(frame, 1)

            frame, results = self.tracker.find_hands(frame)
            landmarks = self.tracker.get_landmarks(frame, results)
            gesture = self.detector.detect_gesture(landmarks)

            if landmarks:
                index_tip = landmarks[8]
                hand_x = index_tip[1]
                hand_y = index_tip[2]

                if gesture == "open_palm":
                    self.controller.resume_control()
                    self.controller.move_mouse(hand_x, hand_y, CAMERA_WIDTH, CAMERA_HEIGHT)

                elif gesture == "pinch":
                    current_time = time.time()

                    if current_time - self.last_click_time > CLICK_COOLDOWN:
                        self.controller.left_click()
                        self.last_click_time = current_time

                elif gesture == "peace":
                    current_time = time.time()

                    if current_time - self.last_click_time > CLICK_COOLDOWN:
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
                2,
            )

            cv2.imshow("Hand Gesture Computer Control", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = HandGestureApp()
    app.run()