from controller import Robot
import math
import struct

timeStep = 32
max_velocity = 6.28

robot = Robot()

wheel_left = robot.getMotor("left wheel motor")
wheel_right = robot.getMotor("right wheel motor")

leftSensors = []
rightSensors = []
frontSensors = []

frontSensors.append(robot.getDistanceSensor("ps7"))
frontSensors[0].enable(timeStep)
frontSensors.append(robot.getDistanceSensor("ps0"))
frontSensors[1].enable(timeStep)

rightSensors.append(robot.getDistanceSensor("ps1"))
rightSensors[0].enable(timeStep)
rightSensors.append(robot.getDistanceSensor("ps2"))
rightSensors[1].enable(timeStep)

leftSensors.append(robot.getDistanceSensor("ps5"))
leftSensors[0].enable(timeStep)
leftSensors.append(robot.getDistanceSensor("ps6"))
leftSensors[1].enable(timeStep)

camera = robot.getCamera("camera")
camera.enable(timeStep)
camera.recognitionEnable(timeStep)

wheel_left.setPosition(float("inf"))
wheel_right.setPosition(float("inf"))

def turn_right():
    setVel(0.6, -0.2)

def turn_left():
    setVel(-0.2, 0.6)

def spin():
    setVel(0.6, -0.6)

def setVel(vl, vr):
    wheel_left.setVelocity(vl*max_velocity)
    wheel_right.setVelocity(vr*max_velocity)

def nearObject(position):
    return math.sqrt((position[0] ** 2) + (position[2] ** 2)) < 0.10

def getVisibleVictims():
    #get all objects the camera can see
    objects = camera.getRecognitionObjects()
    victims = []

    for item in objects:
        if item.get_colors() == [1,1,1]:
            victim_pos = item.get_position()
            victims.append(victim_pos)

    return victims

while robot.step(timeStep) != -1:
    setVel(1,1)
    for i in range(2):
        #for sensors on the left, either
        if leftSensors[i].getValue() > 80:
            turn_right()
        #for sensors on the right, either
        elif rightSensors[i].getValue() > 80:
            turn_left()
    
    #for both front sensors
    if frontSensors[0].getValue() > 80 and frontSensors[1].getValue() > 80:
        spin()

    print(getVisibleVictims())