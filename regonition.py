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

# 获取图像
def getImage(IP, PORT, cameraID):
    camProxy = ALProxy("ALVideoDevice", IP, PORT)
    # vision_definitions.kCameraSelectID = vision_definitions.kBottomCamera ，以前的API写法，使用底部摄像头

    if (cameraID == 0):  # Bottom Camera
        camProxy.setCameraParameter("test", 18, 0)
    elif (cameraID == 1):  # Top Camera
        camProxy.setCameraParameter("test", 18, 1)

    resolution = vision_definitions.kVGA  # 定义resolution
    colorSpace = vision_definitions.kRGBColorSpace  # 定义色域
    fps = 15

    nameId = camProxy.subscribe("test", resolution, colorSpace, fps)  # 使用Borker订阅模块
    naoImage = camProxy.getImageRemote(nameId)  # 获取当前图片

    imageWidth = naoImage[0]
    imageHeight = naoImage[1]

    array = naoImage[6]
    im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

    im.save("D:\\camImage.png", "PNG")  # 临时图片路径
    camProxy.unsubscribe(nameId)
    def Binarization(image, pattern="yellow"):
    """
    Binarization()此方法是采用HSV色域进行二值化图像处理
    :param image:  传入的图像对象
    :param pattern: 需要识别的颜色，默认黄色
    :return:
    """
    # Setting the pattern
    lower = []
    upper = []
    if (pattern == "red"):
        lower = np.array([0, 120, 120])
        upper = np.array([10, 255, 255])
    elif (pattern == "yellow"):
        lower = np.array([20, 100, 100])
        upper = np.array([34, 255, 255])
    elif (pattern == "blue"):
        lower = np.array([110, 70, 70])
        upper = np.array([124, 255, 255])
    # BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Binarization
    mask = cv2.inRange(hsv, lower, upper)

    # Opened the image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)) #形态学基本structure
    opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) #开运算

    cv2.imshow("Binarization", opened)
    return opened


def calcTheLocate(img):
    """
    计算出图中目标中心的的相对坐标
    :param img: 传图图像对象
    :return:
    """
    col = np.ones(640)  # 采用Numpy创建全为1，长度为640的矩阵
    row = np.ones(480)  # 采用Numpy创建全为1，长度为480的矩阵
    colsum = []  # 存储每列的容器
    rowsum = []  # 存储每行的容器
    x = 0
    xw = 0 # w:west
    xe = 0 # e:est
    y = 0
    yn = 0 #n:north
    ys = 0 #s:south
    for i in range(0, 480):  # 遍历每行
        product = np.dot(col, img[i][:])  # 点乘
        colsum.append(product)
    for i in range(0, 480):  # 计算出坐标
        if (colsum[i] == max(colsum)):
            y = i
            val = max(colsum) / 255
            yn = i - val
            ys = i + val
            break
    for i in range(0, 640):
        product = np.dot(row, img[:, i])
        rowsum.append(product)
    for i in range(0, 640):
        if (rowsum[i] == max(rowsum)):
            x = i
            val = max(colsum) / 255
            xw = val - i
            xe = val + i
            break
    print("locate  x: ", x, xw, xe, "........ locate y :", y, yn, ys)

    #画出轮廓
    cv2.circle(img, (x, y), 5, (55, 255, 155), -1)
    cv2.circle(img, (xw, y), 5, (55, 255, 155), -1)
    cv2.circle(img, (xe, y), 5, (55, 255, 155), -1)
    cv2.circle(img, (x, yn), 5, (55, 255, 155), -1)
    cv2.circle(img, (x, ys), 5, (55, 255, 155), -1)
    cv2.putText(img, "center", (x - 20, y - 20),
     cv2.FONT_HERSHEY_SIMPLEX, 0.75, (55, 255, 155), 2)

    cv2.imshow("two", img)
    cv2.waitKey(0)
    return x, y


def getDistanse(x, y, cameraID):
    """
    计算出摄像头在空间中距离目标点的直线距离
    :param x: x坐标
    :param y: y坐标
    :param cameraID:
    :return:
    """
    x = x - 320
    y = y - 240
    alpha = ((-x / 640) * 60.97) * math.pi / 180  # rads
    beta = ((y / 480) * 47.64) * math.pi / 180  # rads
    headAngle = getHeadAngle(IP, PORT)
    # alpha = alpha + headAngle[0]
    beta = beta + headAngle[1]

    print("alpha", alpha, "beta", beta)
    print("alpha", alpha / math.pi * 180, "beta", beta / math.pi * 180)

    setHeadAngle(alpha, beta)
    motionProxy.setStiffnesses("Head", 0.0)
    #  摄像头高度
    H = 495
    cameraAngle = 1.2 * math.pi / 180
    if cameraID == 0:
        H = 495
        cameraAngle = 1.2 * math.pi / 180
    elif cameraID == 1:
        H = 477.33
        cameraAngle = 39.7 * math.pi / 180

    h = H - 210 - 105 / 2  ################## the height and the diam
    headPitchAngle = getHeadPitchAngle(IP, PORT)
    # s = (h-100)/math.tan(cameraAngle + headPitchAngle[0])
    s = h / math.tan(cameraAngle + headPitchAngle[0])
    # s = h/math.tan(cameraAngle +beta)
    x = s * math.cos(alpha) / 1000
    y = s * math.sin(alpha) / 1000

    return x, y, alpha


def getDistanceBottom(x, y):
    x = x - 320
    y = y - 240
    alpha = ((-x / 640) * 60.97) * math.pi / 180  # rads
    beta = ((y / 480) * 47.64) * math.pi / 180  # rads
    headAngle = getHeadAngle(IP, PORT)
    alpha = alpha + headAngle[0]
    beta = beta + headAngle[1]
    setHeadAngle(alpha, beta)
    motionProxy.setStiffnesses("Head", 0.0)

    print("Use bottom camera : ")
    print("alpha", alpha, "beta", beta)
    print("alpha", alpha / math.pi * 180, "beta", beta / math.pi * 180)

    H = 477.33  # Not sure
    cameraAngle = 39.7 * math.pi / 180
    h = H - 210 - 105 / 2
    s = h / math.tan(cameraAngle + beta)
    x = s * math.cos(alpha) / 1000
    y = s * math.sin(alpha) / 1000
    z = 210 + 105 / 2
    return x, y, z
    
    
