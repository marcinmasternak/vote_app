from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from contract_logic import *
from deploy_frame import *
from create_account_frame import *
from vote_frame import *
from get_results_frame import *
from connect_frame import *


class Gui:
    def __init__(self, master):

        self.start_width = master.winfo_screenwidth() // 6
        self.start_height = master.winfo_screenheight() // 6
        master.geometry('+' + str(self.start_width) + '+' + str(self.start_height))
        master.title('Voting App')
        self._master = master

        main_frame = Frame(master)
        main_frame.pack()
        x = 0

        self.quitPass = IntVar()

        #Loading dictionary of default values
        try:
            with open('variables.json', 'r') as handle:
                self.varDict = json.loads(handle.read())
        except Exception as err:
            print(err)
            
         
       
        
        #Initializing Blockchain Interface

        self.blockFace = BlockchainInterface(self)
        
        #Defining variables

        self.text_var_1 = StringVar()
        self.text_var_2 = StringVar()
        self.text_var_2.set('http://127.0.0.1:8545')
        self.text_var_5 = StringVar()
        self.text_var_5.set('1234567')
        self.text_var_6 = StringVar()
        self.text_var_6.set('21')
        self.pw = ''

        #Defining the tabs for the top menu

        self.my_notebook = ttk.Notebook(main_frame)
        self.my_notebook.pack(pady=15)

        

        self.tab_1 = ConnectFrame(self, self.my_notebook, 450)
        self.tab_2 = DeployFrame(self, self.my_notebook, 450)
        self.tab_3 = CreateAccountFrame(self, self.my_notebook, 450)
        self.tab_4 = VoteFrame(self, self.my_notebook, 450)
        self.tab_5 = GetResultsFrame(self, self.my_notebook, 450) #,470

        

    #Defining functions


    def create_window(self, message):
            t = Toplevel(self._master)
            t.geometry('400x200+' + str(self.start_width + 70) + '+' + str(self.start_height + 300))
            t.wm_title("Success")
            l = Label(t, text="\nContract deployed to address:\n")
            l.grid(row=0, column=0, padx=10, pady=10)
            var = StringVar()
            var.set(message)
            e = Entry(t, textvariable=var, width = 43)
            e.grid(row=1, column=0, padx=10, pady=10)
            

    def message_box1(self, title, content):
            t = Toplevel(self._master)
            t.resizable(0,0)
            #t.overrideredirect(True)
            t.geometry('+' + str(self.start_width + 130) + '+' + str(self.start_height + 250))
            var = StringVar()
            var.set(title)
            t.wm_title(var.get())
            
            #l = Label(t, textvariable=var, justify=CENTER)
            #l.grid(row=0, column=0, padx=10, pady=10)
            
            var1 = StringVar()
            var1.set(content)
            e = Text(t, width = 45, height=8)
            e.insert(END, var1.get())
            e.grid(row=1, column=0, padx=10, pady=10)

            b = Button(t, text="Close", command= lambda : t.destroy(), justify=CENTER)
            b.grid(row=2, column=0, padx=10, pady=10)
            t.bind('<Return>', lambda event : t.destroy() )

    def password_box1(self, message):
            def returner(self, t, password):
                self.blockFace.password = password
                self.quitPass.set(1)
                t.destroy()
                
            t = Toplevel(self._master)
            t.resizable(0,0)
            #t.overrideredirect(True)
            t.geometry('+' + str(self.start_width + 130) + '+' + str(self.start_height + 250))
            t.wm_title("Password entry")
            password = StringVar()
            endVar = IntVar()
            
            l = Label(t, text=message, justify=CENTER)
            l.grid(row=0, column=0, padx=10, pady=10)
            
            e = Entry(t, textvariable=password, show='\u2022', width = 20)
            e.grid(row=1, column=0, padx=10, pady=10)
            e.focus()

            b = Button(t, text="OK", command= lambda : returner(self, t, password.get()), justify=CENTER)
            b.grid(row=2, column=0, padx=10, pady=10)
            t.bind('<Return>' , lambda event : returner(self, t, password.get()) )
            t.wait_variable(self.quitPass)
    
    def error_box1(self, message):
            t = Toplevel(self._master)
            t.resizable(0,0)
            #t.overrideredirect(True)
            t.geometry('+' + str(self.start_width + 130) + '+' + str(self.start_height + 250))
            t.wm_title("Error")
            var = StringVar()
            var.set(message)
            l = Label(t, textvariable=var, justify=CENTER)
            l.grid(row=0, column=0, padx=10, pady=10)
            b = Button(t, text="Close", command= lambda : t.destroy(), justify=CENTER)
            b.grid(row=1, column=0, padx=10, pady=10)
            t.bind('<Return>', lambda event : t.destroy() )

    def success_box1(self, message):
            t = Toplevel(self._master)
            t.resizable(0,0)
            #t.overrideredirect(True)
            t.geometry('+' + str(self.start_width + 130) + '+' + str(self.start_height + 250))
            t.wm_title("Success!")
            var = StringVar()
            var.set(message)
            l = Label(t, textvariable=var, justify=CENTER)
            l.grid(row=0, column=0, padx=10, pady=10)
            b = Button(t, text="Close", command= lambda : t.destroy(), justify=CENTER)
            b.grid(row=1, column=0, padx=40, pady=10)
            t.bind('<Return>', lambda event : t.destroy() )
            
"""
    def file_opener(self):
        input = filedialog.askopenfilename(initialdir=".")
        self.text_var_1.set(input)
        with open(input) as handle:
            key_store = handle.read()

    
        

    def commit_funct(self):
        print(BlockchainInterface.getPassword(self))
        deployer = BlockchainInterface( self.entry_1.get(), self.entry_2.get(), self.entry_3.get("1.0", END),
                                    self.entry_4.get("1.0", END), self.entry_5.get(), self.entry_6.get() )
        contractAddress = deployer.connect()
        #messagebox.showinfo('Success', 'Contract has been deployed to:\n' + contractAddress)
        self.create_window(contractAddress)
"""


root = Tk()
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='icon3.png'))
gui = Gui(root)
root.mainloop()

