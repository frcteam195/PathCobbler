import math


fieldWidth = 888  # inches
fieldHeight = 360  # inches

xOffset = 118.20125000
yOffset = fieldHeight - 21.90125000

width = 2704  # pixels
height = 1096  # pixels

bumperWidth = 3.5 * 2.0  # inches

robotWidth = 28 + bumperWidth  # inches
robotHeight = 31.75 + bumperWidth  # inches

C_R = math.sqrt(math.pow(robotWidth, 2) + math.pow(robotHeight, 2)) / 2
C_T = math.atan2(robotHeight, robotWidth)

waypointRadius = 7
splineWidth = 2

kEps = 1E-9
pi = math.pi
