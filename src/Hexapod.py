from Leg import LeftLeg, RightLeg, Leg
from adafruit_servokit import ServoKit
import time
from enum import Enum, auto

class HexState(Enum):
  IDLE = auto()
  STANDING = auto()
  WALKING = auto()
  ROTATING = auto()

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

    self.state = HexState.IDLE
    self.prev_state = None

    self.primingComplete = True
    self.height = 80
    self.maxIndex = 0
    self.restTime = 0.03
    self.directionVector = (0,0)
    self.rotationVelocity = 0

  def setDirectionVector(self, directionVector):
    if not directionVector:
      self.directionVector = (0,0)
      return
    x,y = directionVector
    x = 8-int(x/15)
    y = 8-int(y/15)

    x = max(-8, min(8, x))
    y = max(-8, min(8, y))
    self.directionVector = (x, y)

  def setRotationVelocity(self, rotationVelocity):
    if not rotationVelocity:
      self.rotationVelocity = 0
      return
    self.rotationVelocity = int((rotationVelocity-128)/128*10)

  def set_state(self, new_state):
    if not self.isValidStateChange(new_state):
      return
    self.prev_state = self.state
    self.on_exit(self.state)
    self.state = new_state
    self.on_enter(new_state)

  def isValidStateChange(self, new_state):
    if self.state == new_state:
      return False
    if self.state == HexState.IDLE:
      if new_state != HexState.STANDING:
        return False
    if self.state == HexState.STANDING:
      pass
    if self.state == HexState.WALKING:
      if new_state != HexState.STANDING:
        return False
    if self.state == HexState.ROTATING:
      if new_state != HexState.STANDING:
        return False
    return True
  
  def on_enter(self, state):
    if state == HexState.IDLE:
      print("Entering IDLE")
      self.restTime = 0.03
      self.returnToRest()

    if state == HexState.STANDING:
      print("Entering STANDING")
      self.restTime = 0.03
      self.stand()

    if state == HexState.WALKING:
      print("Entering WALKING")
      
    if state == HexState.ROTATING:
      print("Entering ROTATING")

  def on_exit(self, state):
    if state == HexState.IDLE:
      print("Exiting IDLE")

    if state == HexState.STANDING:
      print("Exiting STANDING")

    if state == HexState.WALKING:
      print("Exiting WALKING")

    if state == HexState.ROTATING:
      print("Exiting ROTATING")

  def handle_idle(self):
    pass

  def handle_standing(self):
    x,y = self.directionVector
    if abs(y) >= 2 or abs(x) >= 2:
      self.set_state(HexState.WALKING)

  def handle_walking(self):
    stepHeight = 80
    x,y = self.directionVector

    #Creates an input dead zone for the controller if below a certain threshhold. Sets Hex into standing mode.
    if abs(y) < 2 and abs(x) < 2:
      self.set_state(HexState.STANDING)
      return

    self.setAngles(x,y)

    #Maps the controller speed to rest time which affect movment speed.
    if(abs(y) >= 2) or (abs(x) >= 2):
      speed = max(abs(x),abs(y))
      self.restTime = (((8-speed)*(0.03-0.003))/6)+0.003

    if(y != 0 or x != 0):
      start = (80,-45,-self.height)
      end = (80,45,-self.height)
      self.L1.createPath(start,end,5,cycle=0.0,isCyclic=True,height2=stepHeight)
      self.L2.createPath(start,end,5,cycle=0.5,isCyclic=True,height2=stepHeight)
      self.L3.createPath(start,end,5,cycle=0.0,isCyclic=True,height2=stepHeight)
      self.R1.createPath(start,end,5,cycle=0.5,isCyclic=True,height2=stepHeight)
      self.R2.createPath(start,end,5,cycle=0.0,isCyclic=True,height2=stepHeight)
      self.R3.createPath(start,end,5,cycle=0.5,isCyclic=True,height2=stepHeight)

  def handle_rotation(self):
    pass

  def update(self):
    if self.state == HexState.IDLE:
      self.handle_idle()
    if self.state == HexState.STANDING:
      self.handle_standing()
    if self.state == HexState.WALKING:
      self.handle_walking()
    if self.state == HexState.ROTATING:
      self.handle_rotation()

    self.moveLegs()
    time.sleep(self.restTime)

  def moveLegs(self):
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

  def setAngles(self,anglex,angley):
    self.L1.setOffsetAngle(anglex,angley)
    self.L2.setOffsetAngle(anglex,angley)
    self.L3.setOffsetAngle(anglex,angley)
    self.R1.setOffsetAngle(anglex,angley)
    self.R2.setOffsetAngle(anglex,angley)
    self.R3.setOffsetAngle(anglex,angley)

  def stand(self):
    point = (80,0,-self.height)
    self.L1.createPath(self.L1.location,point)
    self.L2.createPath(self.L2.location,point)
    self.L3.createPath(self.L3.location,point)
    self.R1.createPath(self.R1.location,point)
    self.R2.createPath(self.R2.location,point)
    self.R3.createPath(self.R3.location,point)

  def setHeight(self,height):
    self.height = height

  def adjustHeight(self,amount):
    if(amount == 0 or self.state != HexState.STANDING):
      return
    amount = amount*2
    if(self.height < 200 and amount > 0) or (self.height > 30 and amount < 0):
      self.height = self.height+amount
      self.stand()
      self.moveLegs()
      

  def returnToRest(self):
    point = (0,0,0)
    self.L1.createPath(self.L1.location,point)
    self.L2.createPath(self.L2.location,point)
    self.L3.createPath(self.L3.location,point)
    self.R1.createPath(self.R1.location,point)
    self.R2.createPath(self.R2.location,point)
    self.R3.createPath(self.R3.location,point)

  # x = out, y = side, z = height