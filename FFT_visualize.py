import serial
import math
import joblib
import numpy as np
import keyboard
import time
import matplotlib.pyplot as plt


def sign(a):
    if a < 0 :
        return -1
    else:
        return 1
#-------------------------------------------------------------------------------#
def two(a,b):
    return float(math.sqrt(a*a + b*b)*sign(a*b))

def three(a,b,c):
    return float(math.sqrt(a*a + b*b + c*c)*sign(a*b*c))

def xy(arr1, arr2):
    ret = []
    for i in range(len(arr1)):
        ret.append(two(arr1[i], arr2[i]))
    return ret

def xyz(arr1, arr2, arr3):
    ret = []
    for i in range(len(arr1)):
        ret.append(three(arr1[i], arr2[i], arr3[i]))
    return ret
#-------------------------------------------------------------------------------#
def max_index(list): # return the index of maximum value
    max = 0
    index = 0
    for i in range(len(list)):
        if (max < list[i]):
            max = list[i]
            index = i

    return index
#-------------------------------------------------------------------------------#
def avg(arr):
    ret = 0
    for i in arr:
        ret += i
    ret = ret / len(arr)
    return ret

def std(arr):
    avg2 = 0
    for i in arr:
        avg2 += i*i
    avg2 = avg2 / len(arr)
    return math.sqrt(abs(avg2 - avg(arr)*avg(arr)))

def FFT(arr):
    fs = len(arr)
    T = 1/fs
    amp = np.abs(np.fft.fft(arr))
    frequency = np.fft.fftfreq(len(amp),T)
    n = ( fs // 2 ) + 1 # for extracting only positive frequency
    AMP = amp[0:n]
    
    dominant_frequency = max_index(AMP)
    
    return dominant_frequency
#-------------------------------------------------------------------------------#
def update_window(A, G, split_data, window_size): 

    num = len(A[0])
    if (num == window_size): # if the size of window is 60, eliminate the first elements of each lists
        for i in range(len(A)):
            del A[i][0]
            del G[i][0]

    ax = float(split_data[0])
    ay = float(split_data[1])
    az = float(split_data[2])
    gx = float(split_data[3])
    gy = float(split_data[4])
    gz = float(split_data[5])

    A[0].append(ax)
    A[1].append(ay)
    A[2].append(az)
    A[3].append(three(ax,ay,az))
    A[4].append(two(ax,ay))
    A[5].append(two(ay,az))
    A[6].append(two(az,ax))

    G[0].append(gx)
    G[1].append(gy)
    G[2].append(gz)
    G[3].append(three(gx,gy,gz))
    G[4].append(two(gx,gy))
    G[5].append(two(gy,gz))
    G[6].append(two(gz,gx))
    
#-------------------------------------------------------------------------------#
def main():

    # draw real time graph
    """
    plt.ion()
    fig, ax = plt.subplots()

    time_data = []
    ax_data = []
    
    ay_data = []
    az_data = []
    gx_data = []
    gy_data = []
    gz_data = []
    """

    # define window lists
    A, G = [], [] # A[0]: ax, A[1]: ay, A[2]: az, A[3]: axyz, A[4]: axy, A[5]: ayz, A[6]: azx  same with list G is for gyroscope

    window_size = 20

    for i in range(7):
        A.append([])
    for i in range(7):
        G.append([])

    # load classifier parameters
    com = "COM4"
    baud = 115200
    x = serial.Serial(com, baud, timeout = 0.1)


    current_time = 0
    previous_time = 0

    
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
            #current_time = time.time()
            print([FFT(A[0]), FFT(A[1]), FFT(A[2]),FFT(A[3]), FFT(A[4]), FFT(A[5]),FFT(A[6]), FFT(G[0]), FFT(G[1]), FFT(G[2]), FFT(G[3]), FFT(G[4]), FFT(G[5]),FFT(G[6])])
            
            #previous_time = current_time
            #print(FFT(A[0]))
            """
            t = time.time()
            time_data.append(t)
            ax_data.append(FFT(A[0]))
            ay_data.append(FFT(A[1]))
            az_data.append(FFT(A[2]))
            gx_data.append(FFT(G[0]))
            gy_data.append(FFT(G[1]))
            gz_data.append(FFT(G[2]))
            
            
            
            ax.clear()
            ax.plot(time_data, ax_data, time_data, ay_data, time_data, az_data, time_data, gx_data, time_data, gy_data, time_data, gz_data)
            ax.set_xlim(t - 10, t)
            ax.set_ylim(0 , 10)

            plt.show()
            plt.pause(0.1)

            
            temp = []

            for i in range(7):
                temp.append(FFT(A[i]))
            for i in range(7):
                temp.append(FFT(G[i]))

            time_data.append(t)
            for i in range(7):
                A_data[i].append(temp[i])
                G_data[i].append(temp[i+7])


            ax.clear()
            ax.plot(time_data, A_data[0])
            ax.set_xlim(t - 10, t)
            ax.set_ylim(min(A_data[0]) , max(A_data[0]))

            plt.show()
            plt.pause(0.1)
            """

main()