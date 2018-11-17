if __name__ == '__main__':

    setHeadAngle(0, 0.25)
    motionProxy.setStiffnesses("Head", 0.0)
    getImage(IP, PORT, 1)
    img = cv2.imread("D:\\camImage.png")

    af = Binarization(img, "yellow")
    x, y = calcTheLocate(af)
    print("final locate : ", x, y)
    flag = None
    if (x == 0 and y == 0):
        flag = False
    else:
        flag = True

    while (flag == False):
        motionProxy.moveTo(-0.1, 0.1, math.pi / 3)
        flag = search()
        if (flag == False):
            motionProxy.moveTo(-0.1, 0.1, math.pi / 3)
            flag = search()
        else:
            flag = True
            break
    af = Binarization(img, "yellow")
    x, y = calcTheLocate(af)
    x, y, theta = getDistanse(x, y, 0)
    print("walk 0:", x, y, theta)
    # print("walk 1:",x,y-y*math.tan(math.radians(25)),theta)
    # motionProxy.walkTo(x-0.130,y,theta)
    moveConfig = [["MaxStepFrequency", 1.0]]
    motionProxy.moveTo(x - 0.11, y - (x - 0.11) * math.tan(math.radians(12)), theta, moveConfig)
    getImage(IP, PORT, 0)
    img = cv2.imread("D:\\camImage.png")
    af = Binarization(img, "yellow")
    x, y = calcTheLocate(af)

    print("walk 1:", x, y, theta)
    motionProxy.walkTo(x - 0.1, y, theta)
    ###pick up the ball
    cartesion()
    motionProxy.setMoveArmsEnabled(False, False)
    # back
    motionProxy.moveTo(0.3, 0, 0)
    markId = None
    # markId = getMarkId(motionProxy)
    while True:
        if markId == None:
            markId = searchLandmark(motionProxy)
        else:
            break

    landmark()
    motionProxy.rest()
