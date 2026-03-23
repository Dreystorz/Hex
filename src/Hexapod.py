from Leg import Leg
from adafruit_servokit import ServoKit
import time
import numpy

class Hexapod:
  def __init__(self):
    self.left = ServoKit(channels=16, address=0x41)
    self.right = ServoKit(channels=16)
    self.left.servo[11].set_pulse_width_range(620,2430) #1c
    self.left.servo[10].set_pulse_width_range(600,2400) #1f
    self.left.servo[9].set_pulse_width_range(640,2450)  #1t

    self.left.servo[15].set_pulse_width_range(580,2380) #4c
    self.left.servo[14].set_pulse_width_range(480,2280) #4f
    self.left.servo[13].set_pulse_width_range(650,2470) #4t

    self.left.servo[3].set_pulse_width_range(500,2370)  #6c
    self.left.servo[2].set_pulse_width_range(560,2380)  #6f
    self.left.servo[1].set_pulse_width_range(610,2450)  #6t

    self.right.servo[4].set_pulse_width_range(630,2450) #2c
    self.right.servo[5].set_pulse_width_range(710,2520) #2f
    self.right.servo[6].set_pulse_width_range(500,2300) #2t

    self.right.servo[0].set_pulse_width_range(640,2435) #3c
    self.right.servo[1].set_pulse_width_range(600,2390) #3f
    self.right.servo[2].set_pulse_width_range(590,2420) #3t

    self.right.servo[12].set_pulse_width_range(570,2380)#5c
    self.right.servo[13].set_pulse_width_range(640,2450)#5f
    self.right.servo[14].set_pulse_width_range(500,2300)#5t

    self.L1 = Leg(self.left,55,3,2,1,"left")
    self.L2 = Leg(self.left,0,11,10,9,"left")
    self.L3 = Leg(self.left,-55,15,14,13,"left")

    self.R1 = Leg(self.right,-55,0,1,2,"right")
    self.R2 = Leg(self.right,0,4,5,6,"right")
    self.R3 = Leg(self.right,55,12,13,14,"right")
    self.primingComplete = True
    self.standing = False
    self.height = 80
    self.maxIndex = 0
    self.moving = False
    self.restTime = 0.03
    self.stopped = True

  def update(self):
    if self.L1.tempComplete and self.L2.tempComplete and self.L3.tempComplete and self.R1.tempComplete and self.R2.tempComplete and self.R3.tempComplete:
      self.primingComplete = True
    else:
      self.primingComplete = False
    self.maxIndex = max([self.L1.pathLen(),self.L2.pathLen(),self.L3.pathLen(),
                        self.R1.pathLen(),self.R2.pathLen(),self.R3.pathLen()])
    self.L1.update(self.primingComplete)
    self.L2.update(self.primingComplete)
    self.L3.update(self.primingComplete)
    self.R1.update(self.primingComplete)
    self.R2.update(self.primingComplete)
    self.R3.update(self.primingComplete)
    time.sleep(self.restTime)

  def setAngles(self,angle):
    self.L1.setOffsetAngle = angle
    self.L2.setOffsetAngle = angle
    self.L3.setOffsetAngle = angle
    self.R1.setOffsetAngle = angle
    self.R2.setOffsetAngle = angle
    self.R3.setOffsetAngle = angle

  def walk(self,dVector):
    stepHeight = 80
    x,y = dVector
    x = 8-int(x/15)
    if x == 9:
      x = 8
    y = 8-int(y/15)
    if y == -9:
      y = -8

    self.L1.setOffsetAngle(x,y)
    self.L2.setOffsetAngle(x,y)
    self.L3.setOffsetAngle(x,y)
    self.R1.setOffsetAngle(x,y)
    self.R2.setOffsetAngle(x,y)
    self.R3.setOffsetAngle(x,y)
    if abs(y) < 2 and abs(y) > -2 and (abs(x) < 2 and abs(x) > -2) and not self.stopped:
      self.restTime = 0.001
      self.moving = False
      self.stopped = True
      self.standing = False
      self.stand()
    if abs(y) == 2 or abs(x) == 2:
      self.restTime = 0.03
    if abs(y) == 3 or abs(x) == 3:
      self.restTime = 0.025
    if abs(y) == 4 or abs(x) == 4:
      self.restTime = 0.02
    if abs(y) == 5 or abs(x) == 5:
      self.restTime = 0.015
    if abs(y) == 6 or abs(x) == 6:
      self.restTime = 0.01
    if abs(y) == 7 or abs(x) == 7:
      self.restTime = 0.07
    if abs(y) == 8 or abs(x) == 8:
      self.restTime = 0.0005

    if((y != 0 or x != 0) and not self.moving):
      self.moving = True
      self.standing = False
      self.stopped = False
      start = (80,-45,-self.height)
      end = (80,45,-self.height)
      self.L1.createPath(start,end,5,cycle=0.0,isCyclic=True,height2=stepHeight)
      self.L2.createPath(start,end,5,cycle=0.5,isCyclic=True,height2=stepHeight)
      self.L3.createPath(start,end,5,cycle=0.0,isCyclic=True,height2=stepHeight)
      self.R1.createPath(start,end,5,cycle=0.5,isCyclic=True,height2=stepHeight)
      self.R2.createPath(start,end,5,cycle=0.0,isCyclic=True,height2=stepHeight)
      self.R3.createPath(start,end,5,cycle=0.5,isCyclic=True,height2=stepHeight)

  def stand(self):
    if self.standing:
      return
    point = (80,0,-self.height)
    self.L1.createPath(self.L1.location,point)
    self.L2.createPath(self.L2.location,point)
    self.L3.createPath(self.L3.location,point)
    self.R1.createPath(self.R1.location,point)
    self.R2.createPath(self.R2.location,point)
    self.R3.createPath(self.R3.location,point)
    self.standing = True
    self.moving = False

  def setHeight(self,height):
    self.height = height

  def adjustHeight(self,amount):
    if(amount == 0):
      return
    amount = amount*2
    if(self.height < 200 and amount > 0):
      self.standing = False
      self.height = self.height+amount
      rest = self.restTime
      self.restTime = 0
      self.stand()
      self.update()
      self.restTime = rest
    elif(self.height > 30 and amount < 0):
      self.standing = False
      self.height = self.height+amount
      rest = self.restTime
      self.restTime = 0
      self.stand()
      self.update()
      self.restTime = rest
      

  def returnToRest(self):
    if not self.standing and (not self.moving):
      return
    point = (0,0,0)
    self.L1.createPath(self.L1.location,point)
    self.L2.createPath(self.L2.location,point)
    self.L3.createPath(self.L3.location,point)
    self.R1.createPath(self.R1.location,point)
    self.R2.createPath(self.R2.location,point)
    self.R3.createPath(self.R3.location,point)
    self.standing = False
    self.moving = False

  def setDefaultRestTime(self):
    self.restTime = 0.03
  # x = out, y = side, z = height