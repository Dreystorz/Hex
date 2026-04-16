import IK
import numpy as np

class Leg():
  def __init__(self,board,angle,coxa,femur,tibia):
    self.board = board #control board the leg is attached to.
    self.angle = angle #angle of leg relative to the side its on, perpendicular to the body is 0, positive is front, negative is back.
    self.coxa = self.board.servo[coxa]
    self.femur = self.board.servo[femur]
    self.tibia = self.board.servo[tibia]
    self.rest = [0,0,0]
    self.location = self.rest

  def set_position(self,x,y,z):
    self.location = [x,y,z]
    coxaAngle, femurAngle, tibiaAngle = IK.getAngles(x,y,z,self.angle)
    self.coxa.angle = coxaAngle
    self.femur.angle = femurAngle
    self.tibia.angle = tibiaAngle
