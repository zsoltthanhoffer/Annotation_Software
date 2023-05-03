import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import cv2
from PIL import Image,ImageTk
import datetime
import imageio
import pandas as pd


class App:
    root = Tk()
    def __init__(self):
        App.root.geometry("1080x720")
        App.root.configure(bg="white")
        App.root.rowconfigure(0,weight=60)
        App.root.rowconfigure(1,weight=1)
        App.root.rowconfigure(2,weight=15)
        App.root.rowconfigure(3,weight=10)
        App.root.rowconfigure(4,weight=0)
        App.root.rowconfigure(5,weight=10)
        App.root.columnconfigure(0,weight=25)
        App.root.columnconfigure(1,weight=20)
        App.root.columnconfigure(2,weight=0)
        App.root.columnconfigure(3,weight=0)
        App.root.columnconfigure(4,weight=20)


    bottom_space = tk.Label(root)
    bottom_space.grid(row=2,column=0,columnspan=5,sticky=[EW,NS])

    video_frame = TkinterVideo(root,keep_aspect=True,scaled=True)
    video_frame.grid(row=0,column=1,columnspan=5,sticky=[EW,NS])

    start_time = tk.Label(root, text = str(datetime.timedelta(seconds=0)))
    start_time.grid(row=3,column=0,sticky=[W,N])

    end_time = tk.Label(root,text= str(datetime.timedelta(seconds=0)))
    end_time.grid(row=3,column=4,sticky=[E,N])

    picfromvid = tk.Label(root,image=None,anchor=CENTER)


    labellist = tk.Listbox(root)

    
    starttimes = ""
    endtimes = ""
    labels = ""
    data = pd.DataFrame(columns=['starttime','endtime','label'])
    tv = ttk.Treeview(root)
    tv["column"] = list(data.columns)
    tv["show"] = "headings"
    for column in tv["columns"]:
        tv.heading(column, text=column)
    tv.grid(row=0,column=0,rowspan=1,sticky=[NS,EW])



    treescrolly = tk.Scrollbar(root,orient="vertical",command=tv.yview)
    treescrollx = tk.Scrollbar(root,orient="horizontal",command=tv.xview)
    tv.configure(xscrollcommand=treescrollx.set,yscrollcommand=treescrolly.set)
    treescrolly.grid(row=0,column=0,sticky=[E,NS])
    treescrollx.grid(row=0,column=0,sticky=[S,EW])
    

    videourl = ""
    


    def openFile():
        file = filedialog.askopenfile(mode="r",filetypes=[('Video Files',['*.mp4','*.mov'])])
        if file is not None:
            global filename
            filename = file.name
            App.video_frame.load(r"{}".format(filename))
            App.videourl = file.name
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


        # video = imageio.get_reader(App.videourl)
        # image_frame = Image.fromarray(video.get_data(App.video_frame.current_frame_number()))
        # image_frame.save('img.png', format='png')
        # img = Image.open("img.png")
        # imgrs = img.resize((100,100))
        # img1 = ImageTk.PhotoImage(imgrs)
        # App.picfromvid["image"] = img1
        # App.picfromvid.grid(row=2,column=0)

    def starthere():
        startheretime = App.start_time["text"]
        App.starttimes = startheretime
        print(App.starttimes)
    def endhere():
        endheretime = App.start_time["text"]
        App.endtimes = endheretime
        print(App.endtimes)
    def submit():
        annot = App.entry.get()
        App.labels = annot
        App.data.loc[len(App.data.index)] = [App.starttimes,App.endtimes,App.labels]
        print(App.data.index)

        App.data.reset_index(inplace=True,drop=True)
        App.clear_data()
        df_rows = App.data.to_numpy().tolist()
        i=0
        for row in df_rows:
            App.tv.insert("","end",iid=i,values=row)
            i+=1
        print(App.tv.get_children())
        print(App.data)

    


    def clear_data():
        App.tv.delete(*App.tv.get_children())
    
    def delete_item():
        for selecteditem in App.tv.selection():
            App.tv.delete(selecteditem)
            App.data.drop(int(selecteditem),inplace=True)
        App.data.reset_index(inplace=True,drop=True)
        App.clear_data()
        df_rows = App.data.to_numpy().tolist()
        i=0
        for row in df_rows:
            App.tv.insert("","end",iid=i,values=row)
            i+=1


    def seek(value):
        App.video_frame.seek(int(value))

    def skip(value:int):
        App.video_frame.seek(int(App.progress_slider.get()+value))
        App.progress_value.set(App.progress_slider.get()+value)

    def video_ended(event):
        App.progress_slider.set(App.progress_slider["to"])
        App.progress_slider.set(0)


    browse_btn = tk.Button(root,text="Browse",command=lambda:App.openFile(),width=10)
    browse_btn.grid(row=1,column=1,sticky=E)
    play_btn = tk.Button(root,text="Play",command=lambda:App.playFile(),width=10)
    play_btn.grid(row=1,column=2)
    stop_btn = tk.Button(root,text="Stop",command=lambda:App.stopFile(),width=10)
    stop_btn.grid(row=1,column=3)
    pause_btn = tk.Button(root,text="Pause",command=lambda:App.pauseFile(),width=10)
    pause_btn.grid(row=1,column=4,sticky=W)

    progress_value = tk.IntVar(root)
    progress_slider = tk.Scale(root, variable = progress_value, from_=0, to=0,orient="horizontal",command=lambda val:App.slide(),showvalue=0)
    progress_slider.grid(row=2,column=0,columnspan=5,sticky=[EW,S])

    def slide():
        App.video_frame.seek(App.progress_value.get())


    video_frame.bind("<<Duration>>",update_duration)
    video_frame.bind("<<SecondChanged>>",update_scale)
    video_frame.bind("<<Ended>>",video_ended)

    starthere_btn = tk.Button(root,text="Start here",width=10,command=lambda:App.starthere())
    starthere_btn.grid(row=3,column=1,sticky=[E,S])
    endhere_btn = tk.Button(root,text="End here",width=10,command=lambda:App.endhere())
    endhere_btn.grid(row=3,column=2,sticky=[W,S])
    label1 = tk.Label(root,text="Label:",width=10)
    label1.grid(row=4,column=1,sticky=[E])
    entry = tk.Entry(root,bg="white",width=10)
    entry.grid(row=4,column=2,sticky=EW)
    submit_btn = tk.Button(root,text="Submit",width=10,command=lambda:App.submit())
    submit_btn.grid(row=5,column=2,columnspan=2,sticky=[N,W])
    delete_btn = tk.Button(root,text="Delete",command=lambda:App.delete_item())
    delete_btn.grid(row=1,column=0)




def main():
    app = App()
    app.root.mainloop()

if __name__ == "__main__": main()