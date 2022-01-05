import cv2
import mediapipe as mp
import time
from threading import Thread

camera_num = 2
exit_bit = False


class WebcamVideoStream:
    stream = None

    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        self.stream.set(cv2.CAP_PROP_EXPOSURE, 77)
        self.stream.set(cv2.CAP_PROP_BRIGHTNESS, 154)
        self.stream.set(cv2.CAP_PROP_GAIN, 106)
        self.stream.set(cv2.CAP_PROP_FOCUS, 0)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.stream.set(cv2.CAP_PROP_FPS, 30 / 1)
        print("fps", self.stream.get(cv2.CAP_PROP_FPS))
        print("fps", self.stream.get(cv2.CAP_PROP_BRIGHTNESS))

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=(), name='camera_thread').start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped

        while True:
            # if the thread indicator variable is set, stop the thread
            if exit_bit:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


if __name__ == '__main__':
    cap = WebcamVideoStream(src=camera_num).start()
    while True:
        ret, frame = (1, cap.read())
        cv2.imshow("Image Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit_bit = True
            print("[System] Quit")
            break
    cap.stop()
