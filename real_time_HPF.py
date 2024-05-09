import serial
import math
import numpy as np
import time
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------#
def update_window(window, split_data, window_size): 

    if (len(window) == window_size): # if the size of window is 60, eliminate the first elements of each lists
        for i in range(len(window)):
            del window[0]
        

    ax = float(split_data[0])
    ay = float(split_data[1])
    az = float(split_data[2])
    gx = float(split_data[3])
    gy = float(split_data[4])
    gz = float(split_data[5])

#-------------------------------------------------------------------------------#
def define_label(label):
    ret = 0
    if (label == 0):
        ret = 1
    else:
        ret = 0
    return ret
#-------------------------------------------------------------------------------#
def is_detected(probability):
    if (probability > 8):
        return True
    else:
        return False
#-------------------------------------------------------------------------------#

def main():
    
    # define window lists. Use only "az" data. window size is 20.
    window = []
    window_size = 20

    # load classifier parameters
    com = "/dev/cu.usbmodem1101"
    baud = 115200
    x = serial.Serial(com, baud, timeout = 0.1)

    time_limit = 0.333 # 20/60 seconds for one impact
    previous_gesture = -1
    current_gesture = -1

    already_detected = False
    start_time = time.time()

    while x.isOpen() is True:
        data = str(x.readline().decode('utf-8')).rstrip()
        
        if data != '':
            split_data = data.split(',')
            if len(split_data) != 6:
                continue
            update_window(A, G, split_data, window_size)
            if ( len( A[0] ) < window_size ):
                continue
            #print(split_data)
            # make total five sliding window and make a decision by using SVM
            
            
            final_window = total_features(A, G, window_size)
            temp = np.array(final_window)
            current_gesture = int(clf.predict(temp.reshape(1,-1))[0])
               
            #print(current_gesture)
            
            # print detection
            #print(already_detected)
            if (current_gesture != previous_gesture and (not already_detected)):
                if (current_gesture != 0):
                    print("Impact Detected!")

            if (current_gesture != previous_gesture):
                already_detected = True
                start_time = time.time()
                    

            if ((time.time() - start_time) > 1 ):
                already_detected = False
                

            previous_gesture = current_gesture
            
            
            


main()