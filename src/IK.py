import math

coxaLength = 39.9
femurLength = 110.0
tibiaLength = 157.5

def calculate_l(x, y, z):
    L1 = math.sqrt(x**2 + y**2)
    return math.sqrt(z**2 + (L1 - coxaLength)**2)

def calculate_coxa_angle(x, y):
    return math.atan2(x, y)

def calculate_femur_angle(x, y, z):
    L = calculate_l(x, y, z)
    alpha1 = math.acos(z/L)
    alpha2 = math.acos((tibiaLength**2 - femurLength**2 - L**2) / (-2 * femurLength * L))
    return alpha1 + alpha2

def calculate_tibia_angle(x, y, z):
    L = calculate_l(x, y, z)
    return math.acos((L**2 - tibiaLength**2 - femurLength**2)/(-2 * femurLength * tibiaLength))


def getAngles(x,y,z):
  coxaAngle = math.degrees(calculate_coxa_angle(x, y))
  femurAngle = math.degrees(calculate_femur_angle(x, y, z))
  tibiaAngle = math.degrees(calculate_tibia_angle(x, y, z))
  return coxaAngle, femurAngle, tibiaAngle