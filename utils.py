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


IP = "192.168.3.8"  # ROBOT IP
PORT = 9559  # 端口
motionProxy = ALProxy("ALMotion", IP, PORT)

#取得头部偏角
def getHeadAngle(IP, PORT):
    # motionProxy = ALProxy("ALMotion",IP,PORT)
    actuator = ["HeadYaw", "HeadPitch"]
    useSensor = False
    headAngle = motionProxy.getAngles(actuator, useSensor)

    return headAngle

#Pitch关节角
def getHeadPitchAngle(IP, PORT):
    # motionProxy = ALProxy("ALMotion",IP,PORT)
    actuator = "HeadPitch"
    useSensor = False
    headAngle = motionProxy.getAngles(actuator, useSensor)

    return headAngle


def setHeadAngle(alpha, beta):
    # motionProxy = ALProxy("ALMotion", IP, PORT)
    motionProxy.setStiffnesses("Head", 1.0)
    maxSpeedFraction = 0.3
    names = ["HeadYaw", "HeadPitch"]
    angles = [alpha, beta]
    motionProxy.angleInterpolationWithSpeed(names, angles, maxSpeedFraction)

    motionProxy.setStiffnesses("Head", 0.0)
