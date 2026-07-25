# handel drawing and erasing on the canvas, as well as combining the canvas with the camera feed
import cv2
import numpy as np

from config import (
    BRUSH_THICKNESS,
    ERASER_THICKNESS,
    MAX_JUMP_DISTANCE
)

from utils import point_distance


class Painter:

    def __init__(self):

        self.canvas = None
        self.previous_point = None


    # Create Canvas
    def create_canvas(self, frame):

        if self.canvas is None:

            self.canvas = np.zeros_like(frame)


    # Draw
    def draw(self, current_point, color):

        if self.previous_point is None:

            self.previous_point = current_point
            return


        distance = point_distance(
            self.previous_point,
            current_point
        )


        # Reject suspicious jumps
        if distance <= MAX_JUMP_DISTANCE:

            cv2.line(
                self.canvas,
                self.previous_point,
                current_point,
                color,
                BRUSH_THICKNESS
            )


        self.previous_point = current_point


    # Erase
    def erase(self, point):

        cv2.circle(
            self.canvas,
            point,
            ERASER_THICKNESS // 2,
            (0, 0, 0),
            -1
        )


    # Reset Previous Point
    def reset_previous(self):

        self.previous_point = None


    # Clear Entire Canvas
    def clear(self):

        if self.canvas is not None:

            self.canvas[:] = 0

        self.previous_point = None


    # Binary Mask
    def create_mask(self):

        gray_canvas = cv2.cvtColor(
            self.canvas,
            cv2.COLOR_BGR2GRAY
        )


        _, drawing_mask = cv2.threshold(
            gray_canvas,
            1,
            255,
            cv2.THRESH_BINARY
        )


        return drawing_mask


    # Combine Canvas + Camera
    def combine(self, frame):

        # Binary drawing mask
        drawing_mask = self.create_mask()


        # Inverse mask
        inverse_mask = cv2.bitwise_not(
            drawing_mask
        )


        # Webcam background
        frame_background = cv2.bitwise_and(
            frame,
            frame,
            mask=inverse_mask
        )


        # Drawing foreground
        canvas_foreground = cv2.bitwise_and(
            self.canvas,
            self.canvas,
            mask=drawing_mask
        )


        # Final image
        output = cv2.add(
            frame_background,
            canvas_foreground
        )


        return output