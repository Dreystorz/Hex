import numpy as np

def getPath(start, end, step, height=0):
    if(height != 0):
        return getCurvedPath(start, end, step, height)
    start = np.array(start)
    end = np.array(end)
    direction = end - start
    distance = np.linalg.norm(direction)
    direction = direction / distance  # Normalize the direction vector

    num_steps = int(np.floor(distance / step))
    points = [start + i * step * direction for i in range(num_steps + 1)]

    if not np.allclose(points[-1], end):  # Add the endpoint if it's not already included
        points.append(end)
    return points

##ChatGPT
def bezier_quadratic(P0, P1, P2, steps):
    points = []
    for t in np.linspace(0, 1, steps):
        point = (1 - t)**2 * P0 + 2 * (1 - t) * t * P1 + t**2 * P2
        points.append(point)
    return points

    
##ChatGPT
def getCurvedPath(start, end, step, height):
    temp = getPath(start, end, step)
    start = np.array(start)
    end = np.array(end)
    control = np.array(tuple((a + b) / 2 for a, b in zip(start, end)))
    control[2] = control[2]+(height*2)
    return bezier_quadratic(start, control, end, len(temp)-1)