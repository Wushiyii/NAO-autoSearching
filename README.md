# NAO-autoSearching
It's a object recognition algorithm based on NAO robot by using naoqi、OpenCv、Numpy、matplotlib etc.. 

### Intro

It's a robotic searching and recognition algorithn by Python.And it's mainly based on OpenCV、Naoqi、Numpy、PIL module.

#### The process :
Open the robot's head camera --> Get image -->  Binary image  --> Morphology -->  Get 2D locate --> Transform to 3D locate --> Go to the target  --> Pick it --> Go to  another target position --> Drop it 

#### The process's detail :
The process has many part:
* Adjusting NAO robot, preparing for getting the image.
Open the robot's camera ,using naoqi to get the image, get robot's current parameter likes head angle or pitch angle.
* Recognition ... 
Binary the image to a two color image by HSV color space which in the  opencv library.After that , using numpy or something like matrix calculator to calculate the image's location.Finally ,transform the 2D location to a absolutely distance by the principle of ranging(it's not so accurate because the robot's move can change itself's parameter).
* Moving 
  After getting the distance between robot and the target,using the 3D measure algorithm to transfer  it to 3D locate which needs many joint's parameter.
* Picking and Dropping
How to control the hand to the target? I use the Cartesian algorithm to handle it. (The algo is based on the dynamic 3D robotic model which provide a Array contains six angel.)

#### The result:
- Original image
<img  src="https://s1.ax1x.com/2018/11/28/FZnN5Q.png" width="400" height="310" />
- After HSV binary:
<img  src="https://s1.ax1x.com/2018/11/18/izofDU.png"  width="400" height="310" />
- After Morphology :
<img  src="https://s1.ax1x.com/2018/11/28/FZnRPJ.png"  width="400" height="310" />
- Calculate the locate:
<img  src="https://s1.ax1x.com/2018/11/18/izohbF.png"  width="400" height="310" />
- Another image to calculate the locate:
<img  src="https://s1.ax1x.com/2018/11/18/izoIUJ.png"  width="400" height="310" />
- Get the center :
<img  src="https://s1.ax1x.com/2018/11/18/izoWuT.png"  width="400" height="310" />
- Using the bottom camera:
<img  src="https://s1.ax1x.com/2018/11/28/FZntUg.png"  />
- Do it selt:
<img  src="https://s1.ax1x.com/2018/11/29/FZKoND.gif"  />
