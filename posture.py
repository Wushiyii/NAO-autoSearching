# encoding=utf-8
from __future__ import division
from naoqi import ALProxy
from PIL import Image
import motion
import cv2
import math
import vision_definitions
import numpy as np
import almath

names = list()
times = list()
keys = list()

IP = "192.168.3.8"  # ROBOT IP
PORT = 9559  # 端口
motionProxy = ALProxy("ALMotion", IP, PORT)

#设定头部位姿
def head(motionProxy):
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.96, 3.92, 5.96])
    keys.append([0.261799, 0.274544, 0.269942])

    names.append("HeadYaw")
    times.append([1.96, 3.92, 5.96])
    keys.append([0.387463, -0.659662, -0.0123138])

    motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.angleInterpolation(names, keys, times, True)


#搜索landmark
def searchLandmark(motionProxy):
    motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.moveTo(-0.1, 0.1, math.pi / 2)
    head(motionProxy)
    print("search.........")
    markId = getMarkId()
    return markId


def landmark():
    # Set here your robto's ip.
    ip = "192.168.3.8"
    # Set here the size of the landmark in meters.
    landmarkTheoreticalSize = 0.06  # in meters
    # Set here the current camera ("CameraTop" or "CameraBottom").
    currentCamera = "CameraTop"

    memoryProxy = ALProxy("ALMemory", ip, 9559)
    landmarkProxy = ALProxy("ALLandMarkDetection", ip, 9559)

    motionProxy.setMoveArmsEnabled(False, False)

    # Subscribe to LandmarkDetected event from ALLandMarkDetection proxy.
    landmarkProxy.subscribe("landmarkTest")

    # Wait for a mark to be detected.
    markData = memoryProxy.getData("LandmarkDetected")
    while (markData is None or len(markData) == 0):
        markData = memoryProxy.getData("LandmarkDetected")

    # Retrieve landmark center position in radians.

    #####################
    markInfoArray = markData[1]
    for markInfo in markInfoArray:
        markShapeInfo = markInfo[0]
        markExtraInfo = markInfo[1]
        alpha = markShapeInfo[1]
        beta = markShapeInfo[2]
        print "mark  ID: %d" % (markExtraInfo[0])
        print "  alpha %.3f - beta %.3f" % (markShapeInfo[1], markShapeInfo[2])
        print "  width %.3f - height %.3f" % (markShapeInfo[3], markShapeInfo[4])

    ############
    wzCamera = markData[1][0][0][1]
    wyCamera = markData[1][0][0][2]

    # Retrieve landmark angular size in radians.
    angularSize = markData[1][0][0][3]

    # Compute distance to landmark.
    distanceFromCameraToLandmark = landmarkTheoreticalSize / (2 * math.tan(angularSize / 2))

    # Get current camera position in NAO space.
    transform = motionProxy.getTransform(currentCamera, 2, True)
    transformList = almath.vectorFloat(transform)
    robotToCamera = almath.Transform(transformList)

    # Compute the rotation to point towards the landmark.
    cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, wyCamera, wzCamera)

    # Compute the translation to reach the landmark.
    cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)

    # Combine all transformations to get the landmark position in NAO space.
    robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform * cameraToLandmarkTranslationTransform

    print "x " + str(robotToLandmark.r1_c4) + " (in meters)"
    print "y " + str(robotToLandmark.r2_c4) + " (in meters)"
    print "z " + str(robotToLandmark.r3_c4) + " (in meters)"

    x = float(robotToLandmark.r1_c4)
    y = float(robotToLandmark.r2_c4)
    z = float(robotToLandmark.r3_c4)
    print(x, y)
    # print("xxxxxxxxxxxxxxxxxxxxx")
    # print math.sqrt(1 - (math.cos(alpha))**2 + (math.cos(beta))**2)
    # theta = math.acos(math.sqrt(1 - (math.cos(alpha))**2 - (math.cos(beta))**2))
    theta = math.atan(y / x)

    motionProxy.moveTo(x, y, theta)
    # motionProxy.moveTo(x, y, theta)

    landmarkProxy.unsubscribe("landmarkTest")


def getMarkId():
    # Set here your robto's ip.
    ip = "192.168.3.8"
    # Set here the size of the landmark in meters.
    # landmarkTheoreticalSize = 0.06  # in meters
    # Set here the current camera ("CameraTop" or "CameraBottom").
    # currentCamera = "CameraTop"

    memoryProxy = ALProxy("ALMemory", ip, 9559)
    landmarkProxy = ALProxy("ALLandMarkDetection", ip, 9559)

    # Subscribe to LandmarkDetected event from ALLandMarkDetection proxy.
    landmarkProxy.subscribe("landmarkTest")
    markId = None
    # Wait for a mark to be detected.
    markData = memoryProxy.getData("LandmarkDetected")
    # while (markData is None or len(markData) == 0):
    markData = memoryProxy.getData("LandmarkDetected")
    if (markData is None or len(markData) == 0):
        markId = None
    else:
        markInfoArray = markData[1]
        for markInfo in markInfoArray:
            markShapeInfo = markInfo[0]
            markExtraInfo = markInfo[1]
            alpha = markShapeInfo[1]
            beta = markShapeInfo[2]
            print "mark  ID: %d" % (markExtraInfo[0])
            markId = markExtraInfo[0]

    return markId


# ('lwx : ', -1.627792477607727, 'lwy : ', 0.47067877650260925, 'lwz : ', -0.4202498197555542)
# ('rwx : ', 1.8139231204986572, 'rwy : ', 0.49902573227882385, 'rwz : ', 0.371066689491272)
def cartesion():
    chainName = "LArm"
    frame = motion.FRAME_ROBOT
    useSensor = False
    # Get the current position of the chainName in the same frame
    current = motionProxy.getPosition(chainName, frame, useSensor)
    target = [
        current[0],
        current[1],
        current[2],
        current[3] - 1.62779,
        current[4] + 0.47067,
        current[5] - 0.42024]
    fractionMaxSpeed = 0.5
    axisMask = motion.AXIS_MASK_VEL  # just control position
    motionProxy.setPositions(chainName, frame, target, fractionMaxSpeed, axisMask)

    motionProxy.getPosition()
