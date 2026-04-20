import IK
import numpy as np

class Leg():
  def __init__(self,board,coxa,femur,tibia,config,home_position):
    self.board = board #control board the leg is attached to.
    self.config = config
    self.home_position = home_position
    self.coxa = self.board.servo[coxa]
    self.femur = self.board.servo[femur]
    self.tibia = self.board.servo[tibia]
    self.rest = [0,0,0]
    self.location = self.rest

  def set_position(self,x,y,z):
    self.location = [x+self.home_position[0],y+self.home_position[1],(z+self.home_position[2])]
    
    coxaAngle, femurAngle, tibiaAngle = IK.getAngles(self.location[0],self.location[1],self.location[2])
    
    self.coxa.angle = self.config["COXA"]["offset"]-coxaAngle*self.config["COXA"]["dir"]
    print(f"coxa: {coxaAngle}, femur: {femurAngle}, tibia: {tibiaAngle}")
    self.femur.angle = self.config["FEMUR"]["offset"]+((femurAngle-116)*self.config["FEMUR"]["dir"])
    self.tibia.angle = self.config["TIBIA"]["offset"]+((tibiaAngle-25)*self.config["TIBIA"]["dir"])