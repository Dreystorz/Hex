import math

coxaLength = 39.9
femurLength = 110.0
tibiaLength = 157.5
# restOffsetX = 70
# restOffsetZ = -7
restOffsetX = 0
restOffsetZ = 0

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

def getCoxaAngle(x,y):
  x = restOffsetX+x
  angle = math.atan(y/x)
  angle = 90-math.degrees(angle)
  return angle

def getAngles(x,y,z,offset):
  coxaAngle = getCoxaAngle(x,y)-offset
  femurAngle = getFemurAngle(x,y,z)
  tibiaAngle = getTibiaAngle(x,y,z)
  return coxaAngle, femurAngle, tibiaAngle