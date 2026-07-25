#calculate distance between two points and smooth the coordinates of the points to reduce jitter
import math

from config import SMOOTHING_ALPHA


class CoordinateSmoother:

    def __init__(self):

        self.x = None
        self.y = None


    def smooth(self, raw_x, raw_y):

        alpha = SMOOTHING_ALPHA


        if self.x is None or self.y is None:

            self.x = raw_x
            self.y = raw_y

        else:

            self.x = (
                alpha * raw_x
                + (1 - alpha) * self.x
            )

            self.y = (
                alpha * raw_y
                + (1 - alpha) * self.y
            )


        return int(self.x), int(self.y)


    def reset(self):

        self.x = None
        self.y = None


# Distance
def point_distance(point1, point2):

    return math.hypot(
        point1[0] - point2[0],
        point1[1] - point2[1]
    )