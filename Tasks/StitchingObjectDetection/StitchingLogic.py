import numpy as np
import imutils
import cv2
import math


class Stitcher:
    def __init__(self):
        self.imgarr = []
        self.isOp = False
        self.recCnt = 0

    def join(self):
        count = 0
        while(len(self.imgarr)>1 and count<5):
            count += 1
            for j in range(1,len(self.imgarr)):
                #print("comparing " + str(0) + " and " + str(j))
                found = self.doMatch(0,j)
                self.recCnt = 0
                if found:
                    break
            if not found:
                self.imgarr.append(self.imgarr[0])
                del self.imgarr[0]

    def doMatch(self,i,j):
        if self.checkMatch(i,j):
            del self.imgarr[max(i,j)]
            del self.imgarr[min(i,j)]
            self.imgarr.append(self.result)
            #print("merge " + str(i) + " and " + str(j) + " and append")
            #print("images left now are " + str(len(self.imgarr)))
            return True
        return False

    def checkMatch(self,i, j):
        try:
            (self.result, vis) = self.stitch(i,j)
            return True
        except Exception as e:
            return False
            

    def stitch(self, i, j, ratio=0.75, reprojThresh=4.0):
        # unpack the images, then detect keypoints and extract
        # local invariant descriptors from them
        imageB = self.imgarr[i]
        imageA = self.imgarr[j]
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)
        # match features between the two images
        M = self.matchKeypoints(kpsA, kpsB,
                        featuresA, featuresB, ratio, reprojThresh)
        # if the match is None, then there aren't enough matched
        # keypoints to create a panorama
        if M is None:
            return None
        # otherwise, apply a perspective warp to stitch the images
        # together
        (matches, status) = M
        
        vis= self.drawMatches(imageA, imageB, kpsA, kpsB, matches,
                                   status)
        result = self.myWarpPerspective(imageB, imageA)
        if result.shape[1] < max(imageA.shape[1],imageB.shape[1])+100:
            self.isOp = True
            #print("el 3ax")
            self.recCnt += 1
            if (self.recCnt<2):
                self.doMatch(j,i)
            return None
        if self.bpr - self.bpl2 > 50:
            #print("left out")
            return None
        #cv2.imshow("Result",result)
        #cv2.imshow("vis",vis)
        #cv2.waitKey(0)
        
        return (result, vis)

    def detectAndDescribe(self, image):
        # convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # detect and extract features from the image
        descriptor = cv2.xfeatures2d.SIFT_create()
        (kps, features) = descriptor.detectAndCompute(image, None)
        # convert the keypoints from KeyPoint objects to NumPy
        # arrays
        kps = np.float32([kp.pt for kp in kps])
        # return a tuple of keypoints and features
        return (kps, features)

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
        # compute the raw matches and initialize the list of actual
        # matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []
        # loop over the raw matches
        for m in rawMatches:
            # ensure the distance is within a certain ratio of each
            # other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
        # computing a homography requires at least 20 matches
        #print(len(matches))
        if len(matches) > 10 or self.isOp:
            self.isOp = False
            # construct the two sets of points
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])
            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB,cv2.RANSAC,
                                             reprojThresh)
            # return the matches along with the homograpy matrix
            # and status of each matched point
            return (matches, status)
        # otherwise, no homograpy could be computed
        return None

    
    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        # initialize the output visualization image
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB
        # loop over the matches
        round1 = True
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # only process the match if the keypoint was successfully
            # matched
            if s == 1:
                # draw the match
                if (round1):
                    self.bpl = self.bpl2 = int(kpsB[trainIdx][0])
                    self.bpr = int(kpsA[queryIdx][0])
                else:
                    self.bpl = min(int(kpsB[trainIdx][0]), self.bpl)
                    self.bpl2 = max(int(kpsB[trainIdx][0]), self.bpl2)
                    self.bpr = min(int(kpsA[queryIdx][0]), self.bpr)

                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
                round1 = False

        # return the visualization
        return vis

    def myWarpPerspective(self,img1, img2):
        img1 = img1[0:500,0:self.bpl]
        img2 = img2[0:500,self.bpr:img2.shape[1]]
        res = cv2.hconcat([img1,img2])
        #cv2.imshow("Result",res)
        return res

    def maxWidth(self):
        res = self.imgarr[0]
        for img in self.imgarr:
            res = img if img.shape[1]>res.shape[1] else res
        return res

    
            

            

if __name__ == "__main__":
    stitcher = Stitcher()
    cv2.destroyAllWindows()


