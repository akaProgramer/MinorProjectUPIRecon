import tkinter as rw
import tkinter.messagebox
from tkinter import ttk
import concurrent.futures
from turtle import left
from jmespath import search
from numpy import pad
import threading
import requests
from time import sleep
from sys import exit
from random import uniform as rand
from datetime import datetime
import regex as re
import socket


API_URL = 'https://upibankvalidator.com/api/upiValidation?upi='
with open("data/general_suffixes.txt", "r") as suffix_file:
    upi_suffix_dict = suffix_file.read().splitlines()
class App(rw.Tk):
    def __init__(self):
        self.found = 0
        self.count = 0
        super().__init__()
        self.geometry("600x500+300+2")
        self.title("UPI Recon")
        # self.wm_iconbitmap("images\me_icon.ico")

    def check_internet(self):
        try:
            socket.create_connection(("1.1.1.1",53))
            return True
        except OSError:
            pass
        return False
       
    def start_operation(self,searchtext):
        self.searched_string.config(text=searchtext)
        self.logs_text['state']= rw.NORMAL
        self.logs_text.delete(1.0,rw.END)
        self.logs_text['state']= rw.DISABLED
        self.status_bar.config(text="")
        t= threading.Thread(target=self.searchvpa,args=(searchtext,upi_suffix_dict,5))
        t.start()

    def textget(self):
        self.progressbar_percent.config(text="0%")
        self.progressbar['value'] = 0
        text= self.search_bar.get()
        email_pattern= r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        car_no_pattern1= r'^[A-Za-z]{2}[ -][0-9]{1,2}[a-zA-z](?: [A-Za-z])?(?: [A-Za-z]*)? [0-9]{4}$'
        car_no_pattenn2= r'^[A-Za-z]{2}[ -][0-9]{1,2}(?: [A-Za-z])?(?: [A-Za-z]*)? [0-9]{4}$'
        number_pattern= r'^[6-9]\d{9}$'
        if (re.fullmatch(email_pattern,text)):
            email=text.split("@")
            email_text= email[0]
            self.start_operation(email_text)
        elif (re.fullmatch(car_no_pattern1,text) or re.fullmatch(car_no_pattenn2,text)):
            car_number= text.replace(" ","")
            car_text= "netc."+ car_number
            self.start_operation(car_text)
        elif re.fullmatch(number_pattern,text):
            number_text= text
            self.start_operation(number_text)
        else:
            self.status_bar["text"]= "not a valid input"
        self.searched_string.config(text=text)

    def searchvpa(self, searchtext,vpa_dict, threadcount):
        self.search_button['state']= rw.DISABLED
        print(searchtext)
        self.search_bar.delete(0,rw.END)
        if(threadcount == 0):
            for suffix in vpa_dict:
                try:
                    self.address_discovery(searchtext + '@' + suffix, API_URL)
                except KeyboardInterrupt:
                    exit(0)
        else:
            threadcount = 10 if threadcount > 10 else threadcount
            with concurrent.futures.ThreadPoolExecutor(max_workers=threadcount) as executor:
                try:
                    for suffix in vpa_dict:
                        executor.submit(self.address_discovery, searchtext + '@' + suffix, API_URL)
                        sleep(rand(.1, .2))
                        
                except KeyboardInterrupt:
                    executor._threads.clear()
                    concurrent.futures.thread._threads_queues.clear()
        if self.found == 0:
            self.status_bar.config(text="No record Found")
        else:
            self.status_bar.config(text=f"{self.found} records found")
        self.search_button['state']= rw.NORMAL
        self.count=0
        self.found=0
        
    def address_discovery(self, vpa, api_url):
        r = requests.post(api_url+vpa)
        print(r.status_code)
        if r.status_code == 200 and r.json()['isUpiRegistered'] is True:
            self.logs_text['state']= rw.NORMAL
            name= r.json()['name']
            print(name+vpa)
            self.logs_text.insert(rw.END,name+" "+vpa+"\n")
            self.found += 1
            self.logs_text['state']= rw.DISABLED
        if r.status_code == 400:
            print("Bad Request")
        if r.status_code == 429:
            print("Too Many Requests")
        self.count += 1
        self.reportProgress(self.count)
        


    

    def reportProgress(self, value):
        value= (round(((value)/len(upi_suffix_dict))*100))
        self.progressbar['value']= value
        self.progressbar_percent.config(text=f"{value}%")


    def window(self):
        self.window_frame = rw.Frame(self)
        self.window_frame.pack(pady=20,expand=True,fill=rw.BOTH)
        self.label_frame= rw.LabelFrame(self.window_frame)
        self.label_frame.pack()
        self.label = rw.Label(self.label_frame,text="UPI Recon",font=("Roboto Medium", 30),bg="#ffffff")
        self.label.grid(column= 0, row= 0)
        
        self.action_frame= rw.LabelFrame(self.window_frame)
        self.search_bar_label= rw.Label(self.action_frame,text="Enter a mob. no.\ email \ car no.:")
        self.search_bar_label.grid(column=0,row=0,sticky=rw.NSEW)
        self.search_bar= rw.Entry(self.action_frame,width=30)
        self.search_bar.grid(column=1,row=0,padx=10)
        self.search_button= rw.Button(self.action_frame,text="Search",command= self.textget)
        self.search_button.grid(column=2,row=0,pady=10,sticky=rw.NSEW)
        self.searched_string= rw.Label(self.action_frame)
        self.searched_string.grid(column=0,row=1,sticky=rw.NSEW)
        self.action_frame.pack(pady=20,expand=True,fill=rw.BOTH)
        

        logs_label= rw.LabelFrame(self.window_frame, text= "Results")
        self.progressbar= ttk.Progressbar(logs_label,orient="horizontal",mode="determinate",length=500, maximum=100)
        self.progressbar.pack(padx=5,pady=(2,2),expand=True,fill="x")
        self.progressbar_percent=rw.Label(logs_label)
        self.progressbar_percent.pack(pady=(1,30))
        scrollbar= rw.Scrollbar(logs_label)
        scrollbar.pack(side=rw.RIGHT,fill=rw.Y)
        self.logs_text= rw.Text(logs_label,width=60,height=10,yscrollcommand=scrollbar.set, state=rw.DISABLED)
        self.logs_text.pack(expand=True,fill="both")
        scrollbar.config(command=self.logs_text.yview)
        self.status_bar= rw.Label(logs_label)
        self.status_bar.pack()
        logs_label.pack(fill="both",expand=True)

    def start(self):
        self.window()
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()