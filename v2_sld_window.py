import serial
import math
import joblib
import numpy as np
import keyboard
import time
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------#
def two(a,b):
    return float(math.sqrt(a*a + b*b))

def three(a,b,c):
    return float(math.sqrt(a*a + b*b + c*c))

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

def max_index(list): # return the index of maximum value
    max = 0
    index = 0
    for i in range(len(list)):
        if (max < list[i]):
            max = list[i]
            index = i

    return index
#-------------------------------------------------------------------------------#
def quick_sort(arr):
    def sort(low, high):
        if high <= low:
            return

        mid = partition(low, high)
        sort(low, mid - 1)
        sort(mid, high)

    def partition(low, high):
        pivot = arr[(low + high) // 2]
        while low <= high:
            while arr[low] < pivot:
                low += 1
            while arr[high] > pivot:
                high -= 1
            if low <= high:
                arr[low], arr[high] = arr[high], arr[low]
                low, high = low + 1, high - 1
        return low

    return sort(0, len(arr) - 1)
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
    amp = np.abs(np.fft.fft(arr))
    n = ( fs // 2 ) + 1 # for extracting only positive frequency
    AMP = amp[0:n]
    dominant_frequency = max_index(AMP)
    
    return dominant_frequency
#-------------------------------------------------------------------------------#
def extract_features(arr_source, length):
    arr = arr_source[(len(arr_source) - length) : -1]
    features = []
    features.append(int(avg(arr))) # mean value
    features.append(int(std(arr))) # standard deviation value
    sorted = arr.copy()
    quick_sort(sorted)
    features.append(sorted[0]) # min
    features.append(sorted[int(len(sorted) * 0.25)]) # 1/4 quantile
    features.append(sorted[int(len(sorted) * 0.5)]) # 2/4 quantile
    features.append(sorted[int(len(sorted) * 0.75)]) # 3/4 quantile
    features.append(sorted[-1]) # max
 
    features.append(FFT(arr)) # add FFT values dominant frequency value

    return features
#-------------------------------------------------------------------------------#
def total_features(A, G, length):
    ret = []
    for i in range(len(A)):
        ret += extract_features(A[i], length)
    for i in range(len(G)):
        ret += extract_features(G[i], length)

    return ret
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
    A[3].append(three(ax, ay, az)) # axyz
    A[4].append(two(ax, ay)) # axy
    A[5].append(two(ay, az)) # ayz
    A[6].append(two(az, ax)) # ayz

    G[0].append(gx)
    G[1].append(gy)
    G[2].append(gz)
    G[3].append(three(gx, gy, gz)) # gxyz
    G[4].append(two(gx, gy)) # gxy
    G[5].append(two(gy, gz)) # gyz
    G[6].append(two(gz, gx)) # gzx

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
    
    # define window lists
    A, G = [], [] # A[0]: ax, A[1]: ay, A[2]: az, A[3]: axyz, A[4]: axy, A[5]: ayz, A[6]: azx  same with list G is for gyroscope

    window_size = 30

    for i in range(7):
        A.append([])
    for i in range(7):
        G.append([])

    # load classifier parameters
    clf = joblib.load('parameters.joblib')
    com = "COM4"
    baud = 115200
    x = serial.Serial(com, baud, timeout = 0.1)
    previous_gesture = -1
    current_gesture = -1

    #delta_t = 7

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