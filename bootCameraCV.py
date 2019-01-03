import MulticameraSetupOpenCV
import time
import os

def set_dir(directory):
    '''check if a dir exists, if not... make it'''
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)

start_time = time.time()

record_length = 14 #hrs
record_length = record_length*60*60 #time in seconds

experiment_name = "open_CV_test_no_max"
directory = os.path.join("/media/pi/SamsungT5", experiment_name)

n = 4 #number of cameras

#directory = "/media/pi/VOLES1/Firstbond2/"+experiment_name

set_dir(directory)
#directory = "/media/pi/
#run the main process and start acquiring those sweet sweet images
folder_num = len([folder for folder in os.listdir(directory)])

if folder_num == 0:
    MulticameraSetupOpenCV.main(directory+"/"+str(folder_num), break_time = start_time+record_length,
                          num_cameras = n)

while time.time()-start_time < record_length:
    time.sleep(n)
    folder_num += 1
    print("new folder %i"%folder_num)
    MulticameraSetupOpenCV.main(directory+"/"+str(folder_num), break_time = start_time+record_length,
                          num_cameras = n)





