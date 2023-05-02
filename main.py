import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import cv2
from PIL import Image,ImageTk
import datetime


class App:
    root = Tk()
    def __init__(self):
        App.root.geometry("1080x720")
        App.root.configure(bg="white")
        # App.root.columnconfigure(0,weight=1)
        # App.root.columnconfigure(1,weight=50)
        # self.f1 = LabelFrame(App.root)
        # self.f1.grid()
        App.root.rowconfigure(0,weight=60)
        App.root.rowconfigure(1,weight=1)
        App.root.rowconfigure(2,weight=15)
        App.root.rowconfigure(3,weight=30)
        App.root.columnconfigure(0,weight=50)
        App.root.columnconfigure(1,weight=25)
        App.root.columnconfigure(4,weight=25)

    left_space = tk.Label(root)
    left_space.configure(bg="black")
    left_space.grid(row=0,column=0,rowspan=2,sticky=[EW,NS])

    bottom_space = tk.Label(root)
    #bottom_space.configure(bg="red")
    bottom_space.grid(row=2,column=0,columnspan=5,sticky=[EW,NS])

    video_frame = TkinterVideo(root,keep_aspect=True,scaled=True)
    video_frame.grid(row=0,column=1,columnspan=5,sticky=[EW,NS])

    start_time = tk.Label(root, text = str(datetime.timedelta(seconds=0)))
    start_time.grid(row=3,column=0,sticky=[W,N])

    end_time = tk.Label(root,text= str(datetime.timedelta(seconds=0)))
    end_time.grid(row=3,column=4,sticky=[E,N])



    def openFile():
        file = filedialog.askopenfile(mode="r",filetypes=[('Video Files',['*.mp4','*.mov'])])
        if file is not None:
            global filename
            filename = file.name
            App.video_frame.load(r"{}".format(filename))
    def playFile():
        App.video_frame.play()
    
    def stopFile():
        App.video_frame.stop()
    
    def pauseFile():
        App.video_frame.pause()

    def update_duration(event):
        duration = App.video_frame.video_info()["duration"]

        App.end_time["text"] = str(datetime.timedelta(seconds=duration))
        App.progress_slider["to"] = duration

    def update_scale(event):
        App.progress_value.set(App.video_frame.current_duration())
        App.start_time["text"] = str(datetime.timedelta(seconds=App.video_frame.current_duration()))

    def seek(value):
        App.video_frame.seek(int(value))

    def skip(value:int):
        App.video_frame.seek(int(App.progress_slider.get()+value))
        App.progress_value.set(App.progress_slider.get()+value)

    # def play_pause():
    #     if App.video_frame.is_paused():
    #         App.video_frame.play()
    #         play_pause_btn["text"] = "Pause"
    #     else:
    #         App.video_frame.pause()
    #         play_pause_btn["text"] = "Play"

    def video_ended(event):
        App.progress_slider.set(App.progress_slider["to"])
        #play_pause_btn["text"] = "Play"
        App.progress_slider.set(0)

    # def currimg():
    #     return App.video_frame.current_img()
    # currentimage = tk.Label(image=video_frame.current_img())
    # currentimage.grid(row=2,column=0)

    browse_btn = tk.Button(root,text="Browse",command=lambda:App.openFile())
    browse_btn.grid(row=1,column=1,sticky=E)
    play_btn = tk.Button(root,text="Play",command=lambda:App.playFile())
    play_btn.grid(row=1,column=2)
    stop_btn = tk.Button(root,text="Stop",command=lambda:App.stopFile())
    stop_btn.grid(row=1,column=3)
    pause_btn = tk.Button(root,text="Pause",command=lambda:App.pauseFile())
    pause_btn.grid(row=1,column=4,sticky=W)

    progress_value = tk.IntVar(root)
    progress_slider = tk.Scale(root, variable = progress_value, from_=0, to=0,orient="horizontal",command=lambda val:App.slide(),showvalue=0)
    progress_slider.grid(row=2,column=0,columnspan=5,sticky=[EW,S])

    def slide():
        App.video_frame.seek(App.progress_value.get())


    video_frame.bind("<<Duration>>",update_duration)
    video_frame.bind("<<SecondChanged>>",update_scale)
    video_frame.bind("<<Ended>>",video_ended)




def main():
    app = App()
    app.root.mainloop()

if __name__ == "__main__": main()