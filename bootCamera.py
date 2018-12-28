import MulticameraSetup
import time
import os

def set_dir(directory):
    '''check if a dir exists, if not... make it'''
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)

start_time = 1542396650.7324896

record_length = 24.5 #hrs
record_length = record_length*60*60 #time in seconds

experiment_name = "11_16_18 second bond 3 cams"
directory = "/media/pi/VOLES1/"+ experiment_name

n = 3 #number of cameras

#directory = "/media/pi/VOLES1/Firstbond2/"+experiment_name

set_dir(directory)
#directory = "/media/pi/
#run the main process and start acquiring those sweet sweet images
folder_num = len([folder for folder in os.listdir(directory)])

if folder_num == 0:
    MulticameraSetup.main(directory+"/"+str(folder_num), break_time = start_time+record_length,
                          num_cameras = n)

while time.time()-start_time < record_length:
    time.sleep(n)
    folder_num += 1
    print("new folder %i"%folder_num)
    MulticameraSetup.main(directory+"/"+str(folder_num), break_time = start_time+record_length,
                          num_cameras = n)





