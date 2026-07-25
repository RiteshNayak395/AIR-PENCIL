# Configuration file for the Air Pencil application
# Camera
CAMERA_INDEX = 0


# MediaPipe
MAX_HANDS = 1

MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7


# Drawing

BRUSH_THICKNESS = 5
ERASER_THICKNESS = 80


# OpenCV uses BGR
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CURRENT_COLOR = GREEN

# Smoothing
SMOOTHING_ALPHA = 0.4

# Gesture Stabilization
GESTURE_FRAMES_REQUIRED = 4

# Jump Rejection
MAX_JUMP_DISTANCE = 80

# Toolbar
TOOLBAR_HEIGHT = 80


COLOR_BUTTONS = [

    ("GREEN", GREEN, (20, 10, 120, 65)),

    ("BLUE", BLUE, (140, 10, 240, 65)),

    ("RED", RED, (260, 10, 360, 65)),

    ("YELLOW", YELLOW, (380, 10, 500, 65))
]