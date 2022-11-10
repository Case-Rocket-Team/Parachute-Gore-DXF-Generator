# Parachute Gore DXF Generator
# Copyright © 2022 Eabha Abramson
# functions.py - Contains utility functions ranging from a distance function to a DXF write function

from math import asin, pi, sin, cos, atan, sqrt, pow
from typing import SupportsFloat
import ezdxf
import platform
from numpy import array, ndarray

def dist(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calcuates the distance between two points with coordinates (x1, y1) and (x2, y2)."""
    return sqrt(pow(x2-x1,2) + pow(y2-y1,2))

def loc(a: float, b: float, theta: float) -> float:
    """Calculates the length of the third side of a triangle given the first two sides and the angle between them (measured in radians). Uses the law of cosines."""
    return sqrt(pow(a,2) + pow(b,2) - 2*a*b*cos(theta))

def sign(x: SupportsFloat) -> int:
    """Returns 1 for positive numbers, 0 for 0, and -1 for negative numbers."""
    if x == 0:
        return 0
    else:
        return 1 if x > 0 else -1

def sec(x: SupportsFloat) -> float:
    """Calculates the secant of x (measured in radians)."""
    return pow(cos(x), -1)

def ellipsoidalPointList(d: float, r: float, hole: float) -> ndarray[float, float]:
    """Returns a list of points taken from the intersection of the first quadrant of the x-y plane and the surface of an ellipsoidal parachute with the given parameters. For the purposes of this function, the y axis is located vertically along the center of the chute and the x axis lies horizontally and intersects the bottom edge of the chute."""
    num_pts = int(d * 5)
    ellipse_profile = array([])
    ellipse_profile.resize(num_pts+1, 2, refcheck=False)
    i = 0
    while i < num_pts + 1 and (i == 0 or ellipse_profile[i-1,0] > hole/2):
        t = 0.5 * pi * (i / num_pts)
        ellipse_profile[i,:] = [d / 2 * cos(t), d / 2 * r * sin(t)]
        i += 1
    ellipse_profile.resize(i, 2)
    return ellipse_profile

def toroidalPointList(d1: float, d2: float, R: float, h: float) -> ndarray[float, float]:
    """Returns a list of points taken from the intersection of the first quadrant of the x-y plane and the surface of an toroidal parachute with the given parameters. For the purposes of this function, the y axis is located vertically along the center of the chute and the x axis lies horizontally and intersects the bottom edge of the chute."""
    num_pts = int(d1 * 10)
    torus_profile = array([])
    torus_profile.resize(num_pts+1, 2, refcheck=False)
    phi = asin(1 - h)
    a = (d1 - d2) / (2 * (1 + cos(phi)))
    r = (d2 / 2) + (a * cos(phi))
    i = 0
    while i < num_pts + 1 and (i == 0 or torus_profile[i-1,0] > d2 / 2):
        t = pi * (i / num_pts)
        torus_profile[i,:] = [r + a * cos(t), R * a * sin(t)]
        i += 1
    torus_profile.resize(i,2)
    return torus_profile

def goreProfile(point_list: ndarray[float, float], n: int, model: int) -> ndarray[float, float]:
    """Returns a set of points along the outer edge of a gore for a parachute with n gores, when given the profile of one edge of the gore."""
    num_pts = len(point_list)
    angle = 2 * pi / n
    gore_edge_profile = array([])
    gore_edge_profile.resize(len(point_list), 2, refcheck=False)
    if model == 0:
        gore_edge_profile[0,:] = [loc(point_list[0,0], point_list[0,0], angle) / 2, point_list[0,1]]
    else:
        gore_edge_profile[0,:] = [point_list[0,0] * angle / 2, point_list[0,1]]
    for i in range(1,num_pts):
        x_last = point_list[i-1,0]
        y_last = point_list[i-1,1]
        x = point_list[i,0]
        y = point_list[i,1]
        x_next = 0
        if model == 0:
            x_next = loc(x, x, angle) / 2
        else:
            x_next = x * angle / 2
        dx = x_next - gore_edge_profile[i-1][0]
        y_next = gore_edge_profile[i-1][1] + sqrt(pow(x-x_last,2) + pow(y-y_last,2) - pow(dx,2))
        gore_edge_profile[i,:] = [x_next, y_next]
    l = num_pts * 2
    gore_profile = array([])
    gore_profile.resize(l, 2, refcheck=False)
    for i in range(num_pts):
        gore_profile[i,:] = [-gore_edge_profile[i,0], gore_edge_profile[i,1]]
    for i in range(num_pts):
        gore_profile[num_pts+i,:] = gore_edge_profile[-1-i,:]
    return gore_profile

def offset(point_list: ndarray[float, float], offset: int) -> ndarray[float, float]:
    """Takes a list of points describing the outer edges of a parachute gore offsets each line outward by the given amount. Returns the new, offset list of points. Relies on the assumption that the x values of the points are always increasing."""
    offset_list = array([])
    offset_list.resize(len(point_list), 2, refcheck=False)
    # Offset the bottom right point. Uses a for loop so all the variables are local
    for i in range(-1, 0):
        x_last = point_list[i-1,0]
        y_last = point_list[i-1,1]
        x = point_list[i,0]
        y = point_list[i,1]
        x_next = point_list[i+1,0]
        y_next = point_list[i+1,1]
        if x == x_last:
            slope1 = 0
        else:
            slope1 = (y - y_last)/(x - x_last)
        if x == x_next:
            slope2 = 0
        else:
            slope2 = (y_next - y)/(x_next - x)
        theta1 = atan(slope1)
        theta2 = atan(slope2)
        dtheta = theta1 - theta2
        mag = offset * sec(dtheta/2)
        dir = (theta1 + theta2) / 2
        offset_list[i,:] = [x + mag * cos(dir), y + mag * sin(dir)]
    # Offset the bottom left point. Uses a for loop so all the variables are local
    for i in range(0, 1):
        x_last = point_list[i-1,0]
        y_last = point_list[i-1,1]
        x = point_list[i,0]
        y = point_list[i,1]
        x_next = point_list[i+1,0]
        y_next = point_list[i+1,1]
        if x == x_last:
            slope1 = 0
        else:
            slope1 = (y - y_last)/(x - x_last)
        if x == x_next:
            slope2 = 0
        else:
            slope2 = (y_next - y)/(x_next - x)
        theta1 = atan(slope1)
        theta2 = atan(slope2)
        dtheta = theta1 - theta2
        mag = offset * sec(dtheta/2)
        dir = pi + (theta1 + theta2) / 2
        offset_list[i,:] = [x + mag * cos(dir), y + mag * sin(dir)]
    # Offset the rest of the points
    for i in range(1, len(point_list) - 1):
        x_last = point_list[i-1,0]
        y_last = point_list[i-1,1]
        x = point_list[i,0]
        y = point_list[i,1]
        x_next = point_list[i+1,0]
        y_next = point_list[i+1,1]
        if x == x_last:
            slope1 = 0
        else:
            slope1 = (y - y_last)/(x - x_last)
        if x == x_next:
            slope2 = 0
        else:
            slope2 = (y_next - y)/(x_next - x)
        theta1 = atan(slope1)
        theta2 = atan(slope2)
        dtheta = theta1 - theta2
        mag = offset * sec(dtheta/2)
        dir = theta1 + pi/2 - dtheta/2
        offset_list[i,:] = [x + mag * cos(dir), y + mag * sin(dir)]
    return offset_list

def getDXF(point_list: ndarray, folder: str, output: str, units: int) -> None:
    """Takes a list of points and creates a DXF file of the lines connecting the points in the order of the list, icluding connecting the last point to the first. Saves the DXF file with the given output name in the given folder. The document units are set according to the value given."""
    doc = ezdxf.new()
    doc.units = units
    msp = doc.modelspace()
    layer = doc.layers.new(name="Layer 1", dxfattribs={"linetype": "CONTINUOUS", "color": 7, "lineweight": 0})
    for i in range(len(point_list)):
        msp.add_line((point_list[i-1,0], point_list[i-1,1]), (point_list[i,0], point_list[i,1]), dxfattribs={"layer": "Layer 1"})
    if folder == "":
        doc.saveas(output)
    else:
        if platform.system() == "Windows":
            doc.saveas(folder + "\\" + output)
        else:
            doc.saveas(folder + "/" + output)
