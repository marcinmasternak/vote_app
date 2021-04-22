from tkinter import *
from tkinter import _setit
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from contract_logic import *
from web3 import Web3

class VoteFrame:
    def __init__(self, master_gui, notebook, _width):
        
        self.frame = Frame(notebook, width = _width)
        self.frame.pack(fill="both", expand=1)
        notebook.add(self.frame, text="Vote")
        self._master_gui = master_gui

        self.vote_address = StringVar()

        #Retreived contract data
        self.vote_name = StringVar()
        self.vote_name.set('--- No Vote Contract specified ---  ')
        self.start = StringVar()
        self.start.set(' -- N/A --')
        self.end = StringVar()
        self.end.set(' -- N/A --')
        self.candidates_dict = {' -- N/A --' : 1}

        self.selectedCandidate = StringVar()
        self.selectedCandidate.set("Select")


        #Retreive form
        self.label_1 = Label(self.frame, text='Provide address of the vote contract:', justify=LEFT)
        self.entry_1 = Entry(self.frame, textvariable=self.vote_address, width=45)
        self.button_1 = Button(self.frame, text="Retreive vote details",
                               command=self.retreive_vote,
                               justify=LEFT)

        self.label_1.grid(row=0, column=0, padx=10, pady=(30,0), columnspan=2, sticky='w')
        self.entry_1.grid(row=2, column=0, padx=10, pady=(0,0), columnspan=2, sticky='w')
        self.button_1.grid(row=3, column=0, padx=10, pady=10, columnspan=2, sticky='W')

        #Vote details
        self.label_2 = Label(self.frame, text='Vote name:', justify=LEFT)
        self.label_3 = Label(self.frame, textvariable=self.vote_name, justify=LEFT)
        self.label_2.grid(row=4, column=0, padx=10, pady=(15,0), columnspan=2, sticky='w')
        self.label_3.grid(row=5, column=0, padx=10, pady=(0,0), columnspan=2, sticky='w')
        
        self.label_4 = Label(self.frame, text="Vote start:", justify=LEFT)
        self.label_4.grid(row=6, column=0, padx=(10,10), pady=(15,0), sticky='w')
        self.label_5 = Label(self.frame, text="Vote end:", justify=LEFT)
        self.label_5.grid(row=7, column=0, padx=(10,10), pady=(15,0), sticky='w')

        self.label_4_1 = Label(self.frame, textvariable=self.start, justify=LEFT)
        self.label_4_1.grid(row=6, column=1, padx=0, pady=(15,0), sticky='w')
        self.label_5_1 = Label(self.frame, textvariable=self.end, justify=LEFT)
        self.label_5_1.grid(row=7, column=1, padx=0, pady=(15,0), sticky='w')

        self.label_6 = Label(self.frame, text="Select candidate: ", justify=LEFT)
        self.label_6.grid(row=8, column=0, padx=(10,10), pady=(30,0), sticky='w')
        self.candidateMenu = OptionMenu(self.frame, self.selectedCandidate, *self.candidates_dict.keys())
        self.candidateMenu.config(width=20)
        self.candidateMenu.grid(row=8, column=1, padx=0, pady=(20,0), sticky='w')

        self.button_2 = Button(self.frame, text="VOTE", command=self.vote, height=3, width=15, justify=LEFT)
        self.button_2.grid(row=9, column=0, padx=(45,0), pady=(70,0), columnspan=2)


    def retreive_vote(self):
        self._master_gui.blockFace.retreive_vote(self.vote_address.get())

    def vote(self):
        if ( self._master_gui.blockFace.keystore == None):
            self._master_gui.error_box1('No local account selected!\nAdd keystore in "Connect" tab')
        elif (self._master_gui.blockFace.w3 == None):
            self._master_gui.error_box1('Not connected! Select provider in "Connect" tab')
        elif ( not self._master_gui.blockFace.w3.isAddress(self.vote_address.get()) ):
            self._master_gui.error_box1("Provided contract address is not valid")
        elif ( self.selectedCandidate.get() == 'Select' or self.selectedCandidate.get() == ' -- N/A --' ):
            self._master_gui.error_box1("You need to retreive vote details\n"
                                       + "and select the candidate")
        elif not self._master_gui.blockFace.checkIfOpen():
            self._master_gui.error_box1("Looks like this vote is closed")
        else:
            self._master_gui.blockFace.vote( self.vote_address.get(),
                                             self.candidates_dict[self.selectedCandidate.get()],
                                             self.selectedCandidate.get()
                                             )
        
    def refresh(self):
        self.candidateMenu.destroy()
        self.selectedCandidate.set("Select")
        self.candidateMenu = OptionMenu(self.frame, self.selectedCandidate, *self.candidates_dict.keys())
        self.candidateMenu.config(width=20)
        self.candidateMenu.grid(row=8, column=1, padx=0, pady=(20,0), sticky='w')

