#from clickthru import *
import tkinter as tk


class APP(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.grid()
        self.createWidgets()
        self.createCanvas()
        
    def createWidgets(self):
        self.label = tk.Label(text= "Load Taxonomy",font=("Arial Bold",30))
        self.label.grid()

        #this needs to include a path
        self.path_label = tk.Label(text= "path: \\overview",font=("Arial Bold",10))
        self.path_label.grid(column=0,row=1) 
        self.path_add = tk.Entry(width=10)
        self.path_add.grid(column=0,row=2)
        self.path_add_button = tk.Button(text="Add to Path", command= self.add_to_path)
        self.path_add_button.grid(column=0,row=3)
        self.path_del_button = tk.Button(text="Up a level", command= self.del_to_path)
        self.path_del_button.grid(column=0,row=4)
        #needs to include a path
        
        
        self.close_button = tk.Button(text="Close", command= self.destroy)
        self.close_button.grid(column=1,row=0)

        
        self.start = tk.Label(text= "Start yy/dd/hh",font=("Arial",10))
        self.start.grid(column=2,row=1)
        self.startin = tk.Entry(width=10)
        self.startin.grid(column=2,row=2)
        self.close_button = tk.Button(text="Update", command= self.update_start)
        self.close_button.grid(column=3,row=2)
        
        self.end = tk.Label(text= "End yy/dd/hh",font=("Arial",10))
        self.end.grid(column=2,row=3)
        self.endin = tk.Entry(width=10)
        self.endin.grid(column=2,row=4)
        self.close_button = tk.Button(text="Update", command= self.update_end)
        self.close_button.grid(column=3,row=4)
        
        self.delta = tk.Label(text= "Delta t hh/mm *default=15m*",font=("Arial",10))
        self.delta.grid(column=2,row=5)
        self.deltain = tk.Entry(width=10)
        self.deltain.grid(column=2,row=6)
        self.close_button = tk.Button(text="Update", command= self.update_delta)
        self.close_button.grid(column=3,row=6)
        
        self.global_button = tk.Button(text="Global Refresh",state='disabled')
        self.global_button.grid(column=5,row=0)
        self.global_check_state=tk.IntVar()
        self.global_check_state.set(0)
        self.global_check = tk.Checkbutton(var=self.global_check_state,command=self.global_config)
        self.global_check.grid(column=4, row=0)   
        
        self.local_button = tk.Button(text="Local Refresh")
        self.local_button.grid(column=6,row=0)
    
    def createCanvas(self):
        self.dataframe=tk.Frame(width=500,height=300,bd=4)
        self.dataframe.place(x=30,y=300)
        
        self.canvas=tk.Canvas(self.dataframe)
        self.frame=tk.Frame(self.canvas)
        self.scrollbar=tk.Scrollbar(self.dataframe,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.frame,anchor='nw')
        self.frame.bind("<Configure>",self.scrollfunction)

    def populateCanvas(self):
        tags=read_tagnames()
        path=self.path_label['text']
    
    def scrollfunction(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=200,height=200)
   
    def global_config(self):
        if self.global_check_state.get() == 0:
            self.global_button.configure(state='disable')
        if self.global_check_state.get() == 1:
            self.global_button.configure(state='normal')

    def add_to_path(self):
        new_path=self.path_label['text']+"\\"+self.path_add.get()
        self.path_label.configure(text=new_path)
        
    def del_to_path(self):
        txt=self.path_label['text']
        new_path=txt[:txt.rfind("\\")]
        self.path_label.configure(text=new_path)
        
    def update_start():
        return 1
    def update_end():
        return 1
    def update_delta():
        return 1
        
window = APP()

window.geometry('1200x1000')
window.title("Load Taxonomy Viewer Not ClickThru Yet")
window.mainloop()