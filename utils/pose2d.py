import math
import stat
import constants

from translation2d import Translation2d
from rotation2d import Rotation2d


class Pose2d:
    def __init__(self, translation, rotation, comment=''):
        self.translation: Translation2d = translation
        self.rotation: Rotation2d = rotation
        self.comment = comment

    @staticmethod
    def exp(delta):
        sin_theta = math.sin(delta.dtheta)
        cos_theta = math.cos(delta.dtheta)
        s = 0
        c = 0

        if abs(delta.dtheta) < constants.kEps:
            s = 1.0 - 1.0 / 6.0 * delta.dtheta * delta.dtheta
            c = 0.5 * delta.dtheta
        else:
            s = sin_theta / delta.dtheta
            c = (1.0 - cos_theta) / delta.dtheta

        return Pose2d(Translation2d(delta.dx * s - delta.dy * c, delta.dx * c + delta.dy * s), \
                      Rotation2d(cos_theta, sin_theta, False))

    @staticmethod
    def log(transform):
        dtheta = transform.getRotation().getRadians()
        half_dtheta = 0.5 * dtheta
        cos_minus_one = transform.getRotation().cos - 1.0
        halftheta_by_tan_of_halfdtheta = 0

        if abs(cos_minus_one) < constants.kEps:
            halftheta_by_tan_of_halfdtheta = 1.0 - 1.0 / 12.0 * dtheta * dtheta
        else:
            halftheta_by_tan_of_halfdtheta = -(half_dtheta * transform.getRotation().sin) / cos_minus_one

        translation_part = transform.getTranslation().rotateBy(Rotation2d(halftheta_by_tan_of_halfdtheta, -half_dtheta, False))
        return Twist2d(translation_part.x, translation_part.y, dtheta)

    def getTranslation(self):
        return self.translation

    def getRotation(self):
        return self.rotation

    def transformBy(self, other):
        return Pose2d(self.translation.translateBy(other.translation.rotateBy(self.rotation)), \
                      self.rotation.rotateBy(other.rotation))

    def inverse(self):
        rotation_inverted = self.rotation.inverse()
        return Pose2d(self.translation.inverse().rotateBy(rotation_inverted), rotation_inverted)

    def normal(self):
        return Pose2d(self.translation, self.rotation.normal())

    def interpolate(self, other, x):
        if x <= 0:
            return Pose2d(self.translation, self.rotation, self.comment)
        elif x >= 1:
            return Pose2d(other.translation, other.rotation, other.comment)

        twist = Pose2d.log(self.inverse().transformBy(other))
        return self.transformBy(Pose2d.exp(twist.scaled(x)))

    def distance(self, other):
        return Pose2d.log(self.inverse().transformBy(other)).norm()

    def heading(self, other):
        return math.atan2(self.translation.y - other.translation.y, self.translation.x - other.translation.x)

    def transform(self, other):
        other.position.rotate(self.rotation)
        self.translation.translateBy(other.translation)
        self.rotation.rotateBy(other.rotation)
