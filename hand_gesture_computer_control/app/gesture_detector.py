import math


class GestureDetector:
    def __init__(self, pinch_threshold=35):
        self.pinch_threshold = pinch_threshold

    def calculate_distance(self, point1, point2):
        return math.hypot(point2[1] - point1[1], point2[2] - point1[2])

    def fingers_up(self, landmarks):
        if not landmarks:
            return []

        fingers = []

        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]

        if thumb_tip[1] > thumb_ip[1]:
            fingers.append(1)
        else:
            fingers.append(0)

        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]

        for tip, pip in zip(finger_tips, finger_pips):
            if landmarks[tip][2] < landmarks[pip][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def detect_gesture(self, landmarks):
        if not landmarks:
            return "no_hand"

        fingers = self.fingers_up(landmarks)

        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        pinch_distance = self.calculate_distance(thumb_tip, index_tip)

        if pinch_distance < self.pinch_threshold:
            return "pinch"

        if fingers == [0, 1, 0, 0, 0]:
            return "one_finger"

        if fingers == [0, 1, 1, 0, 0]:
            return "two_fingers"

        if fingers == [0, 1, 1, 1, 0]:
            return "three_fingers"

        if fingers == [0, 1, 1, 1, 1]:
            return "four_fingers"

        if fingers == [1, 1, 1, 1, 1]:
            return "open_hand"

        if fingers == [0, 0, 0, 0, 0]:
            return "fist"

        return "unknown"