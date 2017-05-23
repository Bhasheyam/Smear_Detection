from os import listdir
from os.path import isfile, join
import numpy as np
import cv2

#from skimage.filters import threshold_adaptive

#defining the characteristic for the smear, it might be a radius od 10-12 pixel.

minpix=10
maxpix=12
char1= 3.14*minpix**2
char2= 3.14*maxpix**2
count=0
while count<5:
 if count==4:
     count += 1


 mypath='./sample_drive/cam_'+str(count)

 #Fetch all the images stored in the folder - GEOSpatial
 onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

 avg = np.zeros((500, 500, 3), np.float)
 avg_2 = np.zeros((500, 500, 3), np.float)

 # Start Displaying the images - GEOSpatial
 for n in range(0, len(onlyfiles)):
     x = cv2.imread(join(mypath, onlyfiles[n]))
     resized_image = cv2.resize(x, (500, 500))
     # resized_image = cv2.GaussianBlur(resized_image, (3,3), 0)
     resized_image = cv2.medianBlur(resized_image, 5)
     # cv2.imshow('Images', resized_image)
     im = np.array(resized_image, dtype=np.float)
     avg_2 = avg_2 + im / len(onlyfiles)
     avg = avg + im
     print(count)
     # cv2.waitKey()
     # cv2.destroyAllWindows()

 avg = avg / len(onlyfiles)
 # Generate, save and preview final image
 cv2.imwrite("Average_cam"+str(count)+".jpg",avg)

 avg_img = np.array(np.round(avg), dtype=np.uint8)
 grey_avg_img = cv2.cvtColor(avg_img, cv2.COLOR_BGR2GRAY)
 w_img = cv2.adaptiveThreshold(grey_avg_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 105, 11)
 w_img = cv2.bitwise_not(w_img)

 #onlyfiles1 = [f for f in listdir(mypath) if isfile(join(mypath, f))]
 img = cv2.imread(join(mypath,onlyfiles[17]))
# CV2.imshow('imgtest.png',img)
 resized_image = cv2.resize(img, (500, 500))

 _, contours,_ = cv2.findContours(w_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


 if contours:
     if (cv2.contourArea(contours[0]) >char1 and cv2.contourArea(contours[0]) <char2):
         final = cv2.drawContours(resized_image, contours, -1, (0, 0, 255), 2)
         cv2.imwrite("final_Image_Cam" + str(count) + ".jpg", final)
         cv2.imwrite("mask_Cam" + str(count) + ".jpg", w_img)


 count +=1

