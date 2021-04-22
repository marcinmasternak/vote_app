from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from contract_logic import *
from datetime import datetime
from web3 import Account
import os

class CreateAccountFrame:
    def __init__(self, master_gui, notebook, _width):
        
        frame = Frame(notebook, width = _width)
        frame.pack(fill="both", expand=1)
        notebook.add(frame, text="Create Account")
        self._master_gui = master_gui

        self.keystore_pass = None
        self.keystore_name = StringVar()
        self.keystore_name_default = "new_keystore_ +current_date"
        self.keystore_name.set(self.keystore_name_default)
        #self.keystore = None
        #self.keystore_pass = None
      

        #Defining the widgets

        #Get new keystore name
        self.label_1 = Label(frame, text='Enter name for the key-store file:', justify=LEFT)
        self.entry_1 = Entry(frame, textvariable=self.keystore_name, width=42)
        self.button_1 = Button(frame, text="Create account", command=self.createAccount, justify=LEFT)

        self.label_1.grid(row=0, column=0, padx=10, pady=(30,0), sticky='w')
        self.entry_1.grid(row=2, column=0, padx=10, pady=(0,0), sticky='w')
        self.button_1.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        

        
    def createAccount(self):
        self._master_gui.password_box1("Provide password for the key-store.")
        password = self._master_gui.blockFace.password
        self._master_gui.password_box1("Verify password for the key-store.")

        if ( password != self._master_gui.blockFace.password):
            self._master_gui.error_box1("Passwords don't match")
            return
        
        account = Account.create()
        keystore = account.encrypt(password)
        if ( self.keystore_name.get() == self.keystore_name_default ):
            self.keystore_name.set( "new_keystore_" + datetime.now().strftime("%d-%m-%Y-%H:%M:%S") )
        try:
            print(self.keystore_name.get())
            with open("Key_Stores" + os.path.sep + self.keystore_name.get(), 'w') as handle:
                json.dump(keystore, handle)
            self._master_gui.message_box1( 'Account created',
                                           'Address:\n' + account.address +
                                           '\n\nKeystore location:\n' + os.getcwd() + os.path.sep + "Key_Stores"
                                           + os.path.sep + '\n\nKeystore name:\n' + self.keystore_name.get()
                                           )
            self.keystore_name.set(self.keystore_name_default) 
        except Exception as err:
            self._master_gui.error_box1(err)
