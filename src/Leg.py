import IK
import numpy as np

class Leg():
  def __init__(self, board, coxa, femur, tibia, config, name: str):
    self.board = board #control board the leg is attached to.
    self.config = config
    self.coxa = self.board.servo[coxa]
    self.femur = self.board.servo[femur]
    self.tibia = self.board.servo[tibia]
    self.name = name
    self.location = []

  def set_position(self,x,y,z):
    self.location = [(x*self.config["XYZ_DIRECTION"][0])+self.config["HOME_POSITION"][0],
                     (y*self.config["XYZ_DIRECTION"][1])+self.config["HOME_POSITION"][1],
                     (z*self.config["XYZ_DIRECTION"][2])+self.config["HOME_POSITION"][2]]
    
    coxaAngle, femurAngle, tibiaAngle = IK.getAngles(self.location[0],self.location[1],self.location[2])
    #print(f"coxa: {coxaAngle}, femur: {femurAngle}, tibia: {tibiaAngle}")
    
    self.coxa.angle = self.config["COXA"]["offset"]-coxaAngle*self.config["COXA"]["dir"]
    self.femur.angle = self.config["FEMUR"]["offset"]+((femurAngle-116)*self.config["FEMUR"]["dir"])
    self.tibia.angle = self.config["TIBIA"]["offset"]+((tibiaAngle-25)*self.config["TIBIA"]["dir"])