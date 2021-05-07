import cv2
import numpy as np
import classifier

class Localize:

    def process(self, frame):
        """
        Todo:
        preprocess frame to find out the location of UFO's. 
        sort them from top to bottom based on their location,
        crop the UFO image from original frame and pass it to classifier.
        submit the predicted numbers list.
        """

        ################## Please write your code here ###################

        """To find location of UFO's and crop them from top to bottom"""

        # create an opencv image
        img = cv2.imread(frame)

        # applying canny edge detection
        edged = cv2.Canny(img, 10, 250)

        #finding contours
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # sorting contours from top to bottom
        def get_contour_precedence(contour, cols):
            tolerance_factor = 10
            origin = cv2.boundingRect(contour)
            return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

        cnts.sort(key=lambda x:get_contour_precedence(x, img.shape[1]))

        # For debugging purposes.
        #for i in range(len(cnts)):
             #img = cv2.putText(img, str(i), cv2.boundingRect(cnts[i])[:2], cv2.FONT_HERSHEY_COMPLEX, 1, [125])
        
        
        #saving them to a cropped folder
        idx = 0
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            if w>50 and h>50:
                idx+=1
                new_img=img[y:y+h,x:x+w]
                #cropping images
                cv2.imwrite("cropped/"+str(idx) + '.png', new_img)
        #cv2.imshow("Original Image",image)
        #cv2.imshow("Canny Edge",edged)
        #cv2.waitKey(0)
        print('>> Objects Cropped Successfully!')
        print(">> Check out 'cropped' Directory")
        ##################################################################


        """
        Example: (how to use classifier)

        Note:-
        1. instead of reading cropped image from directory
        you need to find the locations of UFO's on the frame, crop them
        and sort them from top to bottom,
        pass them through classifier and return predicted numbers

        2. This example below is just for demonstration purpose,
        you can delete it when you write your own code above.
        """
        crop1 = cv2.imread("cropped/1.png")
        crop2 = cv2.imread("cropped/4.png")
        crop3 = cv2.imread("cropped/5.png")
        crop4 = cv2.imread("cropped/7.png")
        myanswer = classifier.predict(images=[crop1, crop2, crop3, crop4])
        return myanswer

localize = Localize()