from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from contract_logic import *

class GetResultsFrame:
    def __init__(self, master_gui, notebook, _width):
        
        self.frame = Frame(notebook, width = _width)
        self.frame.pack(fill="both", expand=1)
        notebook.add(self.frame, text="Get Results")
        self._master_gui = master_gui

        self.vote_address = StringVar()
        self.vote_address.set("")
        self.vote_name = StringVar()
        self.vote_name.set('--- No Vote Contract specified ---  ')
        self.start = StringVar()
        self.start.set(' -- N/A --')
        self.end = StringVar()
        self.end.set(' -- N/A --')

        self.candidates_dict = {}
        self.voter_count = 0
        self.results_dict = {}

        self.label_1 = Label(self.frame, text="Provide address of the Vote Contract:")
        self.label_1.grid(row=0, column=0, columnspan=2, padx=10, pady=(30,0), sticky='w')

        self.entry_1 = Entry(self.frame, textvariable=self.vote_address, justify=LEFT, width=50)
        self.entry_1.grid(row=1, column=0, columnspan=2, padx=10, pady=(0,10), sticky='w')

        self.button_1 = Button(self.frame, text="Retreive results", command=self.retreive, justify=LEFT)
        self.button_1.grid(row=2, column=0, columnspan=2, padx=10, pady=(10,10),sticky='w')

# Display vote details:

        self.label_2 = Label(self.frame, text='Vote name:', justify=LEFT)
        self.label_3 = Label(self.frame, textvariable=self.vote_name, justify=LEFT)
        self.label_2.grid(row=3, column=0, columnspan=2, padx=10, pady=(15,0), sticky='w')
        self.label_3.grid(row=4, column=0, columnspan=2, padx=10, pady=(0,0), sticky='w')
        
        self.label_4 = Label(self.frame, text="Vote start:", justify=LEFT)
        self.label_4.grid(row=5, column=0, padx=(10,10), pady=(15,0), sticky='w')
        self.label_5 = Label(self.frame, text="Vote end:", justify=LEFT)
        self.label_5.grid(row=6, column=0, padx=(10,10), pady=(15,0), sticky='w')

        self.label_4_1 = Label(self.frame, textvariable=self.start, justify=LEFT)
        self.label_4_1.grid(row=5, column=1, padx=0, pady=(15,0), sticky='w')
        self.label_5_1 = Label(self.frame, textvariable=self.end, justify=LEFT)
        self.label_5_1.grid(row=6, column=1, padx=0, pady=(15,0), sticky='w')

        self.label_6_0 = Label(self.frame, text='RESULTS', font='bold', justify=LEFT)
        self.label_6_0.grid(row=7, column=0, columnspan=2, padx=10, pady=(15,0), sticky='w')
        self.label_6 = Label(self.frame, text='Candidate:', justify=LEFT)
        self.label_6_1 = Label(self.frame, text='Votes:', justify=LEFT)
        self.label_6.grid(row=8, column=0, padx=10, pady=(15,0), sticky='w')
        self.label_6_1.grid(row=8, column=1, padx=10, pady=(15,0), sticky='w')
        self.text = Text(self.frame, spacing3=10, width=50, height=10)
        self.text.grid(row=9, column=0, columnspan=2, padx=10, pady=0)


    def printResults(self):
        results = sorted(self.results_dict.items(), key=lambda item: item[1], reverse=True)
        for i in results:
            self.text.insert(END, self.candidates_dict[i[0]] + " - " + str(i[1]) + "\n"  )

    def retreive(self):
        self.candidates_dict = {}
        self.voter_count = 0
        self.results_dict = {}
        self.text.delete('1.0', END)
        if (self._master_gui.blockFace.w3 == None):
            self._master_gui.error_box1('Not connected! Select provider in "Connect" tab')
        elif ( not self._master_gui.blockFace.w3.isAddress(self.vote_address.get()) ):
            self._master_gui.error_box1("Provided contract address is not valid")
        #elif not self._master_gui.blockFace.checkIfClosed():
        #    self._master_gui.error_box1("Looks like this vote is not closed yet")
        self._master_gui.blockFace.retreive_results(self.vote_address.get())
        self.printResults()
        
        
        return
        

       
