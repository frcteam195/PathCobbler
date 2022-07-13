import math
import constants

from rotation2d import Rotation2d

class Translation2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norm(self):
        return math.hypot(self.x, self.y)

    def norm2(self):
        return self.x * self.x + self.y * self.y

    def translateBy(self, other):
        return Translation2d(self.x + other.x, self.y + other.y)

    def rotateBy(self, rotation):
        return Translation2d(self.x * rotation.cos - self.y * rotation.sin, self.x * rotation.sin + self.y * rotation.cos)

    def direction(self):
        return Rotation2d(self.x, self.y, True)

    def inverse(self):
        return Translation2d(-self.x, -self.y)

    def interpolate(self, other, x):
        if x <= 0:
            return Translation2d(self.x, self.y)
        elif x >= 1:
            return Translation2d(other.x, other.y)

        return self.extrapolate(other, x)

    def extrapolate(self, other, x):
        return Translation2d(x * (other.x - self.x) + self.x, x * (other.y - self.y) + self.y)

    def scale(self, s):
        return Translation2d(self.x * s, self.y * s)

    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y

    @staticmethod
    def getAngle(a, b):
        cos_angle = Translation2d.dot(a, b) / (a.norm() * b.norm())
        if math.isnan(cos_angle):
            return Rotation2d(1, 0, False)

        return Rotation2d.fromRadians(math.acos(math.min(1.0, math.max(cos_angle, -1.0))))

    @staticmethod
    def cross(a, b):
        return a.x * b.y - a.y * b.x

    def distance(self, other):
        return self.inverse().translateBy(other).norm()

    def drawX(self):
        return (self.x + constants.xOffset) * (constants.width / constants.fieldWidth)

    def drawY(self):
        return constants.height - (self.y + constants.yOffset) * (constants.height / constants.fieldHeight)
