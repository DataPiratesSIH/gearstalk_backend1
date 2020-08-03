from threading import Thread
import cv2
import shutil

class RTSPVideoWriterObject(object):
    def __init__(self, src=0):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)

        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))
        self.name = '0'

        # Set up codec and output video settings
        self.codec = cv2.VideoWriter_fourcc('M','J','P','G')
        self.output_video = cv2.VideoWriter(f'{self.name}.avi', self.codec, 30, (self.frame_width, self.frame_height))

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
    
    def update_file(self, name):
        self.output_video = cv2.VideoWriter(f'{name}.avi', self.codec, 30, (self.frame_width, self.frame_height))


    def save_frame(self):
        self.output_video.write(self.frame)

    def remove_frame(self, filename):
        shutil.rm(filename)

if __name__ == '__main__':
    rtsp_stream_link = 'http://192.168.0.100:8080/video'
    video_stream_widget = RTSPVideoWriterObject(rtsp_stream_link)
    while True:
        if count % 30 == 0 and count != 0:
            video_stream_widget.update_file(str(count))

        try:
            video_stream_widget.save_frame()
        except AttributeError:
            print(AttributeError)
        count +=1
