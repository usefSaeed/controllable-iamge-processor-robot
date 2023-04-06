import cv2
import serial
import mediapipe as mp
#arduino = serial.Serial('com4',9600)


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        img = cv2.flip(img,1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)


        if self.results.multi_hand_landmarks:       #check if detects smth
            for handLms in self.results.multi_hand_landmarks: #for each hand draw landmarks
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for Id, lm in enumerate(myHand.landmark): #getting ids and their position as ratio

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([Id, cx, cy])  #store ids with their position

        return lmList

    def fingerCounter(self,lmList):
        tipIds = [4, 8, 12, 16, 20]
                 
        fingers = []
        if lmList[1][1] > lmList[17][1]:   #if right hand

            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:  #detect right thumb
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:  #detect left thumb
                fingers.append(1)
            else:
                fingers.append(0)

        for Id in range(1,5):  
            if lmList[tipIds[Id]][2] < lmList[tipIds[Id]-2][2]:    #detect other 4 fingers
                fingers.append(1)                                            
            else:
                fingers.append(0)

        totalFingers = sum(fingers)

        return totalFingers

def main():

    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:                        #if it detects hand
            totalFingers = detector.fingerCounter(lmList)
            if totalFingers>0:
                print(totalFingers)
                command = bytes(str(totalFingers)+'\n','ascii')
                #arduino.write(command)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()
