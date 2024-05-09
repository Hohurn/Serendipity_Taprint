import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from scipy import signal


def butter_highpass(cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=3):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

#-------------------------------------------------------------------------------#
def FFT(arr):
    fs = len(arr) //30
    T = 1/fs
    amp = np.abs(np.fft.fft(arr))
    n = ( fs // 2 ) + 1 # for extracting only positive frequency
    print(fs)
    return amp[1:n] 

#-------------------------------------------------------------------------------#
def main():
    filename='data' 
    file_ext='.csv'
    
    uniq = 8 # number of data file "data(uniq).csv" in "Taprint_dataset" folder

    input_path = './Taprint_dataset/%s(%d)%s' %(filename,uniq,file_ext)

    while os.path.exists(input_path):  

        # get data from .csv file and store it to the list
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


        # draw the maximum abs value of highpass filtered value respect of window length 
        window_size = 20
        maximum = []
        cutoff = 10.
        for i in range(len(az) - window_size):

            temp = az[i : i + window_size]
        
            Fs = (window_size // (30*(window_size / len(az))))
            hpf = butter_highpass_filter(temp, cutoff, Fs)
            maximum.append(max(abs(max(hpf)), abs(min(hpf))))

        plt.plot(maximum)
        plt.show()
        
        # codes for drawing filter applied time series data
        """
        Fs = len(az) //30
        cutoff = 10.
        hpf1 = butter_highpass_filter(gx, cutoff, Fs)
        hpf2 = butter_highpass_filter(gy, cutoff, Fs)
        hpf3 = butter_highpass_filter(gz, cutoff, Fs)

        # original signal
        plt.subplot(3,1,1)
        plt.plot(gx, 'y', label='origin')
        plt.plot(hpf1, 'b', label='filtered data(gx)')
        plt.legend()

        # filtered ax data
        plt.subplot(3,1,2)
        plt.plot(gy, 'y', label='origin')
        plt.plot(hpf2, 'g', label='filtered data(gy)')
        plt.legend()

        # filtered ax data
        plt.subplot(3,1,3)
        plt.plot(gz, 'y', label='origin')
        plt.plot(hpf3, 'r', label='filtered data(gz)')


        plt.legend()
        plt.show() 
        """
        break
    
    


main()