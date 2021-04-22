from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from contract_logic import *
import json
import os

class ConnectFrame:
    def __init__(self, master_gui, notebook, _width):
        
        frame = Frame(notebook, width = _width)
        frame.pack(fill="both", expand=1)
        notebook.add(frame, text="Connect")
        self._master_gui = master_gui
        
        
        self.provider = StringVar()
        self.provider.set('http://127.0.0.1:8545')
        self.status = StringVar()
        self.status.set('Not connected')
        self.address = StringVar()
        if (not self._master_gui.blockFace.checkAddress(self.address.get()) ):
            self.address.set('No valid account selected  - Open Keystore ' + u'\u2193'u'\u2193')
        self.keystore_path = StringVar()
        #master_gui.after(1, self.updateStatus)
      
        #Defining the widgets

       

        #Provider address
        label_1 = Label(frame, text='Address of blockchain access provider:', justify=LEFT)
        entry_1 = Entry(frame, textvariable=self.provider, width=50)
        #Status
        label_2 = Label(frame, textvariable=self.status, justify=LEFT)
        #Commit
        button_1 = Button(frame, text='Connect', command=self.connect, justify=LEFT)
        button_2 = Button(frame, text='Check status', command=self.updateStatus, justify=LEFT)
        #Account display
        label_3 = Label(frame, text='Ethereum account:', justify=LEFT)
        entry_3 = Entry(frame, textvariable=self.address, width=50)
        entry_3.configure(state="readonly")
        #Keystore select
        label_4 = Label(frame, text='Keystore file:', justify=LEFT)
        button_4 = Button(frame, text="Select", command=self.file_opener, justify=LEFT)
        entry_4 = Entry(frame, textvariable=self.keystore_path, width=50)
        
        


        #Inserting widgets into the grid

        label_1.grid(row=0, column=0, columnspan = 2, padx=10, pady=(30,5), sticky='W')
        
        entry_1.grid(row=1, column=0,  columnspan = 2, padx=10, pady=10, sticky='W')

        button_1.grid(row=3, column=0, padx=10, pady=10, sticky='W')

        label_2.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        button_2.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        label_3.grid(row=5, column=0, columnspan = 2, padx=10, pady=(30,5), sticky='w')

        entry_3.grid(row=6, column=0, columnspan = 2, padx=10, pady=10, sticky='w')

        label_4.grid(row=7, column=0, columnspan = 2, padx=10, pady=(30,5), sticky='w')
        entry_4.grid(row=8, column=0, columnspan=2, padx=10, pady=0, sticky='W')
        button_4.grid(row=9, column=0, padx=10, pady=10, sticky='W')
      

        

    def connect(self):
        self._master_gui.blockFace.provider = self.provider.get()
        self._master_gui.blockFace.connect()
        _status = self._master_gui.blockFace.is_connected()
        self.status.set(_status)
        print('Status ' + _status)

    def updateStatus(self):
        _status = self._master_gui.blockFace.is_connected()
        self.status.set(_status)
        print('Updated status ' + _status)

    def file_opener(self):
        input = filedialog.askopenfilename(initialdir="." + os.path.sep + "Key_Stores")
        self.keystore_path.set(input)
        try:
            with open(input) as handle:
                self._master_gui.blockFace.keystore = json.loads(handle.read())
            if self._master_gui.blockFace.checkAddress(self._master_gui.blockFace.keystore['address']):
                self.address.set(self._master_gui.blockFace.keystore['address'])
        except:
            self.keystore_path.set(' <- Try again : Invalid keystore!!!')
