from tensorflow import keras
import csv
import numpy as np
import serial
import time
import matplotlib.pyplot as plt

def softmax(A, B): # A is target probability
    x = np.exp(A)
    y = np.exp(B)
    ret = x/(x+y)
    return ret
#-------------------------------------------------------------------------------#
def update_window(window_list, data, window_size): 
    num = len(window_list)
    if (num == window_size): # if the size of window is 60, eliminate the first elements of each lists
        del window_list[0]

    window_list.append(data)
    

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
    # draw graph
    plt.ion()
    fig, ax = plt.subplots()
    x_data = []
    y_data = []
    y1_data = []
    y2_data = []

    # define window lists
    A = [] 

    window_size = 30

    # load classifier parameters
    model = keras.models.load_model('revised_cnn_parameters.keras')
    com = "COM4"
    baud = 9600
    x = serial.Serial(com, baud, timeout = 0.1)

    while x.isOpen() is True:
        data = str(x.readline().decode('utf-8')).rstrip()
        if data != '':
            split_data = data.split(',')
            if len(split_data) != 6:
                continue
            update_window(A, split_data, window_size)
            if ( len( A ) < window_size ):
                continue
            
            A = np.asarray([A]).astype('float32')
       
            result_array = model.predict(A)
            softmax_result = softmax(result_array[0][1], result_array[0][0])
            print(softmax_result)
            
            gx = time.time()
            gy = softmax_result
            gy1 = result_array[0][1]
            gy2 = result_array[0][0]

            x_data.append(gx)
            y_data.append(gy)
            y1_data.append(gy1)
            y2_data.append(gy2)

            ax.clear()
            ax.plot(x_data,y1_data, x_data, y2_data)

            ax.set_xlim(gx - 10, gx)
            ax.set_ylim(min(y1_data+y2_data) , max(y1_data+y2_data))

            plt.show()
            plt.pause(0.1)
            
            A = np.squeeze(A, axis = 0)
            A = list(A)

            
            
            


main()


















