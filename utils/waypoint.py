class Waypoint:
    def __init__(self, x, y, track, heading, curvature=0, enabled=True):
        self.x = float(x)
        self.y = float(y)
        self.track = float(track)
        self.heading = float(heading)
        self.curvature = float(curvature)
        self.enabled = enabled
        self.clicked = False

    def set_clicked(self, clicked: bool):
        self.clicked = clicked

    def __str__(self):
        return f'X: {self.x}, Y: {self.y}, Theta: {self.track}, Heading: {self.heading} Enabled: {"Y" if self.enabled else "N"}'

    def toJson(self):
        json_obj = dict()

        json_obj['x'] = self.x
        json_obj['y'] = self.y
        json_obj['theta'] = self.track
        json_obj['heading'] = self.heading
        json_obj['comment'] = ''

        return json_obj
