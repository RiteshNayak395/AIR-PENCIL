#the main file of project, it will run the whole program

import cv2

from config import (
    CAMERA_INDEX,
    CURRENT_COLOR,
    TOOLBAR_HEIGHT
)

from hand_tracker import HandTracker

from gesture import (
    get_finger_states,
    detect_gesture,
    GestureStabilizer
)

from painter import Painter

from utils import CoordinateSmoother

from ui import (
    draw_toolbar,
    select_color,
    draw_mode,
    draw_cursor,
    draw_eraser_cursor,
    draw_coordinates
)


# Initialize Camera

cap = cv2.VideoCapture(CAMERA_INDEX)


if not cap.isOpened():

    print("Error: Could not open webcam.")
    exit()


# Initialize Components
hand_tracker = HandTracker()

gesture_stabilizer = GestureStabilizer()

smoother = CoordinateSmoother()

painter = Painter()


# Default color
current_color = CURRENT_COLOR


# Main Loop

while True:

    success, frame = cap.read()


    if not success:

        print("Failed to read camera.")
        break


    # Mirror webcam
    frame = cv2.flip(frame, 1)


    # Create Canvas

    painter.create_canvas(frame)


    # Detect Hand

    landmarks, hand_type = hand_tracker.detect(frame)


    # Draw Toolbar

    draw_toolbar(
        frame,
        current_color
    )


    # Hand Detected

    if landmarks is not None:

        # Finger States

        fingers = get_finger_states(
            landmarks,
            hand_type
        )

        print("Finger State:", fingers)


        # Raw Gesture
        raw_gesture = detect_gesture(
            fingers
        )

        # Stable Gesture
        stable_gesture = (
            gesture_stabilizer.update(
                raw_gesture
            )
        )


        # Index Fingertip
        # Landmark 8

        raw_x, raw_y = landmarks[8]


        # Smooth Coordinates

        x, y = smoother.smooth(
            raw_x,
            raw_y
        )


        current_point = (x, y)


        # Display Mode
        draw_mode(
            frame,
            stable_gesture
        )


        # Coordinates

        draw_coordinates(
            frame,
            current_point
        )


        # DRAW MODE

        if stable_gesture == "DRAW":

            draw_cursor(
                frame,
                current_point,
                current_color
            )


            # Don't draw over toolbar
            if y > TOOLBAR_HEIGHT:

                painter.draw(
                    current_point,
                    current_color
                )

            else:

                painter.reset_previous()


        # SELECT MODE

        elif stable_gesture == "SELECT":

            painter.reset_previous()


            current_color = select_color(
                current_point,
                current_color
            )


        # ERASE MODE

        elif stable_gesture == "ERASE":

            painter.reset_previous()


            # Visible eraser
            draw_eraser_cursor(
                frame,
                current_point
            )


            # Don't erase toolbar
            if y > TOOLBAR_HEIGHT:

                painter.erase(
                    current_point
                )


        # IDLE MODE

        else:

            painter.reset_previous()


    # No Hand
    else:

        painter.reset_previous()

        smoother.reset()


    # Draw Toolbar Again
    # This updates selected color highlight
    draw_toolbar(
        frame,
        current_color
    )


    # Combine Webcam + Canvas
    output = painter.combine(
        frame
    )


    # Display
    cv2.imshow(
        "AI Air Pencil",
        output
    )


    # Keyboard
    key = cv2.waitKey(1) & 0xFF


    # C -> Clear
    if key == ord('c'):

        painter.clear()


    # Q -> Quit
    elif key == ord('q'):

        break


# Cleanup
cap.release()

hand_tracker.close()

cv2.destroyAllWindows()