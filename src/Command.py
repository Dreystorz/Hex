MAX_X = 8
MAX_Y = 8
MIN_X = -8
MIN_Y = -8

class Command:
  def __init__(self):
    self.move_x = 0
    self.move_y = 0
    self.rotate = 0
    self.height = 0
    self.stand_pressed = False
    self.sit_pressed = False

  def print(self):
    print(f"Move X: {self.move_x}, Move Y: {self.move_y}, Rotate: {self.rotate}, Height: {self.height}, Stand: {self.stand_pressed}, Sit: {self.sit_pressed}")

  def read_controller_input(self, raw_x, raw_y, rotate, height_change, sit, stand):
    # Parse the raw command and update the command attributes
    self.move_x = apply_deadzone(smooth(self.move_x, remap(raw_x, 0, 255, MIN_X, MAX_X), alpha=0.15))
    self.move_y = apply_deadzone(smooth(self.move_y, remap(raw_y, 255, 0, MIN_Y, MAX_Y), alpha=0.15))
    self.height = -height_change
    self.stand_pressed = stand
    self.sit_pressed = sit

def smooth(current, target, alpha=0.15):
  return current + (target - current) * alpha
  
def apply_deadzone(value):
  if(abs(value) < 1):
    return 0
  return value

def remap(value, in_min, in_max, out_min, out_max):
  return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min