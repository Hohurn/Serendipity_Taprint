import serial
import keyboard
import time
import csv
import os
 
filename='data' 
file_ext='.csv' 
foldername = 'Taprint_dataset'

uniq=1
output_path='./%s/%s(%d)%s' %(foldername,filename,uniq,file_ext)

sampling_time = 30

com = "COM4"
baud = 115200
x = serial.Serial(com, baud, timeout = 0.1)
while True:
    if keyboard.read_key() == "a":

        # generate file
        while os.path.exists(output_path):  
            uniq+=1
            output_path='./%s/%s(%d)%s' % (foldername,filename,uniq,file_ext) 
    

        with open(output_path, mode='a') as sensor_file:
            sensor_writer = csv.writer(sensor_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            sensor_writer.writerow(["ax", "ay", "az", "gx", "gy", "gz"])
        
        # perform countdown!
        state = [True, True, True, True, True, True]
        start = time.time()
        while x.isOpen() is True:
            data = str(x.readline().decode('utf-8')).rstrip()
        
            if data != '':
                split_data = data.split(',')
                if len(split_data) != 6:
                    continue
                #print(split_data)
                if (time.time() - start) > 2 and state[0] :
                    state[0] = False
                    print("Ready!")
                if (time.time() - start) > 3 and state[1] :
                    state[1] = False
                    print("333333333333333")
                if (time.time() - start) > 4 and state[2] :
                    state[2] = False
                    print("222222222222222")
                if (time.time() - start) > 5 and state[3] :
                    state[3] = False
                    print("111111111111111")
                if (time.time() - start) > 6 and state[4] :
                    state[4] = False
                    print("Start!")
                if (time.time() - start) > (5 + sampling_time) and state[5] :
                    state[5] = False
                    print("Finished!")
                    break

                if 6 < (time.time() - start) < (5 + sampling_time):
                    with open(output_path, mode='a') as sensor_file:
                        sensor_writer = csv.writer(sensor_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        sensor_writer.writerow([float(split_data[0]), float(split_data[1]), float(split_data[2]), float(split_data[3]), float(split_data[4]), float(split_data[5])])
    elif keyboard.read_key() == "x":
        break
