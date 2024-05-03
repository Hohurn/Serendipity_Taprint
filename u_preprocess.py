import csv
import os
import math
import numpy as np

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
    avg2 = 0.0
    for i in arr:
        avg2 += i*i
    avg2 = avg2 / float(len(arr))
    return math.sqrt(abs(avg2 - avg(arr)*avg(arr)))

def FFT(arr):
    fs = len(arr)
    T = 1/fs
    amp = np.abs(np.fft.fft(arr))
    frequency = np.fft.fftfreq(len(amp),T)
    n = ( fs // 2 ) + 1 # for extracting only positive frequency
    AMP = amp[0:n]
    FREQ = frequency[0:n]
    print(len(arr))
    #print(AMP)
    #print(FREQ)  #check whether this list elements are all positive by removing this comment
    AMP1 = AMP.copy()
    quick_sort(AMP1)
    index_list = []
    for i in range(10): # procedure to get the index of lowest frequency get 10 dominant frequency
        a = len(AMP) - i - 1
        for j in range(len(AMP)):
            if(AMP[j] == AMP1[a]):
                if j in index_list:
                    continue
                else:
                    index_list.append(j)
    Dominant_freq = []
    for i in range(len(index_list)):
        Dominant_freq.append(FREQ[index_list[i]])
    quick_sort(Dominant_freq)
    
    return Dominant_freq[0:5] # get lowest 5 frequecy from 
#-------------------------------------------------------------------------------#
def extract_features(arr):
    features = []
    features.append(float(avg(arr))) # mean value
    features.append(float(std(arr))) # standard deviation value
    sorted = arr.copy()
    features.append(sorted[0]) # min
    features.append(sorted[int(len(sorted) * 0.25)]) # 1/4 quantile
    features.append(sorted[int(len(sorted) * 0.5)]) # 2/4 quantile
    features.append(sorted[int(len(sorted) * 0.75)]) # 3/4 quantile
    features.append(sorted[-1]) # max
 
    fft = FFT(arr) # add FFT values 

    return features + fft
#-------------------------------------------------------------------------------#
def main():
    filename='data' 
    file_ext='.csv'
    folder_number = 4
    uniq = 1
    input_path = './DataSet_%d_separated/%s(%d)%s' %(folder_number,filename,uniq,file_ext)

    while os.path.exists(input_path):  

        f = open(input_path,'r')
        rdr = csv.reader(f)

        ax, ay, az = [], [], []
        
        gx, gy, gz = [], [], []
        

        a = 0
        for line in rdr:
            if len(line) != 0 and a != 0:
                ax.append(float(line[0]))
                ay.append(float(line[1]))
                az.append(float(line[2]))
                gx.append(float(line[3]))
                gy.append(float(line[4]))
                gz.append(float(line[5]))
            a += 1

        axyz = xyz(ax, ay, az)
        axy = xy(ax, ay)
        ayz = xy(ay, az)
        azx = xy(az, ax)

        gxyz = xyz(gx, gy, gz)
        gxy = xy(gx, gy)
        gyz = xy(gy, gz)
        gzx = xy(gz, gx)

        f.close()
        linear_features = extract_features(ax) + extract_features(ay) + extract_features(az) + extract_features(axyz) + extract_features(axy) + extract_features(ayz) + extract_features(azx)
        angular_features = extract_features(gx) + extract_features(gy) + extract_features(gz) + extract_features(gxyz) + extract_features(gxy) + extract_features(gyz) + extract_features(gzx)
        total_features = linear_features + angular_features
        
        output_path = './final_dataset_%d.csv' %(folder_number)

        if uniq == 1: # control the writer mode for writing to output file
            mode = 'w'
        else:
            mode = 'a'

        f = open(output_path, mode)
        writer = csv.writer(f)
        writer.writerow(total_features)

        input_path='./DataSet_%d_separated/%s(%d)%s' % (folder_number,filename,uniq,file_ext) 
        uniq+=1
    
    


main()