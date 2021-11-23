import cv2
import time


one_shot = 1

list_2_SEND = [0,0,0,0,0,0,0,0]

list_1_RCVD = [0,0,0,0,0,0,0,0]

list_1_INIT = [0,0,0,0,0,0,0,0]
#list_2  = [0,0,0,0,0,0,0,0]

def storeToTwoFile(): 

    # Its important to use binary mode
    #print("STORETOTWO")
    TwoFile = open('TwoFile', 'w') 
    string_list_2_SEND = str(list_2_SEND)
    # source, destination 
    TwoFile.write(string_list_2_SEND)                   
    TwoFile.close()

def accessFromOneFile():
    OneFile = open('OneFile', 'r')
    try:
        string0 = OneFile.read()
        print('string0 = ',string0)
        string0_stripped = string0[1:len(string0)-1] #strip [ and ]
        string1 = string0_stripped
        #print(string1)
        string2 = string1.replace(","," ")
        #print(string2)
        listz = string2.split()#STRING INTO LIST OF SUBSTRINGS
        print('listz = ',listz)
        for j in range(8):
           list_1_RCVD[j] = int(listz[j])
           #list_1_RCVD[j] = list_1[j]
        #print(listz[0]-1)
    except:
        print('READ ERROR')
    OneFile.close()

def init_OneFile():
    global list_1_RCVD
    OneFile = open('OneFile', 'w') #w write   
    for i in range(8):
        list_1_INIT[i] = 0
        list_1_RCVD[i] = 0
        list_2_SEND[i] = 0
    OneFile.write(str(list_1_INIT))  
    OneFile.close() 

def do_run():
  while True:
    global one_shot  
    if (one_shot ==1):
        init_OneFile()
        one_shot = 0    
    print('list_1_RCVD =',list_1_RCVD)    
    storeToTwoFile()
    for j in range(8):
         list_2_SEND[j] = list_2_SEND[j] + 2
         #list_2[j] = list_2_SEND[j]     
    accessFromOneFile() 
    time.sleep(.3)
    if cv2.waitKey(1) == 27: #esc key ends loop. now can hit X on stream window   
                break


def main():
    do_run()
  

if __name__=="__main__":
  main()


