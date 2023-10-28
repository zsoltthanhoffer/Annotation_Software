import tkinter as tk
from tkinter import *
#from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import cv2
import PIL
from PIL import Image,ImageTk
import datetime
import imageio
import pandas as pd
import numpy as np
import os
import threading
import time
import queue
import xml.etree.ElementTree as ET
from tkinter.font import BOLD, Font
from model_creator import model_creation
from xml_reader import xmlreader
import tkinterdnd2



class App:
    root = ttk.Window(themename='superhero')
    # s = ttk.Style()
    # s.theme_use('xpnative')
    def __init__(self):
        self.root.geometry("1080x720")
        #self.root.configure(bg="white")
        self.root.rowconfigure(0,weight=70)
        self.root.rowconfigure(1,weight=1)
        self.root.rowconfigure(2,weight=15)
        self.root.rowconfigure(3,weight=10)
        self.root.rowconfigure(4,weight=0)
        self.root.rowconfigure(5,weight=10)
        self.root.columnconfigure(0,weight=1)
        self.root.columnconfigure(1,weight=20)
        self.root.columnconfigure(2,weight=0)
        self.root.columnconfigure(3,weight=0)
        self.root.columnconfigure(4,weight=20)

        self.bold12 = Font(self.root, size=12,weight=BOLD)
        self.normal12 = Font(self.root,size=12)
        
        self.label_text = tk.StringVar()
        starthere_btn = ttk.Button(self.root,text="Start here",width=10,command=lambda:self.starthere())
        starthere_btn.grid(row=3,column=1,sticky=[E,S],padx=2,pady=2)
        endhere_btn = ttk.Button(self.root,text="End here",width=10,command=lambda:self.endhere())
        endhere_btn.grid(row=3,column=2,sticky=[W,S],padx=2,pady=2)
        label_button = ttk.Button(self.root,text="Label:",width=10,bootstyle="success-outline",state=DISABLED)
        label_button.grid(row=4,column=1,sticky=[E],padx=2,pady=2)
        # label1 = ttk.Label(self.root,text="Label:",bootstyle="inverse-primary",width=13)#,width=10,font=self.bold25,borderwidth=2,relief="solid")
        # label1.grid(row=4,column=1,sticky=[E])
        entry = ttk.Entry(self.root,width=10,textvar=self.label_text)
        entry.grid(row=4,column=2,sticky=EW,padx=2,pady=2)
        submit_btn = ttk.Button(self.root,text="Submit",width=10,command=lambda:self.submit())
        submit_btn.grid(row=5,column=2,columnspan=2,sticky=[N,W],padx=2,pady=2)
        delete_btn = ttk.Button(self.root,text="Delete",command=lambda:self.delete_item(),width = 10)
        delete_btn.grid(row=1,column=0,sticky = E,padx=91)
        frame_btn = ttk.Button(self.root,text="saveframe",width=10,command=lambda:self.saveclick())
        frame_btn.grid(row=1,column=0,sticky=W)
        clear_all_btn = ttk.Button(self.root,text="Clear All",width=10,command=lambda:self.clear_all())
        clear_all_btn.grid(row=1,column=0,sticky=E,padx=5)
        browse_btn = ttk.Button(self.root,text="Browse",command=lambda:self.openFile(),width=10)
        browse_btn.grid(row=1,column=1,sticky=E)
        play_btn = ttk.Button(self.root,text="Play",command=lambda:self.playFile(),width=10)
        play_btn.grid(row=1,column=2)
        # stop_btn = ttk.Button(root,text="Stop",command=lambda:self.stopFile(),width=10)
        # stop_btn.grid(row=1,column=3)
        pause_btn = ttk.Button(self.root,text="Pause",command=lambda:self.pauseFile(),width=10)
        pause_btn.grid(row=1,column=3)
        advanced_setting_btn = ttk.Button(self.root,text="Advanced Settings",command=lambda:self.advanced_settings_window())
        advanced_setting_btn.grid(row=5,column=4,sticky=[E,S],pady=5,padx=5)

        cmsgbox_title = ttk.Label(self.root,text="System Messages")
        cmsgbox_title.grid(row=5,column=0,sticky=[W,N])

        self.console_msgbox = tk.Text(self.root, height=10, width=60)
        self.console_msgbox.grid(row=5,column=0,sticky=[W,S])
        self.console_msgbox.configure(state='disabled')

        self.progress_value = tk.IntVar()
        self.progress_slider = ttk.Scale(self.root, variable = self.progress_value, from_=0, to=0,orient="horizontal",command=lambda val:self.slide())
        self.progress_slider.grid(row=2,column=0,columnspan=5,sticky=[EW,S])
        
        self.video_frame.bind("<<SecondChanged>>",self.update_scale)
        self.video_frame.bind("<<Duration>>",self.update_duration)

        self.root.bind('<Return>',self.submit)
        

    def advanced_settings_window(self):
        self.win = Toplevel(self.root)
        self.win.geometry("1080x720")
        self.win.columnconfigure(0,weight=0)
        self.win.columnconfigure(1,weight=0)
        self.win.columnconfigure(2,weight=100)

        self.win.rowconfigure(0,weight=0)
        self.win.rowconfigure(1,weight=0)
        self.win.rowconfigure(2,weight=0)
        self.win.rowconfigure(3,weight=0)
        self.win.rowconfigure(4,weight=0)
        self.win.rowconfigure(5,weight=0)
        self.win.rowconfigure(6,weight=0)
        self.win.rowconfigure(7,weight=0)
        self.win.rowconfigure(8,weight=0)
        self.win.rowconfigure(9,weight=50)

        
        builtinmodels = ttk.Label(self.win,text="Built in models:",font=self.bold12)
        builtinmodels.grid(row=0,column=0,sticky=[W,N],pady=5)
        variable = ttk.StringVar(self.win)
        modelbtn1 = ttk.Radiobutton(self.win,text="Simple CNN",variable=variable,value="Simple CNN")
        modelbtn1.grid(row=1,column=0,sticky=[W,N],pady=2)
        modelbtn2 = ttk.Radiobutton(self.win,text="CNN",variable=variable,value="CNN")
        modelbtn2.grid(row=2,column=0,sticky=[W,N],pady=2)
        modelbtn3 = ttk.Radiobutton(self.win,text="UNET",variable=variable,value="UNET")
        modelbtn3.grid(row=3,column=0,sticky=[W,N],pady=2)
        modelbtn4 = ttk.Radiobutton(self.win,text="CNN2",variable=variable,value="CNN2")
        modelbtn4.grid(row=4,column=0,sticky=[W,N],pady=2)

        new_model_btn = ttk.Button(self.win,text = "Add Layer",command=lambda:self.new_model_init())
        new_model_btn.grid(row=5,column=0,sticky = [W,N],pady=10)
        self.layer_frame = ttk.Frame(self.win)
        self.layer_frame.grid(row=6,column=0,sticky = [W,N])
        self.layer_prop_frame = ttk.Frame(self.win)
        self.layer_prop_frame.grid(row=6,column=1,sticky=[W,N])
        submit_model_btn = ttk.Button(self.win,text = "Submit")
        submit_model_btn.grid(row=7,column=0,sticky=[W,N],pady=5)


        # scrolly = ttk.Scrollbar(self.win,orient="vertical")
        # t=Text(self.win,width=15,height=15,wrap=NONE,yscrollcommand=scrolly.set)
        # scrolly.config(command = t.yview)

    def new_model_init(self):
        new_layer = ttk.Combobox(self.layer_frame,width=15,values=["Conv2D","MaxPooling","Conv1D","Flatten","Dense"])
        new_layer.pack(pady=2)
        new_layer_prop = ttk.Entry(self.layer_prop_frame,width=30)
        new_layer_prop.pack(pady=2)



    # savinglist = []
    listoflabels = []
    sh_numbers = []
    ef_numbers = []

    def write_message(self,message):
        self.console_msgbox.configure(state='normal')
        self.console_msgbox.insert(tk.END, time.strftime("%H:%M:%S",time.localtime()) + ': ' + message + '\n')
        self.console_msgbox.configure(state='disabled')
        

    def saveclick(self):
        root = ET.Element("file",name=self.file_real_name)
        # root = ET.Element("root")
        for i in range(len(self.listoflabels)):
            t = ET.SubElement(root,"Label",name=self.listoflabels[i])
            #t.text = self.listoflabels[i]
            ET.SubElement(t,"Start_frame").text = str(self.sh_numbers[i])
            ET.SubElement(t,"End_frame").text = str(self.ef_numbers[i])
        tree = ET.ElementTree(root)
        with open (self.file_real_name + '.xml',"wb") as files: tree.write(files)
        # tree.write(self.file_real_name + '.xml')
        self.write_message('XML file saved as ' + self.file_real_name + '.xml')


    canv = tk.Canvas(root)
    canv.grid(row=0,column=1,columnspan=5,sticky=[EW,NS])

    bottom_space = ttk.Label(root)
    bottom_space.grid(row=2,column=0,columnspan=5,sticky=[EW,NS])

    # video_frame = TkinterVideo(root,keep_aspect=True,scaled=True)
    # video_frame.grid(row=0,column=1,columnspan=5,sticky=[EW,NS])
    video_frame = TkinterVideo(canv,keep_aspect=True)
    video_frame.pack(expand=True,fill='both')


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
    tv.grid(row=0,column=0,rowspan=1,sticky=[NS,EW],padx=2,pady=2)

    treescrolly = ttk.Scrollbar(root,orient="vertical",command=tv.yview)
    treescrollx = ttk.Scrollbar(root,orient="horizontal",command=tv.xview)
    tv.configure(xscrollcommand=treescrollx.set,yscrollcommand=treescrolly.set)
    treescrolly.grid(row=0,column=0,sticky=[E,NS],padx=5,pady=5)
    treescrollx.grid(row=0,column=0,sticky=[S,EW],padx=5,pady=5)
    
    file_real_name = ""
    videourl = ""
    start_frame_number = 0
    end_frame_number = 0

    framelist = []



    def saving_frames(self):
        vs = cv2.VideoCapture(self.videourl)
        vs.set(cv2.CAP_PROP_POS_FRAMES,self.start_frame_number)
        frame_width = int(vs.get(3))
        frame_height = int(vs.get(4))
        
        # size = (frame_width,frame_height)
        # k =0
        # l = []
        
        # while True:
        #     grabbed, frame = vs.read()
        #     l.append(frame)
        #     k+=1
        #     if not grabbed:
        #         break
        #     if k == self.end_frame_number:
        #         break
        
        # self.savinglist.append(l)
        vs.release()
        cv2.destroyAllWindows()
        self.write_message('Annotation added!')


    def openFile(self):
        file = filedialog.askopenfile(mode="r",filetypes=[('Video Files',['*.mp4','*.mov'])])
        if file is not None:
            global filename
            filename = file.name
            self.video_frame.load(r"{}".format(filename))
            self.videourl = file.name
            self.file_real_name = os.path.basename(filename).split('/')[-1]
            # os.mkdir('./' + self.file_real_name)
        self.playFile()
        
            

    def playFile(self):
        self.video_frame.play()
        print(self.video_frame)
    
    # def stopFile():
    #     App.video_frame.stop()
    
    def pauseFile(self):
        self.video_frame.pause()
        self.canv.create_line(400,35,400,200, tags=("line",))
        self.canv.tag_raise("line")


    def update_duration(self,event):
        duration = self.video_frame.video_info()["duration"]

        self.end_time["text"] = str(datetime.timedelta(seconds=duration)).split('.')[0]
        self.progress_slider["to"] = duration



    def update_scale(self,event):
        self.progress_value.set(self.video_frame.current_duration())
        self.start_time["text"] = str(datetime.timedelta(seconds=self.video_frame.current_duration())).split('.')[0]

        # video = imageio.get_reader(App.videourl)
        # image_frame = Image.fromarray(video.get_data(App.video_frame.current_frame_number()))
        # image_frame.save('img.png', format='png')
        # img = Image.open("img.png")
        # imgrs = img.resize((100,100))
        # img1 = ImageTk.PhotoImage(imgrs)
        # App.picfromvid["image"] = img1
        # App.picfromvid.grid(row=2,column=0)
    def starthere(self):
        startheretime = self.start_time["text"]
        self.starttimes = startheretime
        self.start_frame_number = self.video_frame.current_frame_number()

    def endhere(self):
        endheretime = self.start_time["text"]
        self.endtimes = endheretime
        self.end_frame_number = self.video_frame.current_frame_number()

    def submit(self):
        thread = threading.Thread(target=self.saving_frames)
        thread.start()
        annot = self.label_text.get()
        self.labels = annot
        self.listoflabels.append(annot)
        self.data.loc[len(self.data.index)] = [self.starttimes,self.endtimes,self.labels]
        
        self.sh_numbers.append(self.start_frame_number)
        self.ef_numbers.append(self.end_frame_number)

        self.data.reset_index(inplace=True,drop=True)
        self.clear_data()
        df_rows = self.data.to_numpy().tolist()
        i=0
        for row in df_rows:
            self.tv.insert("","end",iid=i,values=row)
            i+=1
        

    def clear_data(self):
        self.tv.delete(*self.tv.get_children())
    
    def delete_item(self):
        reversed_list = [int(x) for x in self.tv.selection()]
        reversed_list.reverse()
        for selecteditem in reversed_list:
            # print(len(self.savinglist))
            # del self.savinglist[int(selecteditem)]
            del self.listoflabels[int(selecteditem)]
            self.tv.delete(selecteditem)
            self.data.drop(int(selecteditem),inplace=True)
        self.data.reset_index(inplace=True,drop=True)
        self.clear_data()
        df_rows = self.data.to_numpy().tolist()
        i=0
        for row in df_rows:
            self.tv.insert("","end",iid=i,values=row)
            i+=1

    def clear_all(self):
        self.clear_data()
        self.data = self.data[0:0]
        # del self.savinglist[:]
        del self.listoflabels[:]
        print(self.listoflabels)

    def seek(value):
        App.video_frame.seek(int(value))

    def skip(value:int):
        App.video_frame.seek(int(App.progress_slider.get()+value))
        App.progress_value.set(App.progress_slider.get()+value)

    def video_ended(event):
        App.progress_slider.set(App.progress_slider["to"])
        App.progress_slider.set(0)


    # progress_value = tk.IntVar(root)
    # progress_slider = ttk.Scale(root, variable = progress_value, from_=0, to=0,orient="horizontal",command=lambda val:App.slide())
    # progress_slider.grid(row=2,column=0,columnspan=5,sticky=[EW,S])

    def slide(self):
        self.video_frame.seek(self.progress_value.get())


    # video_frame.bind("<<Duration>>",update_duration)
    # video_frame.bind("<<SecondChanged>>",update_scale)
    video_frame.bind("<<Ended>>",video_ended)

def main():
    app = App()
    app.root.mainloop()


if __name__ == "__main__":
    main()