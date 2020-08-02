import tkinter
from tkinter import messagebox
import cv2
import PIL.Image
import PIL.ImageTk
import keyboard
import time
import numpy as np
from random import randint
from playsound import playsound


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.go = True
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = cv2.VideoCapture(0)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=self.vid.get(3), height=self.vid.get(4))
        self.width = self.vid.get(3)
        self.height = self.vid.get(4)
        self.canvas.pack()

        # Button that starts recording
        self.btn_start = tkinter.Button(window, text="Start", width=50,
                                        command=self.start, bg="green")
        self.btn_start.pack(anchor=tkinter.CENTER, expand=True)
        self.endit = tkinter.Label(window, text="Press e to End")
        self.endit.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_exit = tkinter.Button(window, text="Exit", width=50, command=self.getout, bg="red")
        self.btn_exit.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()

        self.window.mainloop()

    def start(self):
        if messagebox.askyesno('Ready', 'Is Everyone set?'):
            # randomdelay = randint(1000, 1500)
            # cv2.waitKey(randomdelay)
            # start = time.perf_counter_ns()
            # playsound('gun.mp3')
            # end = time.perf_counter_ns()
            # shoottime = ((end - start) / (1000000000))

            width = int(self.vid.get(3))
            height = int(self.vid.get(4))
            size = (width, height)
            outfile = cv2.VideoWriter(
                "outfile.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, size)
            while (self.go):
                val, frame = self.vid.read()
                cv2.waitKey(1)
                outfile.write(frame)
                cv2.imshow('Raw input', frame)
                if (keyboard.is_pressed('e')):
                    break

            self.vid.release()
            outfile.release()
            cv2.destroyAllWindows()

            toprocess = cv2.VideoCapture('outfile.avi')
            framecount = int(toprocess.get(cv2.CAP_PROP_FRAME_COUNT))
            finalimage = np.zeros((height, framecount, 3), np.uint8)
            middle = int(width / 2)
            for x in range(0, framecount - 1):
                val, frame = toprocess.read()
                cv2.waitKey(1)
                for y in range(0, height):
                    blue = frame[y, middle, 0]
                    green = frame[y, middle, 1]
                    red = frame[y, middle, 2]
                    finalimage[y, x] = [blue, green, red]
            cv2.imwrite("final.jpg", finalimage)

            self.vid = cv2.VideoCapture(0)
            cv2.waitKey(10)

        else:
            return

    def getout(self):
        raise SystemExit

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        middle = int(self.width / 2)
        for x in range(0, int(self.height)):
            frame[x, middle] = [0, 0, 0]

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Create a window and pass it to the Application object
App(tkinter.Tk(), "Sprint App")
