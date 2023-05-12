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
import numpy as np
import os
import threading
import time
import queue


class App:
    root = Tk()
    s = ttk.Style()
    s.theme_use('xpnative')
    def __init__(self):
        self.root.geometry("1080x720")
        self.root.configure(bg="white")
        self.root.rowconfigure(0,weight=60)
        self.root.rowconfigure(1,weight=1)
        self.root.rowconfigure(2,weight=15)
        self.root.rowconfigure(3,weight=10)
        self.root.rowconfigure(4,weight=0)
        self.root.rowconfigure(5,weight=10)
        self.root.columnconfigure(0,weight=25)
        self.root.columnconfigure(1,weight=20)
        self.root.columnconfigure(2,weight=0)
        self.root.columnconfigure(3,weight=0)
        self.root.columnconfigure(4,weight=20)


    savinglist = []
    listoflabels = []

    def saveclick():
        k=0
        for item in App.savinglist:
            np.save(App.file_real_name + '/' + App.listoflabels[k],item)
            k+=1
        print('saving to folder is done')


    canv = tk.Canvas(root)
    canv.grid(row=0,column=0,columnspan=5,rowspan=4)
    canv.create_line(300,35,300,200,dash=(4,2))

    bottom_space = ttk.Label(root)
    bottom_space.grid(row=2,column=0,columnspan=5,sticky=[EW,NS])

    video_frame = TkinterVideo(root,keep_aspect=True,scaled=True)
    video_frame.grid(row=0,column=1,columnspan=5,sticky=[EW,NS])

    start_time = ttk.Label(root, text = str(datetime.timedelta(seconds=0)))
    start_time.grid(row=3,column=0,sticky=[W,N])

    end_time = ttk.Label(root,text= str(datetime.timedelta(seconds=0)))
    end_time.grid(row=3,column=4,sticky=[E,N])

    picfromvid = ttk.Label(root,image=None,anchor=CENTER)


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



    treescrolly = ttk.Scrollbar(root,orient="vertical",command=tv.yview)
    treescrollx = ttk.Scrollbar(root,orient="horizontal",command=tv.xview)
    tv.configure(xscrollcommand=treescrollx.set,yscrollcommand=treescrolly.set)
    treescrolly.grid(row=0,column=0,sticky=[E,NS])
    treescrollx.grid(row=0,column=0,sticky=[S,EW])
    
    file_real_name = ""
    videourl = ""
    start_frame_number = 0
    end_frame_number = 0

    framelist = []


    def saving_frames():
        vs = cv2.VideoCapture(App.videourl)
        vs.set(cv2.CAP_PROP_POS_FRAMES,App.start_frame_number)
        frame_width = int(vs.get(3))
        frame_height = int(vs.get(4))
        
        size = (frame_width,frame_height)
        k =0
        l = []
        
        # result = cv2.VideoWriter(App.file_real_name + '/' + App.labels + '.avi',cv2.VideoWriter_fourcc(*'XVID'),5,size,True)
        while True:
            grabbed, frame = vs.read()
            l.append(frame)
            # print('frame running')
            k+=1
            # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            #frame = cv2.resize(frame,(1080,720),interpolation=cv2.INTER_AREA)
            # result.write(frame)

            if not grabbed:
                break
            if k == App.end_frame_number:
                break
            
            # App.frames.append(frame)
        # np.save(App.file_real_name + '/' + App.labels,l)
        # result.release()
        
        App.savinglist.append(l)
        vs.release()
        cv2.destroyAllWindows()
        print('saving ended')


    def openFile():
        file = filedialog.askopenfile(mode="r",filetypes=[('Video Files',['*.mp4','*.mov'])])
        if file is not None:
            global filename
            filename = file.name
            App.video_frame.load(r"{}".format(filename))
            App.videourl = file.name
            App.file_real_name = os.path.basename(filename).split('/')[-1]
            os.mkdir('./' + App.file_real_name)
            

    def playFile():
        App.video_frame.play()
        print(App.video_frame)
    
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
        App.start_frame_number = App.video_frame.current_frame_number()
    def endhere():
        endheretime = App.start_time["text"]
        App.endtimes = endheretime
        App.end_frame_number = App.video_frame.current_frame_number()
    def submit():
        thread = threading.Thread(target=App.saving_frames)
        thread.start()
        annot = App.entry.get()
        App.labels = annot
        App.listoflabels.append(annot)
        App.data.loc[len(App.data.index)] = [App.starttimes,App.endtimes,App.labels]

        App.data.reset_index(inplace=True,drop=True)
        App.clear_data()
        df_rows = App.data.to_numpy().tolist()
        i=0
        for row in df_rows:
            App.tv.insert("","end",iid=i,values=row)
            i+=1
        

    def clear_data():
        App.tv.delete(*App.tv.get_children())
    
    def delete_item():
        for selecteditem in App.tv.selection():
            print(len(App.savinglist))
            del App.savinglist[int(selecteditem)]
            del App.listoflabels[int(selecteditem)]
            App.tv.delete(selecteditem)
            App.data.drop(int(selecteditem),inplace=True)
        App.data.reset_index(inplace=True,drop=True)
        App.clear_data()
        df_rows = App.data.to_numpy().tolist()
        i=0
        for row in df_rows:
            App.tv.insert("","end",iid=i,values=row)
            i+=1

        print(len(App.savinglist))
        print(App.listoflabels)

    def clear_all():
        App.clear_data()
        App.data = App.data[0:0]
        del App.savinglist[:]
        del App.listoflabels[:]
        print(App.listoflabels)

    def seek(value):
        App.video_frame.seek(int(value))

    def skip(value:int):
        App.video_frame.seek(int(App.progress_slider.get()+value))
        App.progress_value.set(App.progress_slider.get()+value)

    def video_ended(event):
        App.progress_slider.set(App.progress_slider["to"])
        App.progress_slider.set(0)


    browse_btn = ttk.Button(root,text="Browse",command=lambda:App.openFile(),width=10)
    browse_btn.grid(row=1,column=1,sticky=E)
    play_btn = ttk.Button(root,text="Play",command=lambda:App.playFile(),width=10)
    play_btn.grid(row=1,column=2)
    stop_btn = ttk.Button(root,text="Stop",command=lambda:App.stopFile(),width=10)
    stop_btn.grid(row=1,column=3)
    pause_btn = ttk.Button(root,text="Pause",command=lambda:App.pauseFile(),width=10)
    pause_btn.grid(row=1,column=4,sticky=W)

    progress_value = tk.IntVar(root)
    progress_slider = ttk.Scale(root, variable = progress_value, from_=0, to=0,orient="horizontal",command=lambda val:App.slide())
    progress_slider.grid(row=2,column=0,columnspan=5,sticky=[EW,S])

    def slide():
        App.video_frame.seek(App.progress_value.get())


    video_frame.bind("<<Duration>>",update_duration)
    video_frame.bind("<<SecondChanged>>",update_scale)
    video_frame.bind("<<Ended>>",video_ended)

    starthere_btn = ttk.Button(root,text="Start here",width=10,command=lambda:App.starthere())
    starthere_btn.grid(row=3,column=1,sticky=[E,S])
    endhere_btn = ttk.Button(root,text="End here",width=10,command=lambda:App.endhere())
    endhere_btn.grid(row=3,column=2,sticky=[W,S])
    label1 = ttk.Label(root,text="Label:",width=10)
    label1.grid(row=4,column=1,sticky=[E])
    entry = ttk.Entry(root,background="white",width=10)
    entry.grid(row=4,column=2,sticky=EW)
    submit_btn = ttk.Button(root,text="Submit",width=10,command=lambda:App.submit())
    submit_btn.grid(row=5,column=2,columnspan=2,sticky=[N,W])
    delete_btn = ttk.Button(root,text="Delete",command=lambda:App.delete_item())
    delete_btn.grid(row=1,column=0)
    frame_btn = ttk.Button(root,text="saveframe",width=10,command=lambda:App.saveclick())
    frame_btn.grid(row=1,column=0,sticky=W)
    clear_all_btn = ttk.Button(root,text="Clear All",width=10,command=lambda:App.clear_all())
    clear_all_btn.grid(row=1,column=0,sticky=E)








def main():
    app = App()
    app.root.mainloop()


if __name__ == "__main__": main()