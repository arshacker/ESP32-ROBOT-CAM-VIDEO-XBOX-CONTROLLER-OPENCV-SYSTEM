#####################################################################
#THE VIDEO STREAMING AQUISITION INSTRUCTIONS AND ASSOCIATED CODE WERE
#FOUND IN GITHUB, DELOREAN-EXPRESS
# https://github.com/Dallyla/delorean-express 
#####################################################################
#ANN:1
import cv2
from urllib import request
import numpy as np
import time
import random
import GFILE_2_C_15M

###############COMBO COMM
one_shot = 1
list_2_SEND = [0,0,0,0,0,0,0,0]
list_1_RCVD = [0,0,0,0,0,0,0,0]
xcm = 0
ycm = 0
xTrack = 0
yTrack = 0

list_state = [1,1,0,0,0,0,0,0]
              #MASK VIEW IS 1
                #COLOR:0 RED, 1 BLUE 2 GREEN

s_destroyOnce = 0
m_destroyOnce = 0
p_destroyOnce = 0
q_destroyOnce = 0


def probe_point(img,x,y):
    center = (x,y)
    radius = 10
    circle_color = (0,0,0)
    circle_width = -1

    cv2.circle(img,
    center,
    radius,
    circle_color,
    circle_width)   

#ANN:2
def text_display(img,text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (1,500)
    fontScale = 0.5
    fontColor = (0,0,0)
    lineType = 2

    topCornerXY = (0,475)
    bottomCornerXY = (800,515)   #image is approx 800X600
    color = (255,255,255)
    lineWidth = -1
    

    cv2.rectangle(img,
        topCornerXY,
        bottomCornerXY,
        color,
        lineWidth)
                  

    cv2.putText(img,text,
        bottomLeftCornerOfText,
        font,
        fontScale,
        fontColor,
        lineType)
    
#ANN:3    
def Combo_Comm():
    global one_shot
    global list_1_RCVD
    global xcm
    global ycm
    global xTrack
    global yTrack
    
    if (one_shot ==1):
        GFILE_2_C_15M.init_OneFile()
        one_shot = 0
    startTime = time.time()    
    print('list_1_RCVD =',list_1_RCVD)
    print('xTrack_DEBUG = ',xTrack)
    GFILE_2_C_15M.storeToTwoFile()
    for j in range(8):
         #list_2_SEND[j] = list_2_SEND[j] + 2
         #list_2_SEND[7] = 66
         #list_2_SEND[6] = round(xcm)
         #list_2_SEND[7] = round(ycm)
         list_2_SEND[6] = round(xTrack)
         list_2_SEND[7] = round(yTrack)
         #FILE_2_C_15M.db['DATA_2'][FILE_2_C_15M.name_list_2[j]] = list_2_SEND[j]
         GFILE_2_C_15M.list_2_SEND[j] = list_2_SEND[j]
    GFILE_2_C_15M.accessFromOneFile()
    print('list_1_RCVD_0 =',GFILE_2_C_15M.list_1_RCVD)
    list_1_RCVD=GFILE_2_C_15M.list_1_RCVD
    print('list_1_RCVD =',list_1_RCVD)
    endTime = time.time()
    print('TIME DURATION ===>',endTime-startTime)
    #time.sleep(.5)
###############END COMBO COMM

font = cv2.FONT_HERSHEY_SIMPLEX

current_milli_time = lambda: int(round(time.time() * 1000))


#ANN:4
#stream = request.urlopen('http://192.168.1.10/stream')
#stream = request.urlopen('http://192.168.1.10/stream_handler')
stream = request.urlopen('http://X.X.X.X') #SERVER IP ADDRESS
#stream = cv2.VideoCapture(0)

bts = b''
count = 0
total_fails = 10
starttime = time.time()
t1 = current_milli_time()
t2 = t1

lower_range= np.array([110,50,50], dtype=np.uint8)
upper_range = np.array([130,255,255], dtype=np.uint8)

#ANN:5 
def do_run():
  global bts
  global count
  global total_fails
  global starttime
  global t1
  global t2
  global xcm 
  global ycm
  global xTrack
  global yTrack
  global s_destroyOnce
  global lower_range
  global upper_range
  global p_destroyOnce
  
  while True:
      
    #Combo_Comm()
    bts += stream.read(1024)
    a = bts.find(b'\xff\xd8')
    b = bts.find(b'\xff\xd9')
    #print(a, b)
    #Combo_Comm()
    if a != -1 and b != -1:
        jpg = bts[a:b+2]
        bts = bts[b+2:]  #cant replace nothing to right of colon with 0
        #img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        # get image height, width
        (width, height) = img.shape[0:2]  #put in 0 instead of nothing to left of colon
                            
        width=round(1.3*width)     #width = 780
        height=round(0.75*height)  #height = 600
        #print("HEIGHT = ") 
        #print(height)
        # calculate the center of the image
        center = (height / 2, width / 2)
        
        angle0 = 0
        #angle90 = 90
        #angle180 = 180
        #angle270 = 270    #ORIGINAL
        
        scale = 1.0

        
        M = cv2.getRotationMatrix2D(center, angle0, scale)
        rotated_0 = cv2.warpAffine(img, M, (width, height))

        
        # cv2.imshow('Video', img)
        
        #ANN:6
        # convert BGR image to a HSV image
        hsv = cv2.cvtColor(rotated_0, cv2.COLOR_BGR2HSV) 

        # NumPy to create arrays to hold lower and upper range 
        # The “dtype = np.uint8” means that data type is an 8 bit integer [36, 28, 75]

        #RED
        #if list_state[1] == 0:
        if list_1_RCVD[4] == 1 and (list_1_RCVD[0] == 0 or list_1_RCVD[0] == 1) and list_1_RCVD[1] == 0:
            lower_range = np.array([136,87,111], dtype=np.uint8) 
            upper_range = np.array([180,255,255], dtype=np.uint8)
        #                            H   S   V

        #BLUE from another tutorial for hsv
        if list_1_RCVD[4] == 1 and list_1_RCVD[0] == 0 and list_1_RCVD[1] == 1:
            lower_range = np.array([110,50,50], dtype=np.uint8)
            upper_range = np.array([130,255,255], dtype=np.uint8)      
         
        #GREEN from opencv color wheel for hsv
        if list_1_RCVD[4] == 1 and list_1_RCVD[0] == 1 and list_1_RCVD[1] == 1:
            lower_range = np.array([35,50,50], dtype=np.uint8)
            upper_range = np.array([80,255,255], dtype=np.uint8)      

        #ANN:7
        # create a mask for image
        if list_1_RCVD[4] == 1:
            mask = cv2.inRange(hsv, lower_range, upper_range)
        

            #Tracking the  Color
            (contours, hierarchy)=cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        
            for pic, contour in enumerate(contours):
                t1 = current_milli_time()
                area = cv2.contourArea(contour)
                if(area>300):
                    x,y,w,h = cv2.boundingRect(contour)	
                    rotated_0 = cv2.rectangle(rotated_0,(x,y),(x+w,y+h),(35,142,35),2)
                    cv2.putText(rotated_0,"TRACKING",(x,y),cv2.FONT_HERSHEY_PLAIN, 0.7, (255,255,0))
                
            
                    if count < total_fails and (t1-t2) >= 500:
                        count += 1
                        print(count)
                        falhas = 'err-%s.png' %(count) 
                        latitude = random.random() * random.randint(10,50)
                        longitude = random.random() * random.randint(10,50)
                        cv2.putText(rotated_0,'Coord',(1,30), font, 0.8,(255,255,255),1)
                        cv2.putText(rotated_0,'X: -{}'.format(latitude),(1,45), font, 0.5,(255,255,255),1)
                        cv2.putText(rotated_0,'Y: -{}'.format(longitude),(1,60), font, 0.5,(255,255,255),1)
                        cv2.imwrite(falhas, rotated_0)
                        t2 = t1
        #ANN:8            
            try:
                xcm = 0
                ycm = 0
                xTrack = 0
                yTrack = 0
                areas = [cv2.contourArea(temp) for temp in contours]
                max_index = np.argmax(areas)
                #largest_contour = contours[max_index]
                Moments = cv2.moments(contours[max_index])
                M00 = Moments['m00']
                if M00 > 525:  # want a min size target
                    M10 = Moments['m10']
                    M01 = Moments['m01']
                    xcm = M10/M00
                    ycm = M01/M00
                    xTrack = (xcm - (width/2))/3
                    yTrack = -(ycm - (height/2))/3
                    print('XCM === ',xcm)
                    print('YCM === ',ycm)
                    print('XTRACK == ',xTrack)
                    print('YTRACK == ',yTrack)
                    text_display(rotated_0,'list_1_RCVD = ' + str(list_1_RCVD) + \
                        '   XCM = ' + str(round(xcm)) + '   YCM = ' + \
                        str(round(ycm)) + '   M00 = ' + str(M00))
                else:
                 text_display(rotated_0,'list_1_RCVD = ' + str(list_1_RCVD) + '    TARGET TOO SMALL') 
            except:
                 print('ERROR')
        else:
            print('NO TRACKING')
            text_display(rotated_0,'list_1_RCVD = ' + str(list_1_RCVD))

        #ANN:8A
        #CROP###################

        cropped = rotated_0[int(0.25*height*(abs(list_1_RCVD[7])/127 )):int(height-0.25*height*(abs(list_1_RCVD[7])/127 )),\
                          int(0.25*width*(abs(list_1_RCVD[7])/127 )):int(width-0.25*width*(abs(list_1_RCVD[7])/127 ))]

        (width_cr, height_cr) = cropped.shape[0:2]

        #cropped = rotated_0[200:400,200:400]
        #END CROP###############            

        #RESIZE##############
        
        width_new = round(width*(1+1.0*(abs(list_1_RCVD[7])/127 )))
        height_new = round(height*(1+1.0*(abs(list_1_RCVD[7])/127 )))
        dim_new = (width_new,height_new)
        #resized = cv2.resize(rotated_0,dim_new,interpolation = cv2.INTER_AREA)
        resized = cv2.resize(cropped,dim_new,interpolation = cv2.INTER_AREA)
        
        
            #cv2.destroyAllWindows()
            #s_destroyOnce = 0
            #cv2.imshow('Stream',resized)   
        #END RESIZE###############


  
            
        #ANN:9
        if list_1_RCVD[4] >= 0 and list_1_RCVD[2] == 0 and list_1_RCVD[3] == 0:
            if s_destroyOnce == 0:
                cv2.destroyAllWindows()
                s_destroyOnce = 1
                m_destroyOnce = 0
                p_destroyOnce = 0
                q_destroyOnce = 0
            cv2.imshow('Stream',rotated_0)
            #cv2.imshow('Stream',resized)
            #cv2.imshow('Stream',r)
        if list_1_RCVD[4] >= 0 and list_1_RCVD[2] == 0 and list_1_RCVD[3] == 1:
            if p_destroyOnce == 0:
                cv2.destroyAllWindows()
                p_destroyOnce = 1
                s_destroyOnce = 0
                q_destroyOnce = 0
            cv2.imshow('Streamer',resized)
            #cv2.imshow('Streamer',cropped) 
        if list_1_RCVD[4] == 1 and list_1_RCVD[2] == 1 and list_1_RCVD[3] == 0:    
            # Bitwise-AND mask and original image->show masked image
            res = cv2.bitwise_and(rotated_0,rotated_0, mask= mask)
            print('RES RES VALUE = ',res[225,450])
            if m_destroyOnce == 0:
                cv2.destroyAllWindows()
                m_destroyOnce = 1
                s_destroyOnce = 0
                p_destroyOnce = 0
                q_destroyOnce = 0
            cv2.imshow('res',res)
        if list_1_RCVD[4] == 1 and list_1_RCVD[2] == 1 and list_1_RCVD[3] == 1:
            print("UNDEFINED")
            if q_destroyOnce == 0:
                cv2.destroyAllWindows()
                q_destroyOnce = 1
                m_destroyOnce = 0
                p_destroyOnce = 0
                s_destroyOnce = 0
            cv2.imshow('Stream',rotated_0)
            
        #ANN:3C 
        Combo_Comm()

        if cv2.waitKey(1) == 27: #esc key ends loop. now can hit X on stream window   
                break
    

def main():
  do_run()

if __name__=="__main__":
  main()
            
