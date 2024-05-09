import matplotlib.pyplot as plt
import csv



# this code makes the visual graph of each csv file and save it to each of folder

folder_num = 1 # number of gestrue(number of labels)
file_num = 10 # number of data of each gesture

for i in range (folder_num):
    #folder_name = './DataSet_%d' %(i + 1)
    folder_name = './Taprint_dataset'
    for j in range(file_num):
        file_path = '%s/data(%d).csv' %(folder_name, j + 1)
        f = open(file_path, 'r')
        rdr = csv.reader(f)

        n = 1
        ax, ay, az, gx, gy, gz = [], [], [], [], [], []
        for line in rdr:
            if (len(line) != 0 and n != 1):
                # make a plot for 6 axis sensor data
                ax.append(float(line[0]))
                ay.append(float(line[1]))
                az.append(float(line[2]))
                gx.append(float(line[3]))
                gy.append(float(line[4]))
                gz.append(float(line[5]))
            
            n = n + 1

        t = []
        for k in range(len(ax)):
            t.append(k + 1)
        print(i)
        #saving_folder_name = './DataSet_%d_visualized' %(i + 1)
        saving_folder_name = './Taprint_dataset_visualized'
        graph_name = '/data(%d)_graph.pdf' %(j + 1)

        path = saving_folder_name + graph_name
        plt.plot(t, ax, t, ay, t, az)
        plt.savefig(path, format='pdf')
        plt.clf()
        f.close()

