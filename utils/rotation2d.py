import math
import constants


class Rotation2d:
    def __init__(self, x, y, normalize):
        self.cos = x
        self.sin = y
        self.normalize = normalize
        if normalize:
            self.normalizeFunc()

    @staticmethod
    def fromRadians(angle_radians):
        return Rotation2d(math.cos(angle_radians), math.sin(angle_radians), False)

    @staticmethod
    def fromDegrees(angle_degrees):
        return Rotation2d.fromRadians(math.radians(angle_degrees))

    def normalizeFunc(self):
        magnitude = math.hypot(self.cos, self.sin)
        if magnitude > constants.kEps:
            self.cos /= magnitude
            self.sin /= magnitude
        else:
            self.cos = 1
            self.sin = 0

    def tan(self):
        if abs(self.cos) < constants.kEps:
            if self.sin >= 0.0:
                return math.inf
            else:
                return -math.inf

        return self.sin / self.cos

    def getRadians(self):
        return math.atan2(self.sin, self.cos)

    def getDegrees(self):
        return math.degrees(self.getRadians())

    def rotateBy(self, other):
        return Rotation2d(self.cos * other.cos - self.sin * other.sin, \
                          self.cos * other.sin + self.sin * other.cos, True)

    def normal(self):
        return Rotation2d(-self.sin, self.cos, False)

    def inverse(self):
        return Rotation2d(self.cos, -self.sin, False)

    def interpolate(self, other, x):
        if x <= 0:
            return Rotation2d(self.cos, self.sin, self.normalize)
        elif x >= 1:
            return Rotation2d(other.cos, other.sin, other.normalize)

        angle_diff = self.inverse().rotateBy(other).getRadians()
        return self.rotateBy(Rotation2d.fromRadians(angle_diff * x))

    def distance(self, other):
        return self.inverse().rotateBy(other).getRadians()
