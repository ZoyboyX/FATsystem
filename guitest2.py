# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import time

def select_image():
    # grab a reference to the image panels
    global panelA

    # open a file chooser dialog and allow the user to select an input
    # image
    capture = cv2.VideoCapture(0)
    time.sleep(1)
    width = int(capture.get(3))
    height = int(capture.get(4))
    size = (width, height)
    outfile = cv2.VideoWriter("outfile.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, size)
    while (capture.isOpened()):
        val, frame = capture.read()
        image = frame
        cv2.waitKey(1000)
        outfile.write(frame)
        #cv2.imshow('vidio', frame)
        # load the image from disk, convert it to grayscale, and detect
        # edges in it
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # convert the images to PIL format...
        image = Image.fromarray(image)

        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)
        if panelA is None:
            # the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)
        else:
            # update the pannels
            panelA.configure(image=image)
            panelA.image = image
        cv2.waitKey(1)
        outfile.write(frame)

# initialize the window toolkit along with the two image panels
root = Tk()
panelA = None

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Start", command=select_image)
btn2 = Button(root, text="Stop", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
btn2.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

# kick off the GUI
root.mainloop()