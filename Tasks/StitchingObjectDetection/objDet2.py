import cv2
import numpy as np


class objDet:
    def __init__(self):
        self.img = cv2.imread("SOD Outputs\Output.jpg",1)
        self.blured = cv2.bilateralFilter(self.img,9,300,300)
        self.kernel = np.ones((5,5),np.uint8)
        self.hsv = cv2.cvtColor(self.blured, cv2.COLOR_BGR2HSV)
        yellow_frag = self.getMask(0,100,0,100,255,255)#with borders
        blue_starfish = self.getMask(100,100,100,150,254,255)#with borders and needs dil
        colony_p1 = self.getMask(150,100,0,255,255,255)#black part missing and white parts
        colony_p2 = self.getMask(0,0,0,150,100,100)#black part with borders
        sponge_p1 = self.getMask(100,0,200,150,50,255)#with white colony and green missing
        sponge_p2 = self.getMask(75,100,100,100,255,200)#green part
        colony = colony_p1 + colony_p2 + sponge_p1
        colony = cv2.dilate(colony,self.kernel,15)
        sponge = sponge_p1 + sponge_p2
        sponge = cv2.dilate(sponge,self.kernel,15)
        self.comp(yellow_frag,3000, 12000,(0,128,255),"Coral Fragment") #3000-12000
        self.comp(blue_starfish,350, 3000,(255,255,0),"Sea Star") #350-3000
        self.comp(colony,3000,7000,(0,205,173),"Coral Colony") #3000-7000
        self.comp(sponge,800,2000,(0,255,128),"Sponge") #800-2000
        #cv2.imshow('image', self.img)
        cv2.imwrite("SOD Outputs\Final Output.jpg",self.img)
        cv2.waitKey(0)        


    def getMask(self,r1,g1,b1,r2,g2,b2):
        lower_range = np.array([r1,g1,b1])
        upper_range = np.array([r2,g2,b2])
        mask = cv2.inRange(self.hsv, lower_range, upper_range)
        if g2==254:
            mask = cv2.dilate(mask,self.kernel,20)

        #cv2.imshow('mask', mask)
        #cv2.waitKey(0)
        return mask
    
    def comp(self,img,area_thres1,area_thres2,col,text):
        skip = []
        ret, labels_map, stats, centroids = cv2.connectedComponentsWithStats(img)
        labels = range(1,np.max(labels_map) + 1)
        for label in labels:
            if label in skip:
                continue
            #mask = np.zeros_like(img)
            #mask[labels_map == label] = 255
            #cv2.imshow('mask', mask)
            #print(stats[label,cv2.CC_STAT_AREA])
            #cv2.waitKey(0)
            area1 = stats[label,cv2.CC_STAT_AREA]
            if area1>area_thres1 and area1<area_thres2:
                l = stats[label,cv2.CC_STAT_LEFT]
                t = stats[label,cv2.CC_STAT_TOP]
                r = stats[label,cv2.CC_STAT_LEFT] + stats[label,cv2.CC_STAT_WIDTH]
                d = stats[label,cv2.CC_STAT_TOP] + stats[label,cv2.CC_STAT_HEIGHT]
                for closeLabel in labels:
                    #mask2 = np.zeros_like(img)
                    #mask2[labels_map == closeLabel] = 255
                    #cv2.imshow('mask2', mask2)
                    #print("l : " + str(l) + " t : " + str(t) + " r : " + str(r) + " d : " + str(d))
                    #cv2.waitKey(0)
                    area2 = stats[closeLabel,cv2.CC_STAT_AREA]
                    l2 = stats[closeLabel,cv2.CC_STAT_LEFT]
                    t2 = stats[closeLabel,cv2.CC_STAT_TOP]
                    r2 = stats[closeLabel,cv2.CC_STAT_LEFT] + stats[closeLabel,cv2.CC_STAT_WIDTH]
                    d2 = stats[closeLabel,cv2.CC_STAT_TOP] + stats[closeLabel,cv2.CC_STAT_HEIGHT]
                    #print("l2 : " + str(l2) + " t2 : " + str(t2) + " r2 : " + str(r2) + " d2 : " + str(d2))
                    if area1>area2:
                        if self.closeTracker(l,r,t,d,l2,r2,t2,d2,15,"left") or self.closeTracker(l,r,t,d,l2,r2,t2,d2,15,"right")or self.closeTracker(l,r,t,d,l2,r2,t2,d2,15,"up")or self.closeTracker(l,r,t,d,l2,r2,t2,d2,15,"down"):
                            l = min(l,l2)
                            t = min(t,t2)
                            r = max(r,r2)
                            d = max(d,d2)
                            skip.append(closeLabel)
                st = (l-10,t-10)
                ed = (r+10,d+10)
                self.img = cv2.rectangle(self.img, st, ed, col, 4)
                labelSize=cv2.getTextSize(text,cv2.FONT_HERSHEY_SIMPLEX,1,2)
                st2 = (l-12,t-int(labelSize[0][1])-27)
                ed2 = (l-8+labelSize[0][0],t+7-int(labelSize[0][1]))
                cv2.rectangle(self.img,st2,ed2,col,cv2.FILLED)
                self.img = cv2.putText(self.img, text, (l-10,t-24), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
                #cv2.imshow("image",self.img)

    def closeTracker(self,l,r,t,d,l2,r2,t2,d2,pixelBlock,case):
        if case == "left" and (abs(r2-l)<pixelBlock and d2>t-pixelBlock and d2<d+pixelBlock):
            #print("lefty")
            return True
        if case == "right" and (abs(l2-r)<pixelBlock  and d2>t-pixelBlock and d2<d+pixelBlock):
            #print("righty")
            return True
        if case == "up" and ((abs(d2-t)<pixelBlock  and r2>l-pixelBlock and r2<r+pixelBlock)):
            #print("up high in the sky")
            return True
        if ((abs(t2-d)<pixelBlock  and r2>l-pixelBlock and r2<r+pixelBlock)):
            #print("I let you down")
            return True
        return False




if __name__ == "__main__":
    
    obj = objDet()
    cv2.destroyAllWindows()






