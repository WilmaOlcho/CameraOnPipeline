import tkinter as tk
from Sources.CanvasOCV import CanvasOCV
import cv2
from pathlib import Path
import time

class Window(tk.Frame):
    def __init__(self, pipeEnd, name = '', width = '', height = '', master = None):
        super().__init__(name = name, width = width, height = height, master = master)
        self.master = master
        self.CanvasOCV = CanvasOCV(master = self)
        self.pipe = pipeEnd
        self.Button = tk.Button(master = self, text = 'Capture', command = self.capture) 
        self.CanvasOCV.pack()
        self.Button.pack()
        self.pack()

    def capture(self):
        image = self.pipe.recv()
        cv2.imwrite(str(time.time()) + '.bmp',image)

    def update(self):
        super().update()
        self.CanvasOCV.set_imageOCV(self.pipe.recv())

class Gui(tk.Tk):
    def __init__(self, PipeEnd, Alive):
        super().__init__()
        self.Alive = Alive
        self.pipe = PipeEnd
        self.window = Window(self.pipe, width = 200, height = 200, master = self)
        self.refresh()
        self.Guiloop()

    def refresh(self):
        self.window.update()
        self.after(200, self.refresh)

    def Guiloop(self):
        while self.Alive:
            self.update()
           
