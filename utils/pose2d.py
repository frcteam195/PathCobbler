import math
import stat
import constants

from translation2d import Translation2d
from rotation2d import Rotation2d


class Pose2d:
    def __init__(self, translation, rotation, comment=''):
        self.translation = translation
        self.rotation = rotation
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

