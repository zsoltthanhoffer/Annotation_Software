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
from xml_reader import xmlreader


class App:

    def __init__(self):
        self.root = ttk.Window(themename='superhero')
        self.root.geometry("520x850")

        self.root.rowconfigure(0,weight=70)
        self.root.rowconfigure(1,weight=1)
        self.root.rowconfigure(2,weight=15)
        self.root.rowconfigure(3,weight=0)
        self.root.rowconfigure(4,weight=0)
        self.root.rowconfigure(5,weight=10)
        self.root.rowconfigure(6,weight=10)
        self.root.columnconfigure(0,weight=10)
        self.root.columnconfigure(1,weight=10)
        self.root.columnconfigure(2,weight=10)
        self.root.columnconfigure(3,weight=10)
        self.root.columnconfigure(4,weight=10)

        self.starttimes = ""
        self.endtimes = ""
        self.labels = ""
        self.data = pd.DataFrame(columns=['starttime','endtime','label'])
        self.tv = ttk.Treeview(self.root)
        self.tv["column"] = list(self.data.columns)
        self.tv["show"] = "headings"
        for column in self.tv["columns"]:
            self.tv.heading(column, text=column)
        self.tv.grid(row=0,column=0,columnspan=5,sticky=[NS,EW],padx=2,pady=2)
        self.tv.column("starttime",width=50)
        self.tv.column("endtime",width=50)
        self.tv.column("label",width=50)

        self.treescrolly = ttk.Scrollbar(self.root,orient="vertical",command=self.tv.yview)
        self.treescrollx = ttk.Scrollbar(self.root,orient="horizontal",command=self.tv.xview)
        self.tv.configure(xscrollcommand=self.treescrollx.set,yscrollcommand=self.treescrolly.set)
        self.treescrolly.grid(row=0,column=4,sticky=[E,NS],padx=5,pady=5)
        self.treescrollx.grid(row=0,column=0,columnspan=5,sticky=[S,EW],padx=5,pady=5)



        self.browse_btn = ttk.Button(self.root,text="Browse",width=10,command=lambda:self.openFile())
        self.browse_btn.grid(row=1,column=2,padx=5)
        self.play_btn = ttk.Button(self.root,text="Play",width=10)
        self.play_btn.grid(row=1,column=3,padx=5)
        self.save_btn = ttk.Button(self.root,text="Save",width=10,command=lambda:self.saveclick())
        self.save_btn.grid(row=1,column=4,padx=5)
        self.delete_btn = ttk.Button(self.root,text="Delete",width=10,command=lambda:self.delete_item())
        self.delete_btn.grid(row=1,column=0,padx=5)
        self.clear_all_btn = ttk.Button(self.root,text="Clear All",width=10,command=lambda:self.clear_all())
        self.clear_all_btn.grid(row=1,column=1,padx=5)


        cmsgbox_title = ttk.Label(self.root,text="System Messages")
        cmsgbox_title.grid(row=5,column=0,sticky=[W,S])

        self.console_msgbox = tk.Text(self.root, height=10, width=40)
        self.console_msgbox.grid(row=6,column=0,columnspan=5,sticky=[W,NS])
        self.console_msgbox.configure(state='disabled')


        self.label_text = tk.StringVar()
        self.starthere_btn = ttk.Button(self.root,text="Start here",width=10,command=lambda:self.starthere())
        self.starthere_btn.grid(row=3,column=3,padx=2,pady=2,sticky=EW)
        self.endhere_btn = ttk.Button(self.root,text="End here",width=10,command=lambda:self.endhere())
        self.endhere_btn.grid(row=3,column=4,padx=2,pady=2,sticky=EW)
        self.label_btn = ttk.Button(self.root,text="Label:",width=10,bootstyle="success-outline",state=DISABLED)
        self.label_btn.grid(row=4,column=3,pady=2,padx=2,sticky=EW)
        self.entry = ttk.Entry(self.root,width=10,textvar=self.label_text)
        self.entry.grid(row=4,column=4,pady=2,padx=2,sticky=EW)
        self.submit_btn = ttk.Button(self.root, text="Submit", width = 10, command=lambda:self.submit())
        self.submit_btn.grid(row=5,column=4,pady=2,padx=2,sticky=[EW,N])

        self.listoflabels = []
        self.sf_numbers = []
        self.ef_numbers = []
        self.starthereframe = 0
        self.endhereframe = 0
        self.startpoints = []
        self.endpoints = []

        self.file_real_name = ""



    def starthere(self):
        self.starthereframe = last_frame_num
        print(last_frame_num)
    
    def endhere(self):
        self.endhereframe = last_frame_num
        print(last_frame_num)

    def submit(self):
        self.sf_numbers.append(self.starthereframe)
        self.ef_numbers.append(self.endhereframe)
        self.startpoints.append((last_x,last_y))
        self.endpoints.append((c_x,c_y))
        annot = self.label_text.get()
        self.listoflabels.append(annot)
        self.data.loc[len(self.data.index)] = [self.starthereframe,self.endhereframe,annot]

        self.data.reset_index(inplace=True,drop=True)
        self.clear_data()
        df_rows = self.data.to_numpy().tolist()
        i=0
        for row in df_rows:
            self.tv.insert("","end",iid=i,values=row)
            i+=1
    def move_cursor_to_entry(self):
        self.entry.focus_set()

    def clear_data(self):
        self.tv.delete(*self.tv.get_children())
    
    def delete_item(self):
        reversed_list = [int(x) for x in self.tv.selection()]
        reversed_list.reverse()
        for selecteditem in reversed_list:
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
        del self.listoflabels[:]



    def saveclick(self):
        root = ET.Element("file",name=self.file_real_name)
        # root = ET.Element("root")
        for i in range(len(self.listoflabels)):
            t = ET.SubElement(root,"Label",name=self.listoflabels[i])
            #t.text = self.listoflabels[i]
            ET.SubElement(t,"Start_frame").text = str(self.sf_numbers[i])
            ET.SubElement(t,"End_frame").text = str(self.ef_numbers[i])
            ET.SubElement(t,"Start_point").text = str(self.startpoints[i])
            ET.SubElement(t,"End_point").text = str(self.endpoints[i])
        tree = ET.ElementTree(root)
        with open (self.file_real_name + '.xml',"wb") as files: tree.write(files)
        # tree.write(self.file_real_name + '.xml')
        self.write_message('XML file saved as ' + self.file_real_name + '.xml')

    def write_message(self,message):
        self.console_msgbox.configure(state='normal')
        self.console_msgbox.insert(tk.END, time.strftime("%H:%M:%S",time.localtime()) + ': ' + message + '\n')
        self.console_msgbox.configure(state='disabled')

        

    def openFile(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
        self.file_real_name = file_path.split('/')[-1]
        if file_path:
            global drawing, last_x, last_y, c_x, c_y, last_frame
            drawing = False
            last_x, last_y = -1, -1
            c_x, c_y = -1, -1
            last_frame = None
            

            # global last_frame
            # last_frame = None
            # global original_image
            # original_image = None            

            def display_video():
                def draw_on_frame(event, x, y, flags, param):
                    global drawing, last_x, last_y, c_x, c_y
                    if event == cv2.EVENT_LBUTTONDOWN:
                        drawing = True
                        last_x, last_y = x, y
                        c_x, c_y = x, y
                    elif event == cv2.EVENT_MOUSEMOVE:
                        if drawing:
                            c_x, c_y = x, y
                            # cv2.rectangle(last_frame, (last_x, last_y), (c_x, c_y), (0, 255, 0), 2)
                    elif event == cv2.EVENT_LBUTTONUP:
                        drawing = False
                        # c_x, c_y = x, y

                cap = cv2.VideoCapture(file_path)
                def on_slider_change(pos):
                    cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
                
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cv2.namedWindow("vid",cv2.WINDOW_NORMAL)
                # cv2.setMouseCallback("vid", draw_on_frame)
                cv2.createTrackbar('Position','vid',0,total_frames,on_slider_change)
                
                # global last_frame
                # last_frame = None
                global last_frame_num
                last_frame_num = None

                while True:
                    ret, frame = cap.read()
                    # if ret:
                    cv2.rectangle(frame, (last_x, last_y), (c_x, c_y), (0, 255, 0), 2)
                    cv2.imshow('vid', frame)
                    cv2.setMouseCallback("vid", draw_on_frame)
                    cv2.setTrackbarPos("Position","vid", int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
                    key = cv2.waitKey(1)
                    last_frame = frame
                    # last_frame_num = frame
                    # original_image = last_frame.copy()
                    if key == ord('q'):
                        last_frame = frame
                        original_image = last_frame.copy()
                        while True:
                            key1 = cv2.waitKey(1) & 0xFF
                            cv2.imshow('vid',last_frame)
                            last_frame = original_image.copy()
                            cv2.rectangle(last_frame, (last_x, last_y), (c_x, c_y), (0, 255, 0), 2)
                            if key1 == ord('q'):
                                break
                            elif key1 == ord('w'):
                                self.starthere()
                            elif key1 == ord('e'):
                                self.endhere()
                            elif key1 == ord('s'):
                                self.submit()
                            elif key1 == 9:
                                self.move_cursor_to_entry()
                    elif key == ord('w'):
                        self.starthere()
                    elif key == ord('e'):
                        self.endhere()
                    elif key == ord('s'):
                        self.submit()
                    elif key == 9:
                        self.move_cursor_to_entry()
                    elif key == 27:
                        break
                    last_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)

                cap.release()
                cv2.destroyAllWindows()

            cv_thread = threading.Thread(target=display_video)
            cv_thread.start()


def main():
    app = App()
    app.root.mainloop()


if __name__ == "__main__":
    main()