import csv

def main():

    file_num = 50

    saving_file_num = 1 # for the numbering of saved file name 

    for i in range(file_num):
        file_path = "./DataSet_1/data(%d).csv" %(i + 1)


        f = open(file_path, 'r')
        rdr = csv.reader(f)
        n = 1
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
        f.close()
        for i in range(10):
            saving_file_path = "./DataSet_4_separated/data(%d).csv" %(saving_file_num)
            f2 = open(saving_file_path, "w")
            writer = csv.writer(f2)

            for j in range(30):
                row = [ ax[ 4*i + j ], ay[ 4*i + j ], az[ 4*i + j ], gx[ 4*i + j ], gy[ 4*i + j ], gz[ 4*i + j ]] 
                writer.writerow(row)
            
            f2.close()

            saving_file_num += 1



    return 0



main()