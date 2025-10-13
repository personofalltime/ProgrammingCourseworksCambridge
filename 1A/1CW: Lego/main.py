import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

global dp, dtw, dt, dl, phi, z, wheelspacing
dp, dtw, dt, dl = 8,4,9,8
wheelspacing = 10

z = np.sqrt(dt*dt+dl*dl)
phi = np.atan(dt/dl)

def calctheta(rm):
    theta = math.pi - np.atan(rm/dp) - np.acos(dtw/np.sqrt((rm*rm) + (dp*dp)))
    return theta

def calcX(theta):
    x = dp + dtw*np.cos(theta) + z*np.cos(phi-theta)
    return x

def calcY(theta, rm):
    y = rm - dtw*np.sin(theta) + z*np.sin(phi-theta)
    return y

def calcRd(x, y):
    return np.sqrt((x*x)+(y*y))

def calculate_ratio_from_rm(rm):
    theta = calctheta(rm)
    rd = calcRd(calcX(theta), calcY(theta, rm))
    ratio = (rm+(wheelspacing/2))/(rm-(wheelspacing/2))
    return ratio

def findcircle(triplet):
    if(triplet[1] == True) or (triplet[1] == False):
        rad = np.sqrt(triplet[0][3]**2 + triplet[0][4]**2)
        return (triplet[0][1], triplet[0][1], rad)

rm = np.linspace(0, 100, 10000)
plt.plot(rm, calculate_ratio_from_rm(rm))
plt.show()

with open("placeholder.gcode") as f:
    allCodes = f.readlines()


tmp3 = []
count = 0

arcSets = []

for i in range(0, math.floor(len(allCodes))):

    curr = allCodes[i].split(" ")

    if(count == 3):
        arcSets.append(tmp3)
        count = 0
        tmp3 = []

    if(curr[0] == "G0") or (curr[0] == "G1"):
        tmp3.append(curr)
        count += 1
    elif(curr[0] == "G2"):
        arcSets.append(tmp3)
        count = 0
        tmp3 = []
        arcSets.append([curr, False]) #False means that it is clockwise
    elif(curr[0] == "G1"):
        arcSets.append(tmp3)
        count = 0
        tmp3 = []
        arcSets.append([curr, True]) #True means that it is counter-clockwise
    





[0, 1, 2, 3, 4]