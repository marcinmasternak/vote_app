from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from contract_logic import *
from datetime import datetime

class DeployFrame:
    def __init__(self, master_gui, notebook, _width):
        
        frame = Frame(notebook, width = _width)
        frame.pack(fill="both", expand=1)
        notebook.add(frame, text="Deploy")
        self._master_gui = master_gui
        
        self.candidate_list = []
        self.start = StringVar()
        self.end = StringVar()
        self.name = StringVar()
        self.name.set("Vote-" + datetime.now().strftime("%d/%m/%Y-%H:%M:%S"))

        #Defining the widgets

        #Provider candidate names
        self.label_name = Label(frame, text='Vote name' , justify=LEFT)
        self.entry_name = Entry(frame, textvar=self.name, justify=LEFT, width=50)

        self.label_1 = Label(frame, text='Candidates:\n[ names separated by ' + u'\u23CE' +' ]\n[ Maximum name length = 20 characters ]' , justify=LEFT)
        self.entry_1 = Text(frame, spacing3=10, width=50, height=10)
        #self.button_1 = Button(frame, text='Deploy', command=self._master_gui.password_box1, justify=LEFT)

        self.button_2 = Button(frame, text='Deploy', command=self.deploy, justify=LEFT)

        #Get vote start and end time

        self.label_2 = Label(frame, text='Vote start:')
        self.entry_2 = Entry(frame, font = "Courier 12", textvariable=self.start, width=19)
        self.label_3 = Label(frame, text='Vote end:')
        self.entry_3 = Entry(frame, font = "Courier 12", textvariable=self.end, width=19)
        self.label_4 = Label(frame, font = "Courier 12", text='DD/MM/YYYY-HH:MM:SS')
        self.label_5 = Label(frame, font = "Courier 12", text='DD/MM/YYYY-HH:MM:SS')
        
        #Inserting widgets into the grid
        self.label_name.grid(row=0, column=0, columnspan = 2, padx=10, pady=(20,0), sticky='W')
        self.entry_name.grid(row=1, column=0,  columnspan = 2, padx=10, pady=0, sticky='W')
        
        self.label_1.grid(row=2, column=0, columnspan = 2, padx=10, pady=(20,0), sticky='W')
        self.entry_1.grid(row=3, column=0,  columnspan = 2, padx=10, pady=0, sticky='W')
        
        self.label_2.grid(row=4, column=0, padx=10, pady=(10,0), sticky='w')
        self.entry_2.grid(row=5, column=0, padx=10, pady=0, ipady=(3), sticky='W')
        self.label_3.grid(row=4, column=1, padx=10, pady=(10,0), sticky='w')
        self.entry_3.grid(row=5, column=1, padx=10, pady=0, ipady=3, sticky='W')
        self.label_4.grid(row=6, column=0, padx=10, pady=(0,10), sticky='W')
        self.label_5.grid(row=6, column=1, padx=10, pady=(0,10), sticky='W')

        #self.button_1.grid(row=7, column=0, padx=10, pady=10, sticky='W')

        self.button_2.grid(row=8, column=0, padx=10, pady=10, sticky='W')

        self.init_start_end_time()

    def read_candidates(self):
        text = self.entry_1.get("1.0", END)
        self.candidate_list = text.splitlines()
        self.candidate_list =[item for item in self.candidate_list if item]
        self.candidate_list =[item[:20].encode('utf-8') for item in self.candidate_list]

    def init_start_end_time(self):
        now = datetime.now()     
        self.start.set(now.strftime("%d/%m/%Y-%H:%M:%S"))

        timestamp = now.timestamp()
        timestamp_later = timestamp + 120
        later = datetime.fromtimestamp(timestamp_later)
        self.end.set(later.strftime("%d/%m/%Y-%H:%M:%S"))

    def deploy(self):
        self.read_candidates()
        if ( len(self.candidate_list) == 0):
            self._master_gui.error_box1('No candidates entered!')
        elif ( self._master_gui.blockFace.keystore == None):
            self._master_gui.error_box1('No account selected!\nAdd keystore in "Connect" tab')
        elif (self._master_gui.blockFace.w3 == None):
            self._master_gui.error_box1('Not connected! Select provider in "Connect" tab')
        else:
            try:
                start = datetime.strptime( self.start.get(),"%d/%m/%Y-%H:%M:%S").timestamp()
                end = datetime.strptime( self.end.get(),"%d/%m/%Y-%H:%M:%S").timestamp()
                self._master_gui.blockFace.deploy(int(start), int(end), self.candidate_list, self.name.get())
            except Exception as err:
                self._master_gui.error_box1(err)
        
      
