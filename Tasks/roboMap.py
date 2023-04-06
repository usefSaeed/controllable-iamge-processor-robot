
import numpy as np
import serial
import cv2
arduino=serial.Serial('COM3', 9600)

def modify(s,index,newstring):
    return s[:index]+newstring+s[index+1:]

task="000"
x = 249
y = 499
fx = 249
fy = 499
flag = 0
lx = 249
ly = 499
firstonly = 0
flags=0
flagm=0
pts = [[fx, fy]]
last = 1
while True:
    modify(task,2,"0")
    canvas = np.zeros((500, 500, 3), dtype = "uint8")
    key = cv2.waitKeyEx(1)
    if(key==-1):
        print("hi")
        arduino.write('1'.encode())




    if (key==108):
        flags=0
        modify(task,0,"x")
    elif (key==109):
        flags=1
        modify(task, 0, "y")
    else :
        flags=2
        modify(task, 0, "z")
    #arduinoData=flags
    #arduinoData = bytes(str(arduinoData), 'ascii')
    #arduino.write(arduinoData.encode())
    if (key==100):
        flagm=0
        modify(task, 1, "m")
    else:
        flagm=1
        modify(task, 1, "b")
    #arduinoData=flagm
    if(key == 2490368):
        y = y-2
        print("Up")
        #arduino.write('u'.encode())
        #arduinoData=key
        #arduinoData = bytes(str(arduinoData), 'ascii')
        #arduino.write(arduinoData)
        modify(task, 2, "u")
        if(flag != 0):
            flag = 0
            fx = x
            fy = y
            if(firstonly == 0):
                firstonly = 1
                lx = x
                ly = y+2
            pts.insert(last, [fx, fy])
            last = last + 1
    elif (key == 2621440):
        y = y+2
        print("Down")
        #arduino.write('d'.encode())
        #arduinoData = key
        #arduinoData = bytes(str(arduinoData), 'ascii')
        #arduino.write(arduinoData)
        modify(task, 2, "d")
        if(flag != 1):
            flag = 1
            fx = x
            fy = y
            if(firstonly == 0):
                firstonly = 1
                lx = x
                ly = y-2
            pts.insert(last, [fx, fy])
            last = last + 1
    elif (key == 2424832):
        x = x-2
        #arduino.write('l'.encode())
        print("Left")
        #arduinoData = key
        #arduinoData = bytes(str(arduinoData), 'ascii')
        #arduino.write(arduinoData)
        modify(task, 2, "l")
        if(flag != 2):
            flag = 2
            fx = x
            fy = y
            if(firstonly == 0):
                firstonly = 1
                lx = x+2
                ly = y
            pts.insert(last, [fx, fy])
            last = last + 1
    elif (key == 2555904):
        x = x+2
        arduino.write('r'.encode())
        print("Right")
        #arduinoData = key
        #arduinoData = bytes(str(arduinoData), 'ascii')
        #arduino.write(arduinoData)
        modify(task, 2, "r")
        if(flag != 3):
            flag = 3
            fx = x
            fy = y
            if(firstonly == 0):
                firstonly = 1
                lx = x-2
                ly = y
            pts.insert(last, [fx, fy])
            last = last + 1
    if(firstonly == 0):
        cv2.line(canvas, (249, 499), (x, y), (0, 0, 255), 2)
    elif(firstonly == 1):
        cv2.line(canvas, (249, 499), (lx, ly), (0, 0, 255), 2)
    pts[last - 1][0] = x
    pts[last - 1][1] = y
    arduinoData = key
    arduinoData = bytes(str(arduinoData), 'ascii')
    arduino.write(arduinoData)

    arr = np.array(pts)
    arr = arr.reshape((-1, 1, 2))
    #print(arr)
    cv2.polylines(canvas, [arr], False, (0, 0, 255), 2)
    cv2.imshow("kdjbsdj", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()