from Leg import Leg
from adafruit_servokit import ServoKit
from enum import Enum, auto

class HexState(Enum):
  SITTING_IDLE = auto()
  SITTING_DOWN = auto()
  STANDING_UP = auto()
  STANDING_IDLE = auto()
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
    self.Legs = [Leg(self.left,35,3,2,1), 
                 Leg(self.left,0,11,10,9), 
                 Leg(self.left,-35,15,14,13), 
                 Leg(self.right,35,0,1,2), 
                 Leg(self.right,0,4,5,6), 
                 Leg(self.right,-35,12,13,14)]

    self.state = HexState.SITTING_IDLE
    self.prev_state = None

    self.height = 80
    self.phase_increment = 0.01
    self.phase = 0

  def set_state(self, new_state):
    if not self.isValidStateChange(new_state):
      return
    self.prev_state = self.state
    self.on_exit(self.state)
    self.state = new_state
    self.on_enter(new_state)

  def isValidStateChange(self, new_state):
    if self.state == HexState.SITTING_IDLE and new_state not in [HexState.STANDING_UP]:
      return False
    if self.state == HexState.SITTING_DOWN and new_state not in [HexState.SITTING_IDLE, HexState.STANDING_UP]:
      return False
    if self.state == HexState.STANDING_UP and new_state not in [HexState.STANDING_IDLE, HexState.SITTING_DOWN]:
      return False
    if self.state == HexState.STANDING_IDLE and new_state not in [HexState.WALKING, HexState.ROTATING, HexState.SITTING_DOWN]:
      return False
    if self.state == HexState.WALKING and new_state not in [HexState.STANDING_IDLE]:
      return False
    if self.state == HexState.ROTATING and new_state not in [HexState.STANDING_IDLE]:
      return False
    return True
  
  def on_enter(self, state):
    pass

  def on_exit(self, state):
    pass

  def handle_sitting_idle(self, cmd):
    self.phase = 0
    if cmd.stand_pressed:
      self.set_state(HexState.STANDING_UP)

  def handle_sitting_down(self, cmd):
    if cmd.stand_pressed:
      self.set_state(HexState.STANDING_UP)

  def handle_standing_up(self, cmd):
    if cmd.sit_pressed:
      self.set_state(HexState.SITTING_DOWN)
    else:
      for leg in self.Legs:
        leg.set_position(120, 0, self.height)

  def handle_standing_idle(self, cmd):
    self.phase = 0
    if cmd.sit_pressed:
      self.set_state(HexState.SITTING_DOWN)
    elif cmd.move_x != 0 or cmd.move_y != 0:
      self.set_state(HexState.WALKING)
    elif cmd.rotate != 0:
      self.set_state(HexState.ROTATING)

  def handle_walking(self, cmd):
    pass

  def handle_rotating(self, cmd):
    pass

  def handle_state(self, cmd):
    if self.state == HexState.SITTING_IDLE:
      self.handle_sitting_idle(cmd)
    elif self.state == HexState.SITTING_DOWN:
      self.handle_sitting_down(cmd)
    elif self.state == HexState.STANDING_UP:
      self.handle_standing_up(cmd)
    elif self.state == HexState.STANDING_IDLE:
      self.handle_standing_idle(cmd)
    elif self.state == HexState.WALKING:
      self.handle_walking(cmd)
    elif self.state == HexState.ROTATING:
      self.handle_rotating(cmd)

  def update(self, cmd):
    self.handle_state(cmd)
    self.phase += self.phase_increment
    self.phase = self.phase % 1

  # x = out, y = side, z = height