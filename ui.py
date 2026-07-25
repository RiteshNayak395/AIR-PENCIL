#select color, draw toolbar, draw mode, draw cursor, draw eraser cursor, draw coordinates

import cv2

from config import (
    COLOR_BUTTONS,
    TOOLBAR_HEIGHT,
    ERASER_THICKNESS,
    WHITE
)


# Draw Toolbar
def draw_toolbar(frame, current_color):

    cv2.rectangle(
        frame,
        (0, 0),
        (frame.shape[1], TOOLBAR_HEIGHT),
        (40, 40, 40),
        -1
    )


    for name, color, box in COLOR_BUTTONS:

        x1, y1, x2, y2 = box


        # Color button
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            -1
        )


        # Button text
        cv2.putText(
            frame,
            name,
            (x1 + 10, y1 + 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            WHITE,
            2
        )


        # Highlight selected color
        if color == current_color:

            cv2.rectangle(
                frame,
                (x1 - 3, y1 - 3),
                (x2 + 3, y2 + 3),
                WHITE,
                3
            )


# Color Selection
def select_color(point, current_color):

    x, y = point


    for name, color, box in COLOR_BUTTONS:

        x1, y1, x2, y2 = box


        if x1 <= x <= x2 and y1 <= y <= y2:

            return color


    return current_color


# Display Mode
def draw_mode(frame, mode):

    cv2.putText(
        frame,
        mode,
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        WHITE,
        2
    )


# Fingertip Cursor
def draw_cursor(frame, point, color):

    cv2.circle(
        frame,
        point,
        8,
        color,
        -1
    )


# Eraser Cursor
def draw_eraser_cursor(frame, point):

    cv2.circle(
        frame,
        point,
        ERASER_THICKNESS // 2,
        WHITE,
        2
    )


# Coordinates
def draw_coordinates(frame, point):

    x, y = point


    cv2.putText(
        frame,
        f"({x}, {y})",
        (x + 10, y + 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        WHITE,
        2
    )