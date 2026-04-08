import IK
import path
import numpy as np
from abc import ABC, abstractmethod

class Leg(ABC):
  def __init__(self,board,angle,coxa,femur,tibia):
    self.board = board #control board the leg is attached to.
    self.angle = angle #angle of leg relative to the side its on, perpendicular to the body is 0, positive is front, negative is back.
    self.offsetAngle = 0
    self.coxa = self.board.servo[coxa]
    self.femur = self.board.servo[femur]
    self.tibia = self.board.servo[tibia]
    self.path = [np.array((0,0,0))]
    self.tempPath = [np.array((0,0,0))]
    self.rest = [0,0,0]
    self.location = self.rest
    self.cycle = 0.0
    self.isCyclic = False
    self.index = 0
    self.tempIndex = 0
    self.tempComplete = True

  def pathLen(self):
    n = 0
    if(self.tempPath):
      n = len(self.tempPath)
    return len(self.path)+n
  
  def setOffsetAngle(self,x,y):
    angle = 0
    if y < 0:
      angle = 180+(-np.degrees(np.arctan(x/y)))
    elif y > 0:
      angle = -np.degrees(np.arctan(x/y))
      if x > 0:
        angle = 360+angle
    elif x > 0:
      angle = 270
    elif x < 0:
      angle = 90

    self.offsetAngle=angle
  
  def toRest(self):
    self.createPath(self.location,self.rest)

  def createPath(self,start,end,step=2,cycle=0.0,isCyclic=False,height=0, height2=0):
    self.isCyclic = isCyclic
    self.tempPath = None
    self.tempIndex = 0
    self.path = None
    self.index = 0

    #If angle of leg is not 0 rotate points accordingly
    start,end,self.location = rotateAboutCenter(self,start,self.location,end)

    #If start and end points are the same set path to start set index to 0 and return
    if(start[0] == end[0] and start[1] == end[1] and start[2] == end[2]):
      self.path = [np.array(start)]
      self.index = 0
      return
    
    #Generate path points
    self.path = path.getPath(start,end,step,height)
    if(isCyclic): #If looping generate path points backwards, if height2 is given generate curved path
      self.path.extend(path.getPath(end,start,step,height2))

    #Set index in terms of cycle, if greater than length of path, wrap around
    self.index = int(len(self.path)*cycle)
    if(self.index >= len(self.path)):
      self.index = self.index-len(self.path)

    #Create temporary path to place legs into starting position
    if(self.location[0] == self.path[self.index][0] and self.location[1] == self.path[self.index][1] and self.location[2] == self.path[self.index][2]):
      self.tempPath = None
      self.tempIndex = 0
    else:
      self.tempPath = path.getPath(self.location,self.path[self.index],step)
      self.tempIndex = 0
      self.tempComplete = False
  
  @abstractmethod
  def setServoAngles(self, point):
    pass

  def update(self, ready):
    p = None
    i = 0
    #Return if no path or index is out of bounds or only 1 point
    if not self.path or self.index >= len(self.path) or len(self.path)<=1:
      return
    
    #Use path if tempPath doesnt exist or is complete
    tempUsed = False
    if(self.tempPath and self.tempIndex < len(self.tempPath) and not len(self.tempPath)<=1):
      p = self.tempPath
      i = self.tempIndex
      tempUsed = True
    else:
      self.tempComplete = True
      if not ready: return
      p = self.path
      i = self.index

    #Set servo angles to current point
    self.setServoAngles(p[i])

    #Set current location to current point
    self.location = p[i]


    #Increment tempIndex if used otherwise increment index
    if(tempUsed):
      self.tempIndex = self.tempIndex+1
    else:
      self.tempPath = None
      self.tempIndex = 0
      self.index = self.index+1
      if(self.index >= len(self.path) and self.isCyclic):
        self.index = 0

class LeftLeg(Leg):
  def setOffsetAngle(self, x, y):
    super().setOffsetAngle(x, y)
    self.offsetAngle = -self.offsetAngle

  def setServoAngles(self, point):
    self.coxa.angle = IK.getCoxaAngleLeft(point)
    self.femur.angle = IK.getFemurAngleLeft(point)
    self.tibia.angle = IK.getTibiaAngleLeft(point)

class RightLeg(Leg):
  def setServoAngles(self, point):
    self.coxa.angle = IK.getCoxaAngleRight(point)
    self.femur.angle = IK.getFemurAngleRight(point)
    self.tibia.angle = IK.getTibiaAngleRight(point)

#==========================================================================================#
def rotateAboutCenter(self,start,location,end):
   if(location[0] == start[0] and location[1] == start[1]): return start,end,location
   center = np.array(tuple((a + b) / 2 for a, b in zip(start, end)))
   center = (center[0],center[1])
   s = rotate_point((start[0],start[1]),self.offsetAngle,center)
   s = rotate_point((s[0],s[1]),self.angle)
   start = (s[0],s[1],start[2])
   e = rotate_point((end[0],end[1]),self.offsetAngle,center)
   e = rotate_point((e[0],e[1]),self.angle)
   end = (e[0],e[1],end[2])

   return start,end,location

def rotate_point_around_origin(point, angle_deg):
    theta = np.radians(angle_deg)
    R = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])
    return R @ point

def rotate_point(point, angle_deg, orgin=(0,0)):
    orgin = np.array(orgin)
    point = np.array(point)
    # Step 1: Translate p2 relative to p1
    relative = point - orgin

    # Step 2: Rotate the vector
    rotated_relative = rotate_point_around_origin(relative, angle_deg)

    # Step 3: Translate back to original position
    new_point = orgin + rotated_relative

    return new_point
