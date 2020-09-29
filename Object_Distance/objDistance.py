import numpy as np
import cv2


#objects values 
dist = 0
focal = 369
pixels = 30
width = 6.5



#find the distance from the camera
def get_dist(rectange_params,image):
    #find no of pixels covered
    pixels = rectange_params[1][0]
    #print(pixels)
    #calculate distance
    dist = (width*focal)/pixels
    
    #tag in the image stream
    image = cv2.putText(image, 'Distance from Camera in CM :', org, font,  
       1, color, 2, cv2.LINE_AA)

    image = cv2.putText(image, str("{:.2f}".format(dist)), (50,110), font,  
       fontScale, color, 2, cv2.LINE_AA)

    return image

#Capture Frame 
cap = cv2.VideoCapture(0)


#basic constants for opencv Functs
kernel = np.ones((3,3),'uint8')
font = cv2.FONT_HERSHEY_SIMPLEX 
org = (0,20)  
fontScale = 1.5 
color = (0, 255, 0) 
thickness = 2


cv2.namedWindow('Object Dist Measure ',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Object Dist Measure ', 700,600)


#loop to capture video frames
while True:
    ret, img = cap.read()

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)


    #predefined mask for yellow colour detection
    lower = np.array([22, 93, 0])
    upper = np.array([45, 255, 255])
    mask = cv2.inRange(hsv_img, lower, upper)
     


    #Remove Extra garbage from image
    d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations = 5)


    #find the histogram
    cont,hei = cv2.findContours(d_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key = cv2.contourArea, reverse = True)[:1]

    for cnt in cont:
        #check for contour area
        if (cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<306000):

            #Draw a rectange on the contour
            print (cnt)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect) 
            box = np.int0(box)
            cv2.drawContours(img,[box], -1,(0,255,0),3)
            
            img = get_dist(rect,img)

    cv2.imshow('Object Distance Measure ',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()