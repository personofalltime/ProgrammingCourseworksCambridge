import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time

global dp, dtw, dt, dl, phi, z, wheelspacing
dp, dtw, dt, dl = 8,4,9,8
wheelspacing = 10

z = np.sqrt(dt*dt+dl*dl)
phi = np.atan(dt/dl)

global currentpos, turnpower, turnmultiplier
currentpos = 0

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

def calculate_rd_from_rm(rm):
    theta = calctheta(rm)
    rd = calcRd(calcX(theta), calcY(theta, rm))
    return rd

def findcircle(triplet):
    if(len(triplet) < 3):
        return (0, 0, 0)
    if(triplet[1] == True) or (triplet[1] == False):
        rad = np.sqrt(triplet[0][3]**2 + triplet[0][4]**2)
        return (rad, triplet[0][1], triplet[0][1])

def calcradius(triplet):
    # [(a, b), (c, d), (e, f)]

    c = np.sqrt((triplet[-1][1]-triplet[0][1])**2 + (triplet[-1][0]-triplet[0][0])**2 )
    a = np.sqrt((triplet[1][1]-triplet[0][1])**2 + (triplet[1][0]-triplet[0][0])**2 )
    b = np.sqrt((triplet[-1][1]-triplet[1][1])**2 + (triplet[-1][0]-triplet[1][0])**2 )

    x = np.acos((a**2 + b**2 - c**2)/(2*a*b))

    radius = np.sqrt((c**2)/(2-(2*np.cos(2*np.pi - 2*x))))

    theta1 = np.acos((c)/(2*radius))
    theta2 = np.atan((triplet[-1][1]-triplet[0][1])/(triplet[-1][0]-triplet[0][0]))

    x = triplet[0][0] + np.cos(theta2-theta1)*radius
    y = triplet[0][1] + np.sin(theta2-theta1)*radius

    return (radius, x, y, np.pi-2*theta1)

def findturnthroughangle(desiredangle):
    
    change = currentpos-desiredangle

    if(change < -(np.pi/2)):
       return 2*np.pi + change
    elif(change > np.pi/2):
        return -(2*np.pi-change)
    else:
        return change

def movetoangle(desiredangle, left):
    if(left):
        #motorB.turn(power=turnpower, brake=true)
        #motorA.turn(power=-turnpower, brake=true)
        time.sleep((turnmultiplier*turnpower)/((findturnthroughangle(desiredangle))*(wheelspacing/2)))
        #motorA.turn(power=0)
        #motorB.turn(power=0)
    else:
        #motorA.turn(power=turnpower, brake=true)
        #motorB.turn(power=-turnpower, brake=true)
        time.sleep((turnmultiplier*turnpower)/((findturnthroughangle(desiredangle))*(wheelspacing/2)))
        #motorA.turn(power=0)
        #motorB.turn(power=0)


def correctforquadrant(x, y):
    if(x >= 0) and (y>=0):
        return np.atan(x/y)
    elif(x > 0) and (y<=0):
        return np.atan(y/x) + np.pi/2
    elif(x < 0) and (y>= 0):
        return np.atan(y/-x) + 1.5*np.pi
    elif(x <= 0) and (y<0):
        return np.atan(x/y) + np.pi
    
def moveincircle(radius, x, y, angle):

    movetoangle(correctforquadrant(x, y), True if (y > 0) else False)
    drawCircle(radius, angle, True if (y > 0) else False)


def drawCircle(rad, angle, left):

    rm = 10
    rd = 0
    while rd < rad:
    
        rd = calculate_rd_from_rm(rm)                         
        rm = rm + 0.1

    ratio = (rm+(wheelspacing/2))/(rm-(wheelspacing/2))

    if(left):
        motR.turn(turnpower)
        motL.turn(ratio*turnpower)
    else:
        motR.turn(ratio*turnpower)
        motL.turn(turnpower)


#rm = np.linspace(0, 100, 10000)
#plt.plot(rm, calculate_ratio_from_rm(rm))
#plt.show()

with open("/home/datis/Documents/ProgrammingCourseworksCambridge/1A/1CW: Lego/placeholder.gcode") as f:
    allCodes = f.readlines()

tmp3 = []
count = 0

arcSets = []

for i in range(0, len(allCodes)):

    curr = allCodes[i]
    curr = curr.replace("\n", "").split(" ")

    if(curr[0] == "G0") or (curr[0] == "G1"):
        tmp3.append((float(curr[1][1:len(curr[1])]), float(curr[2][1:len(curr[1])])))
        count += 1

    if(count == 3) or i == len(allCodes)-1:
        arcSets.append(tmp3)
        count = 1
        tmp = tmp3[-1]
        tmp3 = []
        tmp3.append(tmp)

print(arcSets)
for i in arcSets:
    print(calcradius(i))

[0, 1, 2, 3, 4]