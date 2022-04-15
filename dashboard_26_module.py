import pygame
from pygame.locals import *

import math

pygame.init()

ScreenWidth = 400
ScreenHeight = 950

ScreenSize = (ScreenWidth,ScreenHeight)

DashScreen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption("DASHBOARD")

running = True

black = (0,0,0)
gray = (128,128,128)
light_gray = (200,200,200)
dark_gray = (64,64,64)
white = (255,255,255)
red = (255,0,0)
light_red =(128,0,0)
green = (0,255,0)
blue = (0,0,255)
#ANN:1
LineWidth = 1
LWC=1   #LWC is Line Width correction of blue background next to black outline of xbox
Offset = ScreenWidth*(10/250)                     #10
XOrigin = 0+LWC
YOrigin = ScreenWidth*(280/250)                     #ScreenWidth*1.12    
#YOrigin = ScreenWidth*1.12
Slant = ScreenWidth*(100/250)          #100
Handle = ScreenWidth*(40/250)         #40
HWratio=ScreenWidth*(1.12/250)      #1.12
HWIratio=ScreenWidth*(0.95/250)     #0.95
Kappa = ScreenWidth*(45/250)
DepthX=ScreenWidth*(20/250)         #20
DepthY=ScreenWidth*(30/250)        #30
TrigX=ScreenWidth*(50/250)          #50
TrigY=ScreenWidth*(40/250)          #40
TrigW=ScreenWidth*(30/250)         #30
TrigXO=ScreenWidth*(30/250)         #30
Del=ScreenWidth*(8/250)           #8
Alpha=ScreenWidth*(80/250)        #89
Radius_ABXY= ScreenWidth*(9/250)  #9
Beta = ScreenWidth*(25/250)    #25
#-----------JOYSTICKS------------------
xCenter_1 = ScreenWidth*(160/250)    #160
yCenter_1 = ScreenWidth*(140/250)    #140
radius_1 = math.floor((ScreenWidth/250)*25)    #25
xCenter_2 = ScreenWidth*(45/250)    #160
yCenter_2 = ScreenWidth*(90/250)    #140
radius_2 = math.floor((ScreenWidth/250)*25)    #25
radius_3 = 5
radius_4 = 10
radius_5 = 25
#--------end JOYSTICKS------------
x_HatOrigin = ScreenWidth*(90/250)     #90
y_HatOrigin= ScreenWidth*(193/250) #195
h_width= ScreenWidth*(5/250)  #5
h_height= ScreenWidth*(15/250) #15
L1_R1_radius = ScreenWidth*(7/250)  #7
x_ZOrigin = ScreenWidth*(125/250)   #125
y_ZOrigin = ScreenWidth*(150/250)   #150
Z_radius = ScreenWidth*(1.8/250)*L1_R1_radius    #1.8
#------------SENSORS-------------------------
ZEROSCALEANGLE =260
TOTALANGLE = 335
FontSize = math.floor(ScreenWidth*(40/250))  #40
FontSize_1 = math.floor(ScreenWidth*(20/250))  #20
FontSize_2 = math.floor(ScreenWidth*(20/250))  #20

BottomSensor_2 = ScreenWidth*1.5-2*radius_1 + 2*2*radius_1
Y_Sensor_3 = BottomSensor_2 + 2*radius_1
DelX_Sensor_3 = math.floor((ScreenWidth/250)*60)  #60
DelY_Sensor_3 = math.floor((ScreenWidth/250)*40)  #40
YCenter_Sensor_3 = math.floor((ScreenWidth/250)*6)          #6
XCenter_Sensor_3 = math.floor((ScreenWidth/250)*5)          #5
YCORR_Sensor_1 = math.floor((ScreenWidth/250)*5)          #5
NUMCORR_Sensor_1 = math.floor((ScreenWidth/250)*15)          #15
NUMCORR2_Sensor_1 = math.floor((ScreenWidth/250)*10)          #10
NUMCORR3_Sensor_1 = math.floor((ScreenWidth/250)*12)          #12
NUMCORR4_Sensor_1 = math.floor((ScreenWidth/250)*6)          #6
NUMCORR5_Sensor_1 = math.floor((ScreenWidth/250)*3)          #3
NUMBACKGRND_Sensor_2 = math.floor((ScreenWidth/250)*6)          #6
NUMCORR_Sensor_2 = math.floor((ScreenWidth/250)*6)          #6

DefaultFont = None
DashFont = pygame.font.Font(DefaultFont,FontSize)
DashFont_1 = pygame.font.Font(DefaultFont,FontSize_1)
DashFont_2 = pygame.font.Font(DefaultFont,FontSize_2)
#------------END SENSORS------------------
running = True
#ANN:2
def Dashboard():   #draw black background. draw xbox with white lines. draw lower baclground
                        #and upper background using blue polygons
    
    DashScreen.fill(black)
    XBOX_Outline()
    Button_B(gray)
    Button_X(gray)
    Button_Y(gray)
    Button_A(gray)
    background1(blue)
    background2(blue)
    TrigL_Sig(gray)
    TrigR_Sig(gray)
    Button_L(gray)
    Button_R(gray)
    #print(Angle_to_Rads(180))
    #anArc(gray,160,140,25,0,180)
    JStick_1(red,green,red,green)
    JStick_2(red,green,red,green)
    Hat(gray,gray,gray,gray)
    #pygame.draw.arc(DashScreen,gray,(200,250,50,50),0,3.14,25)
    ZbuttonGroup(gray,gray,gray)
###########WIDGETS#############
    SENSOR_1_NUM_BACKGRND(red)
    SENSOR_1(red)
    SENSOR_1_ARC0(red,260,-80)
    SENSOR_1_FILL(gray,-80,260)
    ####SENSOR_1_VALUE(green,-80,260)    #FULL SCALE   STARTANGLE=-80   END ANGLE=260
                                          #THUS   FULLSCALEANGLE=-80     ZEROSCALEANGLE= 260
                                         #TOTALANGLE=340
                                     #ZERO SCALE   STARTANGLE=260   ENDANGLE=260
    ####SENSOR_1_VALUE(green,260-0.7*340,260)
    #SENSOR_1_VALUE(green,0.7)
    SENSOR_1_NUM(white)
    SENSOR_2_NUM_BACKGROUND(red)    
    SENSOR_2(red)
    SENSOR_2_FILL(gray)
    #SENSOR_2_VALUE(green,0.7)
    SENSOR_2_NUM(white)    
    SENSOR_3(red)
    SENSOR_3_FILL(green)
    ###SENSOR_3_VALUE(red,127,ScreenWidth*.7+XCenter_Sensor_3,Y_Sensor_3 + YCenter_Sensor_3)
    #SENSOR_3_VALUE(red,127)
    pygame.display.update()

##########################DRAWING NOTES#########################

#ARC START ANGLE=0 DEGREES   X=X0,Y=0 END ANGLE IS CCW
#TRIG FUNCS degrees(value),radians(degrees),pi,sin and cos in radians

#######################END DRAWING NOTES########################    

###################SENSOR WIDGETS#####################################
#ANN:3    
def SENSOR_1_NUM_BACKGRND(color):
    pygame.draw.circle(DashScreen,color,(ScreenWidth*0.3,ScreenWidth*1.5+YCORR_Sensor_1 ),2.8*radius_1+4*LWC)

def SENSOR_1(color):
    pygame.draw.circle(DashScreen,color,(ScreenWidth*0.3,ScreenWidth*1.5+YCORR_Sensor_1 ),2*radius_1+4*LWC,4)


def SENSOR_1_VALUE(color,decFraction): 
    pygame.draw.arc(DashScreen,color,(ScreenWidth*0.30-2*radius_1,ScreenWidth*1.5-2*radius_1+YCORR_Sensor_1 ,\
                    2*2*radius_1,2*2*radius_1),\
                    Angle_to_Rads(ZEROSCALEANGLE-decFraction*TOTALANGLE),Angle_to_Rads(ZEROSCALEANGLE),2*radius_1)

#def SENSOR_1_VALUE(color,startAngle,endAngle): 
#    pygame.draw.arc(DashScreen,color,(ScreenWidth*0.25-2*radius_1,ScreenWidth*1.5-2*radius_1,\
#                    2*2*radius_1,2*2*radius_1),\
#                    Angle_to_Rads(startAngle),Angle_to_Rads(endAngle),2*radius_1)

def SENSOR_1_ARC0(color,startAngle,endAngle): 
    pygame.draw.arc(DashScreen,color,(ScreenWidth*0.30-2*radius_1,ScreenWidth*1.5-2*radius_1+YCORR_Sensor_1 ,\
                    2*2*radius_1,2*2*radius_1),\
                    Angle_to_Rads(startAngle),Angle_to_Rads(endAngle),2*radius_1)    

def SENSOR_1_FILL(color,startAngle,endAngle): 
    pygame.draw.arc(DashScreen,color,(ScreenWidth*0.3-2*radius_1,ScreenWidth*1.5-2*radius_1+YCORR_Sensor_1 ,\
                    2*2*radius_1,2*2*radius_1),\
                    Angle_to_Rads(startAngle),Angle_to_Rads(endAngle),2*radius_1)    

def SENSOR_1_NUM(color):
    astring = str(0)
    b_numb = astring.encode()
    DashTextGraphic_1 = DashFont_1.render(b_numb,True,color)
    DashScreen.blit(DashTextGraphic_1,(ScreenWidth*0.3-(2*radius_1+NUMCORR3_Sensor_1)*math.sin(math.pi/12),\
                                     ScreenWidth*1.5+(2*radius_1+NUMCORR3_Sensor_1)*math.cos(math.pi/12)))
    for numb in [1,2,3,4,5]:
        astring = str(numb)
        b_numb = astring.encode()
        DashTextGraphic_1 = DashFont_1.render(b_numb,True,color)
        DashScreen.blit(DashTextGraphic_1,\
               (ScreenWidth*0.3-(2*radius_1+NUMCORR_Sensor_1)*math.sin(math.pi/12+((math.pi-math.pi/12)/5)*numb),\
                ScreenWidth*1.5+(2*radius_1+NUMCORR_Sensor_1)*math.cos(math.pi/12+((math.pi-math.pi/12)/5)*numb)))

    for numb in [1,2,3,4,5]:
        astring = str(numb+5)
        b_numb = astring.encode()
        DashTextGraphic_1 = DashFont_1.render(b_numb,True,color)
        if numb!=5:
            DashScreen.blit(DashTextGraphic_1,\
              (ScreenWidth*0.3-(2*radius_1+NUMCORR2_Sensor_1)*math.sin(math.pi+((math.pi-math.pi/12)/5)*numb),\
               ScreenWidth*1.5+(2*radius_1+NUMCORR2_Sensor_1)*math.cos(math.pi+((math.pi-math.pi/12)/5)*numb)))
        
        if numb==5:
            DashScreen.blit(DashTextGraphic_1,\
               (ScreenWidth*0.3-(2*radius_1+NUMCORR2_Sensor_1)*math.sin(math.pi+((math.pi-math.pi/12)/5)*numb)-NUMCORR4_Sensor_1,\
                ScreenWidth*1.5+(2*radius_1+NUMCORR2_Sensor_1)*math.cos(math.pi+((math.pi-math.pi/12)/5)*numb)+NUMCORR5_Sensor_1))


def SENSOR_2_NUM_BACKGROUND(color):
    pygame.draw.rect(DashScreen,color,(ScreenWidth*.75-NUMBACKGRND_Sensor_2,ScreenWidth*1.5-2.5*radius_1,\
                                       2.4*radius_1,2.5*2*radius_1))
    
def SENSOR_2(color):
    pygame.draw.rect(DashScreen,color,(ScreenWidth*.75,ScreenWidth*1.5-2*radius_1,radius_1,2*2*radius_1),6)

def SENSOR_2_FILL(color):
    pygame.draw.rect(DashScreen,color,(ScreenWidth*.75,ScreenWidth*1.5-2*radius_1,radius_1,2*2*radius_1))

def SENSOR_2_VALUE(color,decFraction):
    pygame.draw.rect(DashScreen,color,(ScreenWidth*.75,\
                        ScreenWidth*1.5-2*radius_1 + (1-decFraction)*(2*2*radius_1),\
                        radius_1,\
                        (decFraction)*2*2*radius_1))
    
def SENSOR_2_NUM(color):
    astring = str(1.0)
    b_numb = astring.encode()
    DashTextGraphic_1 = DashFont_1.render(b_numb,True,color)
    DashScreen.blit(DashTextGraphic_1,(ScreenWidth*.75+1.2*radius_1,\
                                     ScreenWidth*1.5-2*radius_1-NUMCORR_Sensor_2))
    for i in [0.0,0.2,0.4,0.6,0.8,1.0]:
        astring = str(i)
        b_numb = astring.encode()
        DashTextGraphic_1 = DashFont_1.render(b_numb,True,color)
        DashScreen.blit(DashTextGraphic_1,(ScreenWidth*.75+1.2*radius_1,\
                                     ScreenWidth*1.5-2*radius_1-NUMCORR_Sensor_2+(2*2*radius_1-i*2*2*radius_1)))
    
    
#    DashScreen.blit(DashTextGraphic_1,(ScreenWidth*.75+1.2*radius_1,\
#                                     ScreenWidth*1.5-2*radius_1,radius_1,2*2*radius_1))
    


def SENSOR_3(color):
    pygame.draw.rect(DashScreen,color,(ScreenWidth*.7,Y_Sensor_3,DelX_Sensor_3,DelY_Sensor_3),6)

def SENSOR_3_FILL(color):
    pygame.draw.rect(DashScreen,color,(ScreenWidth*.7,Y_Sensor_3,DelX_Sensor_3,DelY_Sensor_3))

def SENSOR_N_FILL(color):
    pygame.draw.rect(DashScreen,color,(0,840,400,70))

def SENSOR_3_VALUE(color,numb):
    #DefaultFont = None
    #GameFont = pygame.font.Font(DefaultFont,60)
    astring = str(numb)
    b_numb = astring.encode()
    DashTextGraphic = DashFont.render(b_numb,True,color)
    DashScreen.blit(DashTextGraphic,(ScreenWidth*.7+XCenter_Sensor_3,Y_Sensor_3 + YCenter_Sensor_3))
    
def SENSOR_N_VALUE(color,numb,xloc,yloc):
    bstring = str(numb)
    c_numb = bstring.encode()
    DashTextGraphic2 = DashFont_2.render(c_numb,True,color)
    DashScreen.blit(DashTextGraphic2,(xloc,yloc))
    
        
#################END SENSOR WIDGETS################################    


def XBOX_Outline():    #lines start lower left and proceed clockwise in all routines in this function
    Outline_Front = pygame.draw.lines(DashScreen,white,True,\
                                #1              #2
                        [(XOrigin+1*LWC,YOrigin),(Offset,Slant),\
                         #(ScreenWidth-Offset,Slant),\
                          (ScreenWidth*0.33,Slant),(ScreenWidth*0.33,Slant+Beta),\
                          (ScreenWidth*0.66,Slant+Beta),(ScreenWidth*0.66,Slant),\
                          (ScreenWidth-Offset,Slant),\
                                        #14
                         (ScreenWidth-4*LWC,YOrigin),\
                         (ScreenWidth-Handle,YOrigin),\
                         (ScreenWidth-Handle-Offset,YOrigin-Kappa),\
                         (XOrigin+Handle+Offset,YOrigin-Kappa),\
                         (XOrigin+Handle,YOrigin)],LineWidth)
                         #(XOrigin+Handle,ScreenWidth*HWratio)],LineWidth)
                          
                                   #15  (ScreenWidth,0)
                                   #16  (0,0)

    #Used for initial design of channel in drawing
    #Channel_Front = pygame.draw.lines(DashScreen,white,False,\
    #                     [(ScreenWidth*0.33,Slant),\
    #                      (ScreenWidth*0.33,Slant+Beta),\
    #                      (ScreenWidth*0.66,Slant+Beta),\
    #                      (ScreenWidth*0.66,Slant)],LineWidth)
                                      

    Outline_Depth = pygame.draw.lines(DashScreen,white,False,\
                                                 #3
                        [(Offset,Slant),(Offset+DepthX,Slant-DepthY),\
                         
                         (ScreenWidth*0.33+DepthX,Slant-DepthY),(ScreenWidth*0.33+DepthX,Slant+Beta-DepthY),\
                         (ScreenWidth*0.66-DepthX,Slant+Beta-DepthY),(ScreenWidth*0.66-DepthX,Slant-DepthY),\

                         
                                           #12
                         (ScreenWidth-Offset-DepthX,Slant-DepthY),\
                                         #13
                         (ScreenWidth-Offset,Slant)],LineWidth)

    #Used for initial design of channel in drawing
    #Channel_Depth = pygame.draw.lines(DashScreen,white,False,\
    #                     [(ScreenWidth*0.33+DepthX,Slant-DepthY),(ScreenWidth*0.33+DepthX,Slant+Beta-DepthY),\
    #                      (ScreenWidth*0.66-DepthX,Slant+Beta-DepthY),(ScreenWidth*0.66-DepthX,Slant-DepthY)],LineWidth)

    Channel_ConnectorL_Top = pygame.draw.lines(DashScreen,white,False,\
                         [(ScreenWidth*0.33,Slant),(ScreenWidth*0.33+DepthX,Slant-DepthY)],LineWidth)

    Channel_ConnectorL_Bot = pygame.draw.lines(DashScreen,white,False,\
                         [(ScreenWidth*0.33,Slant+Beta),(ScreenWidth*0.33+DepthX,Slant+Beta-DepthY)],LineWidth)                      
                        
    Channel_ConnectorR_Bot = pygame.draw.lines(DashScreen,white,False,\
                         [(ScreenWidth*0.66,Slant+Beta),(ScreenWidth*0.66-DepthX,Slant+Beta-DepthY)],LineWidth)

    Channel_ConnectorR_Top = pygame.draw.lines(DashScreen,white,False,\
                         [(ScreenWidth*0.66,Slant),(ScreenWidth*0.66-DepthX,Slant-DepthY)],LineWidth)                      
                                      

    Outline_TriggerL = pygame.draw.lines(DashScreen,white,False,\
                         #4                  #5
         [(Offset+TrigXO,Slant-DepthY),(Offset+DepthX+TrigX,Slant-DepthY-TrigY),\
                                #6
          (Offset+DepthX+TrigX+TrigW,Slant-DepthY-TrigY),\
          (Offset+TrigXO+TrigW,Slant-DepthY)],LineWidth)

    Outline_TriggerL1 = pygame.draw.lines(DashScreen,white,False,\
                                                                     #7
       [(Offset+DepthX+TrigX+TrigW,Slant-DepthY-TrigY),(Offset+DepthX+TrigX+TrigW,Slant-DepthY+Beta)],LineWidth)
    
                                                                   #TriggerR starts lower right, goes ccw
    Outline_TriggerR = pygame.draw.lines(DashScreen,white,False,\
                      #11                                             #10
    [(ScreenWidth-Offset-TrigXO,Slant-DepthY),(ScreenWidth-Offset-DepthX-TrigX,Slant-DepthY-TrigY),\
                                #9
     (ScreenWidth-Offset-DepthX-TrigX-TrigW,Slant-DepthY-TrigY),\
     (ScreenWidth-Offset-TrigXO-TrigW,Slant-DepthY)],LineWidth)
                                                                      
    Outline_TriggerR1 = pygame.draw.lines(DashScreen,white,False,\
        [(ScreenWidth-Offset-DepthX-TrigX-TrigW,Slant-DepthY-TrigY),\
                                #8
        (ScreenWidth-Offset-DepthX-TrigX-TrigW,Slant-DepthY+Beta)],LineWidth)

def Button_L(color):
    pygame.draw.polygon(DashScreen,color,\
    [(Offset+2*Del,Slant-1.2*Del),(Offset+DepthX+0.9*Del,Slant-DepthY+1.2*Del),\
     (Offset+DepthX+0.4*Alpha,Slant-DepthY+1.2*Del),(Offset+0.5*Alpha,Slant-1.2*Del)],0)

def Button_R(color):
    pygame.draw.polygon(DashScreen,color,\
    [(ScreenWidth-Offset-2*Del,Slant-1.2*Del),(ScreenWidth-Offset-DepthX-0.9*Del,Slant-DepthY+1.2*Del),\
     (ScreenWidth-Offset-DepthX-0.4*Alpha,Slant-DepthY+1.2*Del),(ScreenWidth-Offset-0.5*Alpha,Slant-1.2*Del)],0)
              

def TrigL_Sig(color):
    pygame.draw.polygon(DashScreen,color,\
         [(Offset+TrigXO+2.0*Del,Slant-DepthY-Del),(Offset+DepthX+TrigX+0.2*Del,Slant-DepthY-TrigY+Del),\
          (Offset+DepthX+TrigX+TrigW-2*Del,Slant-DepthY-TrigY+Del),\
          (Offset+TrigXO+TrigW-0.5*Del,Slant-DepthY-Del)],0)

def TrigR_Sig(color):
    pygame.draw.polygon(DashScreen,color,\
         [(ScreenWidth-Offset-TrigXO-2.0*Del,Slant-DepthY-1.0*Del),(ScreenWidth-Offset-DepthX-TrigX-0.5*Del,Slant-DepthY-TrigY+0.8*Del),\
          (ScreenWidth-Offset-DepthX-TrigX-TrigW+2.0*Del,Slant-DepthY-TrigY+1.0*Del),\
          (ScreenWidth-Offset-TrigXO-TrigW+0.5*Del,Slant-DepthY-1.0*Del)],0)                   

def background1(color):  #area below xbox. polyg starts lower left corner of xbox and proceeds clockwise
    pygame.draw.polygon(DashScreen,color,[(XOrigin,ScreenHeight),(XOrigin,YOrigin+LWC),\
                (XOrigin+Handle,YOrigin+LWC),\
                (XOrigin+Handle+Offset,YOrigin-Kappa+LWC),\
                (ScreenWidth-Handle-Offset,YOrigin-Kappa+LWC),\
                (ScreenWidth-Handle,YOrigin+LWC),\
                (ScreenWidth,YOrigin+LWC),\
                (ScreenWidth,ScreenHeight)],0)                         
                         
def background2(color):   #area above xbox. polyg starts lower left corner of xbox and proceeds counter clockwise. nbrs below
                        #correspond to nbrs above.
                                               #1               #2
    pygame.draw.polygon(DashScreen,color,[(XOrigin-LWC,YOrigin),(Offset-6*LWC,Slant),\
                         #3
         (Offset+DepthX,Slant-DepthY-4*LWC),\
                           #4                              #5              
         (Offset+TrigXO-4*LWC,Slant-DepthY-4*LWC),(Offset+DepthX+TrigX,Slant-DepthY-TrigY-4*LWC),\
                                       #6  
         (Offset+DepthX+TrigX+TrigW+4*LWC,Slant-DepthY-TrigY),\
                               #7                                     #8          
         (Offset+DepthX+TrigX+TrigW+4*LWC,Slant-DepthY-4*LWC+Beta),(ScreenWidth-Offset-DepthX-TrigX-TrigW-4*LWC,Slant-DepthY-4*LWC+Beta),\
                                         #9
         (ScreenWidth-Offset-DepthX-TrigX-TrigW-4*LWC,Slant-DepthY-TrigY-4*LWC),\
                                         #10
         (ScreenWidth-Offset-DepthX-TrigX,Slant-DepthY-TrigY-4*LWC),\
                                    #11                           #12     
         (ScreenWidth-Offset-TrigXO+4*LWC,Slant-DepthY-4*LWC),(ScreenWidth-Offset-DepthX+4*LWC,Slant-DepthY),\
                            #13                         #14
         (ScreenWidth-Offset+4*LWC,Slant),(ScreenWidth+6*LWC,ScreenWidth*HWratio),\
               #15        #16
         (ScreenWidth,0),(0,0)],0)

def Button_B(color):
    pygame.draw.circle(DashScreen,color,(ScreenWidth*0.92,ScreenWidth*0.58),Radius_ABXY)

def Button_X(color):
    pygame.draw.circle(DashScreen,color,(ScreenWidth*0.8,ScreenWidth*0.58),Radius_ABXY)

def Button_Y(color):
    pygame.draw.circle(DashScreen,color,(ScreenWidth*0.86,ScreenWidth*0.5),Radius_ABXY)

def Button_A(color):
    pygame.draw.circle(DashScreen,color,(ScreenWidth*0.86,ScreenWidth*0.66),Radius_ABXY)

#0 degrees is straight up and degrees go ccw
def Angle_to_Rads(angle):
    return round(angle*(6.28/360),2)

def anArc(color,xCenter,yCenter,radius,startAngle,endAngle): 
    pygame.draw.arc(DashScreen,color,(xCenter-radius,yCenter+radius,2*radius,2*radius),\
                    Angle_to_Rads(startAngle),Angle_to_Rads(endAngle),radius)

def JStick_1(color_up,color_down,color_left,color_right):    
    pygame.draw.arc(DashScreen,color_up,(xCenter_1-radius_1,yCenter_1+radius_1,2*radius_1,2*radius_1),\
                    Angle_to_Rads(50),Angle_to_Rads(130),radius_1)                    
    pygame.draw.arc(DashScreen,color_left,(xCenter_1-radius_1,yCenter_1+radius_1,2*radius_1,2*radius_1),\
                    Angle_to_Rads(140),Angle_to_Rads(220),radius_1)                    
    pygame.draw.arc(DashScreen,color_down,(xCenter_1-radius_1,yCenter_1+radius_1,2*radius_1,2*radius_1),\
                    Angle_to_Rads(230),Angle_to_Rads(310),radius_1)                    
    pygame.draw.arc(DashScreen,color_right,(xCenter_1-radius_1,yCenter_1+radius_1,2*radius_1,2*radius_1),\
                    Angle_to_Rads(320),Angle_to_Rads(40),radius_1)
    
def JStick_1Y(arc_width_up,arc_width_down):
    pygame.draw.arc(DashScreen,gray,(xCenter_1-radius_1,yCenter_1+radius_1,2*radius_1,2*radius_1),\
                    Angle_to_Rads(50),Angle_to_Rads(130),arc_width_up)
    pygame.draw.arc(DashScreen,gray,(xCenter_1-radius_1,yCenter_1+radius_1,2*radius_1,2*radius_1),\
                    Angle_to_Rads(230),Angle_to_Rads(310),arc_width_down)

def JStick_1X(arc_width_left,arc_width_right):
    pygame.draw.arc(DashScreen,gray,(xCenter_1-radius_1,yCenter_1+radius_1,2*radius_1,2*radius_1),\
                    Angle_to_Rads(140),Angle_to_Rads(220),arc_width_left)
    pygame.draw.arc(DashScreen,gray,(xCenter_1-radius_1,yCenter_1+radius_1,2*radius_1,2*radius_1),\
                    Angle_to_Rads(320),Angle_to_Rads(40),arc_width_right)
    
def JStick_2(color_up,color_down,color_left,color_right):    
    pygame.draw.arc(DashScreen,color_up,(xCenter_2-radius_2,yCenter_2+radius_2,2*radius_2,2*radius_2),\
                    Angle_to_Rads(50),Angle_to_Rads(130),radius_2)                    
    pygame.draw.arc(DashScreen,color_left,(xCenter_2-radius_2,yCenter_2+radius_2,2*radius_2,2*radius_2),\
                    Angle_to_Rads(140),Angle_to_Rads(220),radius_2)                    
    pygame.draw.arc(DashScreen,color_down,(xCenter_2-radius_2,yCenter_2+radius_2,2*radius_2,2*radius_2),\
                    Angle_to_Rads(230),Angle_to_Rads(310),radius_2)                    
    pygame.draw.arc(DashScreen,color_right,(xCenter_2-radius_2,yCenter_2+radius_2,2*radius_2,2*radius_2),\
                    Angle_to_Rads(320),Angle_to_Rads(40),radius_2)

def JStick_2Y(arc_width_up,arc_width_down):
    pygame.draw.arc(DashScreen,gray,(xCenter_2-radius_2,yCenter_2+radius_2,2*radius_2,2*radius_2),\
                    Angle_to_Rads(50),Angle_to_Rads(130),arc_width_up)
    pygame.draw.arc(DashScreen,gray,(xCenter_2-radius_2,yCenter_2+radius_2,2*radius_2,2*radius_2),\
                    Angle_to_Rads(230),Angle_to_Rads(310),arc_width_down)

def JStick_2X(arc_width_left,arc_width_right):
    pygame.draw.arc(DashScreen,gray,(xCenter_2-radius_2,yCenter_2+radius_2,2*radius_2,2*radius_2),\
                    Angle_to_Rads(140),Angle_to_Rads(220),arc_width_left)
    pygame.draw.arc(DashScreen,gray,(xCenter_2-radius_2,yCenter_2+radius_2,2*radius_2,2*radius_2),\
                    Angle_to_Rads(320),Angle_to_Rads(40),arc_width_right)


#   x->  y down pos
#
#
#             RECTANGLE--SEE HAT BELOW
#
#                     xo,yo....
#                          .  .
#                          .  .
#               xo,yo+h    ....xo+w,yo+h
#

    

def Hat(color_up,color_down,color_left,color_right):
    pygame.draw.circle(DashScreen,gray,(x_HatOrigin+(h_width/2),y_HatOrigin-(h_width/2)),h_height+2*h_width,1)
    pygame.draw.rect(DashScreen,color_down,(x_HatOrigin,y_HatOrigin,h_width,h_height))
    pygame.draw.rect(DashScreen,color_up,(x_HatOrigin,y_HatOrigin-h_width-h_height,h_width,h_height))
    pygame.draw.rect(DashScreen,color_right,(x_HatOrigin+h_width,y_HatOrigin-h_width,h_height,h_width))
    pygame.draw.rect(DashScreen,color_left,(x_HatOrigin-h_height,y_HatOrigin-h_width,h_height,h_width))

def HatY(color_up,color_down):
    pygame.draw.circle(DashScreen,gray,(x_HatOrigin+(h_width/2),y_HatOrigin-(h_width/2)),h_height+2*h_width,1)
    pygame.draw.rect(DashScreen,color_down,(x_HatOrigin,y_HatOrigin,h_width,h_height))
    pygame.draw.rect(DashScreen,color_up,(x_HatOrigin,y_HatOrigin-h_width-h_height,h_width,h_height))

def HatX(color_left,color_right):
    pygame.draw.circle(DashScreen,gray,(x_HatOrigin+(h_width/2),y_HatOrigin-(h_width/2)),h_height+2*h_width,1)
    pygame.draw.rect(DashScreen,color_right,(x_HatOrigin+h_width,y_HatOrigin-h_width,h_height,h_width))
    pygame.draw.rect(DashScreen,color_left,(x_HatOrigin-h_height,y_HatOrigin-h_width,h_height,h_width))



def ZbuttonGroup(color_left,color_right, color_center):
    pygame.draw.circle(DashScreen,color_left,(x_ZOrigin-Z_radius-2*L1_R1_radius,y_ZOrigin),L1_R1_radius)
    pygame.draw.circle(DashScreen,color_right,(x_ZOrigin+Z_radius+2*L1_R1_radius,y_ZOrigin),L1_R1_radius)
    pygame.draw.circle(DashScreen,color_center,(x_ZOrigin,y_ZOrigin),Z_radius)

def Button_L1(color):
    pygame.draw.circle(DashScreen,color,(x_ZOrigin-Z_radius-2*L1_R1_radius,y_ZOrigin),L1_R1_radius)

def Button_R1(color):
    pygame.draw.circle(DashScreen,color,(x_ZOrigin+Z_radius+2*L1_R1_radius,y_ZOrigin),L1_R1_radius)


def main():
    global running
    Dashboard()
    while (running):
        #BUTTONS AND TRIGGERS EXAMPLE
        Button_B(green)
        Button_L(green)
        ZbuttonGroup(green,gray,gray)
        TrigL_Sig(red)
        TrigR_Sig(green)
        #HAT EXAMPLE
        HatY(gray,green)
        HatX(red,gray)
        #JOYSTICK EXAMPLES
        JStick_1Y(40,20)
        JStick_1X(10,40)
        JStick_2Y(20,40)
        JStick_2X(40,10)        
        #SENSORS EXAMPLE
        SENSOR_1_VALUE(green,0.2)
        SENSOR_2_VALUE(green,0.8)
        SENSOR_3_VALUE(red,102)
        pygame.display.update()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("QUIT")
                running = False
                pygame.quit()

    
  

if __name__ == '__main__' :
    main()

