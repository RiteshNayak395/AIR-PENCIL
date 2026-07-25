#working of this file is to track the hand and return the landmarks and hand type (left or right) using mediapipe library

import cv2
import mediapipe as mp

from config import (
    MAX_HANDS,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE
)


class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            max_num_hands=MAX_HANDS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )


    def detect(self, frame):

        # BGR -> RGB
        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.hands.process(rgb)

        if not results.multi_hand_landmarks:
            return None, None


        hand = results.multi_hand_landmarks[0]


        # Draw skeleton
        self.mp_draw.draw_landmarks(
            frame,
            hand,
            self.mp_hands.HAND_CONNECTIONS
        )


        # Frame dimensions
        h, w, _ = frame.shape


        # Store landmarks
        landmarks = []

        for lm in hand.landmark:

            x = int(lm.x * w)
            y = int(lm.y * h)

            landmarks.append((x, y))


        # Left / Right hand
        hand_type = (
            results
            .multi_handedness[0]
            .classification[0]
            .label
        )


        return landmarks, hand_type


    def close(self):

        self.hands.close()