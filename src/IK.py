import math

coxaLength = 39.9
femurLength = 110.0
tibiaLength = 157.5
restOffsetX = 70
restOffsetZ = -7

def getTibiaAngle(x,y,z):
  a = femurLength
  b = tibiaLength
  x = restOffsetX+x
  z = restOffsetZ+z
  k = math.sqrt((y*y)+(x*x))
  h = math.sqrt((k*k)+(z*z))
  angle = math.acos(((a*a)+(b*b)-(h*h))/(2*b*a))
  angle = math.degrees(angle)
  return angle

def getTibiaAngleRight(point):
  angle = 198-getTibiaAngle(point[0],point[1],point[2])
  return angle

def getTibiaAngleLeft(point):
  angle = getTibiaAngle(point[0],point[1],point[2])-18
  return angle

def getFemurAngle(x,y,z):
  a = femurLength
  b = tibiaLength
  x = restOffsetX+x
  z = restOffsetZ+z
  if(x == 0):
    return 90
  k = math.sqrt((y*y)+(x*x))
  h = math.sqrt((k*k)+(z*z))
  angle = math.acos(((h*h)+(a*a)-(b*b))/(2*h*a))+math.atan(z/k)
  angle = math.degrees(angle)
  return  angle

def getFemurAngleRight(point):
  angle = 65+getFemurAngle(point[0],point[1],point[2])
  return angle


def getFemurAngleLeft(point):
  angle = 115-getFemurAngle(point[0],point[1],point[2])
  return angle

def getCoxaAngle(x,y,z):
  x = restOffsetX+x
  angle = math.atan(y/x)
  angle = 90-math.degrees(angle)
  return angle

def getCoxaAngleRight(point):
  return 180-getCoxaAngle(point[0],point[1],point[2])

def getCoxaAngleLeft(point):
  return getCoxaAngle(point[0],point[1],point[2])
