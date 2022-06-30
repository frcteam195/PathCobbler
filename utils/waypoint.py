class Waypoint:
    def __init__(self, x, y, heading, enabled=True):
        self.x = float(x)
        self.y = float(y)
        self.heading = float(heading)
        self.enabled = enabled

    def __str__(self):
        return f'X: {self.x}, Y: {self.y}, Theta: {self.heading}'
