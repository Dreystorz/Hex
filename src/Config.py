OFFSET_OUT = 200
FRONTBACK_OFFSET = 80

LEG_CONFIG = {
  "LEFT_FRONT": {
    "COXA": {"dir": -1, "offset":-55},
    "FEMUR": {"dir": -1, "offset": 90},
    "TIBIA": {"dir": 1, "offset": 0},
    "HOME_POSITION": [-50+OFFSET_OUT, -FRONTBACK_OFFSET, 0],
    "XYZ_DIRECTION": [1,1,1]
  },
  "LEFT_MIDDLE": {
    "COXA": {"dir": -1, "offset": 0},
    "FEMUR": {"dir": -1, "offset": 90},
    "TIBIA": {"dir": 1, "offset": 0},
    "HOME_POSITION": [OFFSET_OUT, 0, 0],
    "XYZ_DIRECTION": [1,1,1]
  },
  "LEFT_BACK": {
    "COXA": {"dir": -1, "offset": 55},
    "FEMUR": {"dir": -1, "offset": 90},
    "TIBIA": {"dir": 1, "offset": 0},
    "HOME_POSITION": [-50+OFFSET_OUT, FRONTBACK_OFFSET, 0],
    "XYZ_DIRECTION": [1,1,1]
  },
  "RIGHT_FRONT": {
    "COXA": {"dir": 1, "offset": 125},
    "FEMUR": {"dir": 1, "offset": 90},
    "TIBIA": {"dir": -1, "offset": 180},
    "HOME_POSITION": [-50+OFFSET_OUT, FRONTBACK_OFFSET, 0],
    "XYZ_DIRECTION": [-1,1,1]
  },
  "RIGHT_MIDDLE": {
    "COXA": {"dir": 1, "offset": 180},
    "FEMUR": {"dir": 1, "offset": 90},
    "TIBIA": {"dir": -1, "offset": 180},
    "HOME_POSITION": [OFFSET_OUT, 0, 0],
    "XYZ_DIRECTION": [-1,1,1]
  },
  "RIGHT_BACK": {
    "COXA": {"dir": 1, "offset": 235},
    "FEMUR": {"dir": 1, "offset": 90},
    "TIBIA": {"dir": -1, "offset": 180},
    "HOME_POSITION": [-50+OFFSET_OUT, -FRONTBACK_OFFSET, 0],
    "XYZ_DIRECTION": [-1,1,1]
  }
}