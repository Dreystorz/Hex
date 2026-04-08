from Leg import LeftLeg, RightLeg, Leg
from adafruit_servokit import ServoKit
import time
import numpy

class Hexapod:
  def __init__(self):
    self.left = ServoKit(channels=16, address=0x41)
    self.right = ServoKit(channels=16)
    #Initializing the pulse width ranges for each servo, these were found through testing and are not exact.
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

    #Leg initialization, the parameters are (kit,coxaChannel,femurChannel,tibiaChannel,offsetAngle).
    self.L1 = LeftLeg(self.left,55,3,2,1)
    self.L2 = LeftLeg(self.left,0,11,10,9)
    self.L3 = LeftLeg(self.left,-55,15,14,13)

    self.R1 = RightLeg(self.right,-55,0,1,2)
    self.R2 = RightLeg(self.right,0,4,5,6)
    self.R3 = RightLeg(self.right,55,12,13,14)

    self.primingComplete = True
    self.standing = False
    self.height = 80
    self.maxIndex = 0
    self.moving = False
    self.restTime = 0.03
    self.stopped = True

  def update(self):
    #This ensures the legs stay in sync.
    if self.L1.tempComplete and self.L2.tempComplete and self.L3.tempComplete and self.R1.tempComplete and self.R2.tempComplete and self.R3.tempComplete:
      self.primingComplete = True
    else:
      self.primingComplete = False
    #Sets the maximum path length of any of the legs, this is used to ensure all legs finish their paths at the same time.
    self.maxIndex = max([self.L1.pathLen(),self.L2.pathLen(),self.L3.pathLen(),
                        self.R1.pathLen(),self.R2.pathLen(),self.R3.pathLen()])
    self.L1.update(self.primingComplete)
    self.L2.update(self.primingComplete)
    self.L3.update(self.primingComplete)
    self.R1.update(self.primingComplete)
    self.R2.update(self.primingComplete)
    self.R3.update(self.primingComplete)
    time.sleep(self.restTime)

  def setAngles(self,anglex,angley):
    self.L1.setOffsetAngle(anglex,angley)
    self.L2.setOffsetAngle(anglex,angley)
    self.L3.setOffsetAngle(anglex,angley)
    self.R1.setOffsetAngle(anglex,angley)
    self.R2.setOffsetAngle(anglex,angley)
    self.R3.setOffsetAngle(anglex,angley)

  def walk(self,directionVector):
    stepHeight = 80
    x,y = directionVector
    x = 8-int(x/15)
    y = 8-int(y/15)

    x = max(-8, min(8, x))
    y = max(-8, min(8, y))

    self.setAngles(x,y)

    #Creates an input dead zone for the controller if below a certain threshhold. Sets Hex into standing mode.
    if abs(y) < 2 and abs(x) < 2 and not self.stopped:
      self.restTime = 0.001
      self.moving = False
      self.stopped = True
      self.standing = False
      self.stand()

    #Maps the controller speed to rest time which affect movment speed.
    if(abs(y) >= 2) or (abs(x) >= 2):
      speed = max(abs(x),abs(y))
      self.restTime = (((8-speed)*(0.03-0.003))/6)+0.003

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

  def rotate(self,rotationVector):
    #print(rotationVector)
    pass

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