import cv2
import time


one_shot = 1

list_1_SEND = [0,0,0,0,0,0,0,0]

list_2_RCVD = [0,0,0,0,0,0,0,0]

#list_1 = [0,0,0,0,0,0,0,0]
list_2_INIT  = [0,0,0,0,0,0,0,0]

def storeToOneFile(): 

    # Its important to use binary mode
    #print("STORETOONE")
    OneFile = open('OneFile', 'w') 
    string_list_1_SEND = str(list_1_SEND)
    # source, destination 
    OneFile.write(string_list_1_SEND)                   
    OneFile.close()

def accessFromTwoFile():
    TwoFile = open('TwoFile', 'r')
    try:
        string0 = TwoFile.read()
        print('string0 = ',string0)
        string0_stripped = string0[1:len(string0)-1] #strip [ and ]
        string1 = string0_stripped
        #print(string1)
        string2 = string1.replace(","," ")
        #print(string2)
        listz = string2.split()#STRING INTO LIST OF SUBSTRINGS
        print('listz = ',listz)
        for j in range(8):
           list_2_RCVD[j] = int(listz[j])
           #list_2_RCVD[j] = list_2[j]
        print('list_2 = ',list_2_RCVD)   
        #print(listz[0]-1)
    except:
        print('READ ERROR')
    TwoFile.close()

def init_TwoFile():
    global list_2_RCVD
    TwoFile = open('TwoFile', 'w') #w write   
    for i in range(8):
        list_2_INIT[i] = 0
        list_2_RCVD[i] = 0
        list_1_SEND[i] = 0
    TwoFile.write(str(list_2_INIT))  
    TwoFile.close() 

def do_run():
  while True:
    global one_shot  
    if (one_shot ==1):
        init_TwoFile()
        one_shot = 0    
    print('list_2_RCVD =',list_2_RCVD)    
    storeToOneFile()
    for j in range(8):
         list_1_SEND[j] = list_1_SEND[j] + 10
         #list_1[j] = list_1_SEND[j]     
    accessFromTwoFile() 
    time.sleep(.3)
    if cv2.waitKey(1) == 27:  #esc key ends loop. now can hit X on stream window     
                print('break')
                #break

def main():
    do_run()

if __name__=="__main__":
  main()


