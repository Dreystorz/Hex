import numpy as np

def bezier_quadratic(P0, P1, P2, steps):
    points = []
    for t in np.linspace(0, 1, steps):
        point = (1 - t)**2 * P0 + 2 * (1 - t) * t * P1 + t**2 * P2
        points.append(point)
    return points

# Define 3 control points in 3D
P0 = np.array([0, 0, 0])     # Start point
P1 = np.array([5, 10, 0])    # Control point (determines curve)
P2 = np.array([10, 0, 0])    # End point

# Get points along the curve
curve_points = bezier_quadratic(P0, P1, P2, steps=20)

# Print only the x-coordinates
for p in curve_points:
    print(p[0])
