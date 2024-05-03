import matplotlib.pyplot as plt
import csv
#--------------------------------------------------------------------#
def quick_sort(arr):
    def sort(low, high):
        if high <= low:
            return

        mid = partition(low, high)
        sort(low, mid - 1)
        sort(mid, high)

    def partition(low, high):
        pivot = arr[(low + high) // 2][1]
        while low <= high:
            while arr[low][1] > pivot:
                low += 1
            while arr[high][1] < pivot:
                high -= 1
            if low <= high:
                arr[low], arr[high] = arr[high], arr[low]
                low, high = low + 1, high - 1
        return low

    return sort(0, len(arr) - 1)
#--------------------------------------------------------------------#
def make_zero_list(list):
    ret = []
    starting_index = 0
    num_successive_zeros = 0
    num_successive_ones = 0
    for i in range(len(list)):
 
        if (i == 0):
            if (list[i] == 0):
                starting_index = i
                num_successive_zeros += 1
            else:
                num_successive_ones += 1

        elif (i < (len(list) - 1) and i != 0):

            if(list[i] == 0):
                if (num_successive_zeros == 0):
                    starting_index = i
                    num_successive_ones = 0
                num_successive_zeros += 1
            else:
                if (num_successive_ones == 0):
                    ret.append((starting_index, num_successive_zeros))
                    num_successive_zeros = 0

                num_successive_ones += 1
        else:
            if (list[i] == 0):
                if (num_successive_zeros == 0):
                    ret.append((i, 1))
                else:
                    ret.append((starting_index, num_successive_zeros + 1))
            else:
                if (num_successive_ones == 0):
                    ret.append((starting_index, num_successive_zeros))
            
    return ret


def final_filter(zero_list, total_length, num_gesture):
    ret = []
    for i in range(total_length):
        ret.append(500)
    for i in range(num_gesture + 1):
        for j in range(zero_list[i][1]):
            ret[zero_list[i][0] + j] = -500

    return ret
#--------------------------------------------------------------------#
folder_num = 5 # number of gestrue(number of labels)
file_num = 525 # number of data of each gesture

threshold = 100 # threshold for value

num_gesture = 7

for i in range(folder_num):
    if(i != 4):
        continue
    folder_name = './DataSet_%d_separated' %(i + 1)
    for j in range(file_num):
        file_path = '%s/data(%d).csv' %(folder_name, j + 1)
        f = open(file_path, 'r')
        rdr = csv.reader(f)

        n = 2 # change this value to 1 when the first row of the csv file is ax, ay, az, gx, gy, gz

        ax, ay, az, gx, gy, gz = [], [], [], [], [], []
        for line in rdr:
            if (len(line) != 0 and n != 1):
                # make a plot for 6 axis sensor data
                x1 = float(line[0])
                x2 = float(line[1])
                x3 = float(line[2])
                x4 = float(line[3])
                x5 = float(line[4])
                x6 = float(line[5])

                ax.append(x1)
                ay.append(x2)
                az.append(x3)
                gx.append(x4)
                gy.append(x5)
                gz.append(x6)

            n = n + 1

        t = []
        for k in range(len(ax)):
            t.append(k + 1)

        saving_folder_name = './DataSet_%d_separated_visualized' %(i + 1)
        graph_name = '/data(%d)_graph.pdf' %(j + 1)
        path = saving_folder_name + graph_name
        plt.plot(t, ax, t, ay, t, az, t, gx, t, gy, t, gz)
        plt.savefig(path, format='pdf')
        plt.clf()
        f.close()

