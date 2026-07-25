# Gesture Detection and Stabilization

from config import GESTURE_FRAMES_REQUIRED


TIP_IDS = [4, 8, 12, 16, 20]


def get_finger_states(landmarks, hand_type):

    fingers = []


    # Thumb
    if hand_type == "Right":

        if landmarks[4][0] < landmarks[3][0]:
            fingers.append(1)

        else:
            fingers.append(0)


    else:

        if landmarks[4][0] > landmarks[3][0]:
            fingers.append(1)

        else:
            fingers.append(0)


    # Other four fingers
    for tip in TIP_IDS[1:]:

        if landmarks[tip][1] < landmarks[tip - 2][1]:

            fingers.append(1)

        else:

            fingers.append(0)


    return fingers


# Gesture Detection
def detect_gesture(fingers):

    # Index only
    if fingers == [0, 1, 0, 0, 0]:

        return "DRAW"


    # Index + Middle
    elif fingers == [0, 1, 1, 0, 0]:

        return "SELECT"


    # Open palm
    elif fingers == [1, 1, 1, 1, 1]:

        return "ERASE"


    # Fist
    elif fingers == [0, 0, 0, 0, 0]:

        return "IDLE"


    return "IDLE"


# Gesture Stabilizer
class GestureStabilizer:

    def __init__(self):

        self.candidate = None
        self.count = 0
        self.stable_gesture = "IDLE"


    def update(self, gesture):

        if gesture == self.candidate:

            self.count += 1

        else:

            self.candidate = gesture
            self.count = 1


        if self.count >= GESTURE_FRAMES_REQUIRED:

            self.stable_gesture = gesture


        return self.stable_gesture