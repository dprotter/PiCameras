import RPi.GPIO as gp
import os
import time as time
import csv
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2


def main(directory, video_fname = 'video_out', break_time = 10, num_cameras = 4):
    
    #directory_max = 100
    set_dir(directory)
    
    num = 0

    number_of_cameras = num_cameras

    '''hz'''
    freq = float(1.0)
    interval = 1/(freq*number_of_cameras)
    #frame counter and log
    log = []

    #baseline setup
    setup_pins(num_cameras = number_of_cameras)
    set_pins(all_cams[0])

    global cam_stream
    with PiCamera() as camera:

        camera.iso = 800
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))

        loop = time.time()
        """stream = io.BytesIO()
        cam_stream.capture(stream, use_video_port = True)"""

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')



        h, w, = (640, 480)
        cv_writers = [cv2.VideoWriter(filename = video_fname+'_cam_%i'%i+".avi", fourcc=fourcc, fps = freq, apiPreference = 0, frameSize = (640,480)) for i in range(number_of_cameras)]

        with open('log %s'%time.asctime().replace(':','_'),'w', newline='') as csvfile:

            log_writer = csv.writer(csvfile)
            log_writer.writerow(['frame','cap_time','loop time', 'Error'])
            log = [0,0,0,0]
            for i, frame in enumerate(camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)):

                '''if i >= directory_max:
                    break'''
                if break_time < time.time():
                    print('times up')
                    break

                cv_writers[i%number_of_cameras].write(cv2.flip(frame.array,-1))

                log[0], log[1], log[3]=num, time.time()-loop, False
                try:
                    time.sleep(interval-(time.time()-loop))
                except:
                    log[3] = True
                #set pins for the next image
                cam_pins = set_pins(cam_pins = all_cams[(num+1)%number_of_cameras]) #setup the next cam_pins
                print("num: %i, next cam: %i"%(num, (num+1)%number_of_cameras))
                log[2] = time.time()-loop
                log_writer.writerow(log)
                loop = time.time()
                num+=1
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)
    for writer in cv_writers:
        writer.release()


def setup_pins(num_cameras = 6):
    gp.setwarnings(False)
    gp.setmode(gp.BOARD)

    gp.setup(7, gp.OUT)
    gp.setup(11, gp.OUT)
    gp.setup(12, gp.OUT)

    gp.setup(15, gp.OUT)
    gp.setup(16, gp.OUT)
    gp.setup(21, gp.OUT)
    gp.setup(22, gp.OUT)

    gp.output(11, True)
    gp.output(12, True)
    gp.output(15, True)
    gp.output(16, True)
    gp.output(21, True)
    gp.output(22, True)

    #this creates a dictionary of form {cam#: {pinnum: state, pinnum: state, pinnum: state}, }
    #this global dicitonary will be our iterable
    global all_cams
    all_cams = {}
    camera1 = {7:False, 15:True, 16:True, 11:False, 12:True}
    camera2 = {7:True, 15:True, 16:True,11:False, 12:True}
    camera3 = {7:False, 15:True, 16:True, 11:True, 12:False}
    camera4 = {7:True, 15:True, 16:True, 11:True, 12:False}
    camera5 = {7:False, 11:True, 12:True, 15:False, 16:True}
    camera6 = {7:True, 11:True, 12:True, 15:False, 16:True}
    cams = [camera1, camera2, camera3, camera4, camera5, camera6]

    for cam_num, camera in zip(list(range(0, num_cameras)), cams):
        all_cams[cam_num] = camera

def set_pins(cam_pins):
    for key in list(cam_pins.keys()):
        gp.output(key, cam_pins[key])

def set_dir(directory):
    '''check if a dir exists, if not... make it'''
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)

if __name__ == "__main__":
    main("/media/pi/SamsungT5/open_CV_test/0")
