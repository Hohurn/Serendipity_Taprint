import matplotlib.pyplot as plt
import csv
#--------------------------------------------------------------------#
def sort_by_length(arr):
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
def sort_by_index(arr):
    def sort(low, high):
        if high <= low:
            return

        mid = partition(low, high)
        sort(low, mid - 1)
        sort(mid, high)

    def partition(low, high):
        pivot = arr[(low + high) // 2][0]
        while low <= high:
            while arr[low][0] < pivot:
                low += 1
            while arr[high][0] > pivot:
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

#--------------------------------------------------------------------#
def final_filter(zero_list, total_length, num_gesture):
    ret = []
    for i in range(total_length):
        ret.append(500)
    for i in range(num_gesture + 1):
        for j in range(zero_list[i][1]):
            ret[zero_list[i][0] + j] = -500

    return ret

#--------------------------------------------------------------------#

def main():
    #--------------------------------------------------------------------#
    ### hyper parameters ###

    N = 7 # number of gesture in one series dataset
    alpha_value = 5 # number of data augmentation number --> series data should be seperated into 7*5=35 data
    threshold = 50 # threshold for removing near 0 values

    #--------------------------------------------------------------------#

    alpha_list = [-2,-1,0,1, 2]

    num_saved_data = 1 # number of current saving data (variable for saving gestures)
    num_serier_data = 15 # number of listed data(series data set total gesture number is 15*7 = 35)
    
    for num in range(num_serier_data):
        file_path = "./DataSet_3/data(%d).csv" %(num + 1)


        f = open(file_path, 'r')
        rdr = csv.reader(f)
        n = 1
        ax, ay, az, gx, gy, gz = [], [], [], [], [], []
        total, digital = [], []
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
                squared = x1*x1 + x2*x2 + x3*x3 + x4*x4 + x5*x5 + x6*x6
                total.append(squared)
                if (squared > threshold):
                    digital.append(1)
                else:
                    digital.append(0)

            n = n + 1
        f.close()
        # make time domain list (optional)
        t = []
        for k in range(len(ax)):
            t.append(k + 1)

        a = make_zero_list(digital)
        sort_by_length(a)
        longest_zero_lists = a[0 : (N + 1)]
        filter = final_filter(longest_zero_lists, len(ax), N)

        """
        saving_folder_name = './DataSet_3_seperated_visualized'
        graph_name = '/data(%d)_graph.pdf' %(num + 1)
        path = saving_folder_name + graph_name
        plt.plot(t, ax, t, ay, t, az, t, gx, t, gy, t, gz, t, total, t, filter)
        plt.savefig(path, format='pdf')
        plt.clf()
        """

        sort_by_index(longest_zero_lists)
        print(longest_zero_lists)

        for i in range(len(longest_zero_lists) - 1):
            for alpha in alpha_list:
                start = ((longest_zero_lists[i][0] + longest_zero_lists[i][1] +longest_zero_lists[i+1][0]) // 2) - 14 + alpha
                # length = longest_zero_lists[i+1][0] - longest_zero_lists[i][0] - longest_zero_lists[i][1] extract only ones range(length is various)
                length = 30

                # save seperated data to each file
                saving_file_path = "./DataSet_5_separated/data(%d).csv" %(num_saved_data)
                f = open(saving_file_path, "w")
                writer = csv.writer(f)
            
                for k in range(length):
                    values = [ax[start + k], ay[start + k], az[start + k], gx[start + k], gy[start + k], gz[start + k]]
                    writer.writerow(values)
                f.close()

                num_saved_data += 1
    return 0

#--------------------------------------------------------------------#

main()