import tkinter
from PIL import ImageTk, Image

class ScrollableImage(tkinter.Canvas):
    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self['highlightthickness'] = 0
        self.propagate(0)  # wont let the scrollbars rule the size of Canvas
        self.create_image(0,0, anchor='s', image=self.image)
        # Vertical and Horizontal scrollbars
        self.v_scroll = tkinter.Scrollbar(self, orient='vertical')
        self.h_scroll = tkinter.Scrollbar(self, orient='horizontal')
        self.v_scroll.pack(side='right', fill='y')
        self.h_scroll.pack(side='bottom', fill='x')
        # Set the scrollbars to the canvas
        self.config(xscrollcommand=self.h_scroll.set,
                yscrollcommand=self.v_scroll.set)
        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.yview)
        self.h_scroll.config(command=self.xview)
        # Assign the region to be scrolled
        self.config(scrollregion=self.bbox('all'))

        self.focus_set()
        #self.bind_class(self, "<MouseWheel>", self.mouse_scroll)


    # def mouse_scroll(self, evt):
    #     if evt.state == 0 :
    #         # self.yview_scroll(-1*(evt.delta), 'units') # For MacOS
    #         self.yview_scroll( int(-1*(evt.delta/120)) , 'units') # For windows
    #     if evt.state == 1:
    #         # self.xview_scroll(-1*(evt.delta), 'units') # For MacOS
    #         self.xview_scroll( int(-1*(evt.delta/120)) , 'units') # For windows

# --------- Example and testing ---------
# This will be true only if the file is not imported as a package.
if __name__ == "__main__":

    def getout():
        raise SystemExit

    def displayresults():
        x = 1

    def saveresults():
        x = 1

    def addclick():
        x = 2

    root = tkinter.Tk()
    img = Image.open('final.jpg')
    #root.state("zoomed")
    img = ImageTk.PhotoImage(img)
    root.winfo_toplevel().title("Results")

    mainthing = ScrollableImage(root, image=img, width=700, height=img.height())
    mainthing.pack(anchor='n')

    btn_exit = tkinter.Button(root, text="Exit", width=50, command=getout, bg="red")
    btn_exit.pack(anchor='s', expand=True)

    btn_displayresults = tkinter.Button(root, text="Show Results", width=50, command=displayresults, bg="blue")
    btn_displayresults.pack(anchor='s', expand=True)

    btn_saveresults = tkinter.Button(root, text="Save", width=50, command=saveresults, bg="yellow")
    btn_saveresults.pack(anchor='s', expand=True)

    btn_addclick = tkinter.Button(root, text="Add Result", width=50, command=saveresults, bg="green")
    btn_addclick.pack(anchor='s', expand=True)

    root.mainloop()

