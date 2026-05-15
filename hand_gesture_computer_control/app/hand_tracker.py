import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def find_hands(self, frame, draw=True):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks and draw:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                )

        return frame, results

    def get_landmarks(self, frame, results):
        landmarks = []

        if not results.multi_hand_landmarks:
            return landmarks

        height, width, _ = frame.shape
        hand = results.multi_hand_landmarks[0]

        for index, landmark in enumerate(hand.landmark):
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            landmarks.append((index, x, y))

        return landmarks