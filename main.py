import numpy as np
import weakref
import math

G = 6.67408 * 10 ** (-11)   # This is the universal gravitational constant
timeLength = 10**1    # For more accurate results, smaller values must be chosen


class spaceObject:
    instances = []

    def __init__(self, name, position, mass, acceleration, velocity, radius):
        self.__class__.instances.append(weakref.proxy(self))
        self.name = name
        self.position = position
        self.mass = mass
        self.acceleration = acceleration
        self.velocity = velocity
        self.radius = radius


# Here our space objects are defined. Different names must be chosen!


a1 = spaceObject("a1", [0, 0, 0], 5.972 * 10**24, [0, 0, 0], [0, 0, 0], 6371000)
a2 = spaceObject("a2", [150.61 * 10**6.68, 0, 0], 1.989 * 10**30, [0, 0, 0], [0, 0, 0], 696340000)
#a3 = spaceObject("a3", [0, 3, 0], 200000, [0, 0, 0], [0, 0, 0], 0.2)


def getForce(an):
    # This function finds the net force on a spaceObject an

    force = np.array([0, 0, 0])
    distanceVector = ([0, 0, 0])
    for instance in spaceObject.instances:
        distanceVector = np.array(an.position) - np.array(instance.position)
        distancefigure = (distanceVector[0] ** 2) + (distanceVector[1]) ** 2 + (distanceVector[2] ** 2)
        if distancefigure != 0:
            figure1 = distanceVector * an.mass * G * instance.mass / distancefigure**3
            force = force - figure1
        # print(distanceVector)
        # print(distancefigure)
    # print("The net force on " + str(an.name) + " is " + str(force) + " Newton")
    return force


def getAcceleration(an):
    an.acceleration = getForce(an) / an.mass
    # print(an.name + " is accelerating with " + str(an.acceleration) + " meters per second^2")
    return an.acceleration

def getVelocity(an):
    an.velocity = an.velocity + an.acceleration * timeLength

def getPositionChange(an):
    acceleration = getAcceleration(an)
    velocity = np.array(an.velocity)
    positionfigure = timeLength * velocity
    positionChange = 1/2*acceleration*(timeLength)**2 + positionfigure
    getVelocity(an)
    return positionChange

def updatePosition(an):
    an.position = an.position + getPositionChange(an)
    print("The position of " + an.name + " is " + str(an.position) + "\n--------------\n")
    return an.position


maxTime = 140   # This should be chosen so that the spaceObjects are never at the same position vector (Trial and Error)
running = True
t = 0

while running:
    updatePosition(a1)
    updatePosition(a2)
    #updatePosition(a3)
    t = t + timeLength

    counter = 0

    for instance1 in spaceObject.instances:
        for instance2 in spaceObject.instances:
            distanceVector = np.array(instance1.position) - np.array(instance2.position)
            if instance1.name != instance2.name:
                distance = math.sqrt(distanceVector[0]**2 + distanceVector[1]**2 + distanceVector[2]**2)
                if distance<= (instance1.radius + instance2.radius):
                    running = False
                    counter = counter + 1
                    if counter != 1:
                        print(instance1.name + " " + instance2.name + " collided at:")
                        print(t)


