import serial
import math
import numpy as np
import time
import matplotlib.pyplot as plt
from scipy import signal

#-------------------------------------------------------------------------------#
def butter_highpass(cutoff, fs, order=3): # high pass filter in library scipy
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=3):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

#-------------------------------------------------------------------------------#
def update_window(window, az, window_size): 

    if (len(window) == window_size): # if the size of window is equal to window size, eliminate the first elements of each lists
        del window[0]

    window.append(az)

#-------------------------------------------------------------------------------#

def main():
    
    # define window lists. Use only "az" data. window size is 20.
    window = []
    window_size = 20

    # variables for serial communication
    com = "COM4"
    baud = 115200
    x = serial.Serial(com, baud, timeout = 0.1)

    time_limit = 0.1 # 20/60 seconds for one impact
    previous_gesture = -1
    current_gesture = -1

    already_detected = False
    start_time = time.time() # 

    threshold = 0.1 # threshold to identify effect
    cutoff = 10.
    printing_number = 1

    while x.isOpen() is True:
        data = str(x.readline().decode('utf-8')).rstrip()
        
        if data != '':
            az = float(data)
            update_window(window, az, window_size)

            
            if ( len( window ) < window_size ):
                continue
            
            # apply HPF to window data
            Fs = 210
            hpf = butter_highpass_filter(window, cutoff, Fs)
            value = max(abs(max(hpf)), abs(min(hpf)))

            if (value > threshold):
                current_gesture = 1 # impact is occured
            else:
                current_gesture = -1

            # print "impacte detected" when impact is detected
            if (current_gesture != previous_gesture and (not already_detected)):
                if (current_gesture != 0):
                    print("Impact %d Detected!" %(printing_number))
                    printing_number += 1

            if (current_gesture != previous_gesture):
                already_detected = True
                start_time = time.time()
                    

            if ((time.time() - start_time) > time_limit ):
                already_detected = False
                
            previous_gesture = current_gesture
            
            
        

main()