from web3 import Web3
import json
from tkinter import *
from web3 import exceptions
from datetime import datetime


def loadVariables():
    try:
        with open('variables.json', 'r') as file_handler:
            variables_dict = json.load(file_handler)
            return variables_dict
    except Exception as my_exception:
        return my_exception.args[1]


   


class BlockchainInterface:

    
    def __init__(self, master_gui):
        self._master_gui = master_gui
        self.w3 = None
        self.provider = None
        self.address = None
        self.keystore = None
        self.abi = None
        self.bytecode = None
        self.gas = None
        self.vote_name = None
        self.password = None

        #for deploy contract method
        self.tx_receipt = None

        #for retreive contract method
        self.vote_contract = None
        self.fingerprint = 'thisisvalidvoteappcontract654321'.encode('utf-8')
        self.open_time = None
        self.closed_time = None
        #--

        self.loadVariables()
        
        
    def loadVariables(self):

        try:
            with open(self._master_gui.varDict['abi_path'], 'r') as handle:
                self.abi = handle.read().rstrip()
        except Exception as err:
            self._master_gui.error_box1('Error during loading abi from file:\n' + err)
        
        
        try:
            with open(self._master_gui.varDict['bytecode_path'], 'r') as file_handler:
                full_bytecode_from_remix = json.load(file_handler)
                self.bytecode = full_bytecode_from_remix['object']
        except Exception as err:
            self._master_gui.error_box1('Error during loading bytecode from file:\n' + err)

        self.provider = self._master_gui.varDict['provider']
        self.gas = self._master_gui.varDict['gas']   
           

    def getPassword(self, _root):
        def printout():
            self.keystore_password = password_var.get()
            t.destroy()
        t = Toplevel(_root)
        t.wm_title("Password entry")
        l = Label(t, text="\nEnter password to the selected key store:\n")
        l.pack()
        password_var = StringVar()
        passEntry = Entry(t, textvariable=password_var, show='\u2022').pack()
        submit = Button(t, text='Submit', command=printout).pack()

    def sign(self, _construct_txn):
        self._master_gui.password_box1("Enter password to the keystore")
        try:
            key = self.w3.eth.account.decrypt(self.keystore, self.password)
            self.password = None
            account = self.w3.eth.account.privateKeyToAccount(key)
            signed = account.signTransaction(_construct_txn)
            return signed
        except Exception as err:
            raise SignError( type(err).__name__ + "\n" + err.args[0] + "\n\n" + "Wrong password!?" )
            #self._master_gui.error_box1( type(err).__name__ + "\n" + err.args[0] + "\n\n" + "Wrong password!?")
            #return False

    def checkAddress(self, address):
        if ( Web3.isAddress(address) ):
            return True
        else:
            return False

    def toChecksum(self):
        return Web3.toChecksumAddress(self.keystore['address'])

        
    def connect(self):
        self.w3 = Web3(Web3.HTTPProvider(self.provider))

     
    def is_connected(self):
        if ( self.w3 != None ) and ( self.w3.isConnected() ):
            return('Connected!')
        else:
            return('Not connected!')

    def deploy(self, start_time, end_time, candidates, name):

        vote_contract = self.w3.eth.contract(abi = self.abi, bytecode = self.bytecode)
        address = self.w3.toChecksumAddress(self.keystore['address'])

        #gas = vote_contract.constructor(start_time, end_time, candidates).estimateGas()
        
        txn = {'from' : address,
               'nonce' : self.w3.eth.getTransactionCount(address),
               'gas' : self.gas,
               'gasPrice' : self.w3.toWei('40', 'gwei')}
        
               
        construct_txn = vote_contract.constructor(start_time, end_time, candidates, name, self.fingerprint).buildTransaction(txn)

        try:
            signed = self.sign(construct_txn)
            self.tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
            self.tx_receipt = self.w3.eth.waitForTransactionReceipt(self.tx_hash)
            self._master_gui.message_box1("Contract deployed!",
                                      "Name:\n" + name + "\n\n"
                                      + "Address:\n" + self.tx_receipt['contractAddress'])

            vote_contr = self.w3.eth.contract(address=self.tx_receipt['contractAddress'], abi=self.abi)
            ret_name = vote_contr.caller().vote_name()
        except Exception as err:
            self._master_gui.error_box1(err)

    def retreive_vote(self, _address):
        if (self.w3 == None):
            self._master_gui.error_box1('Not connected! Select provider in "Connect" tab')
            return
        elif ( not Web3.isAddress(_address) ):
            self._master_gui.error_box1("Provided string is not a valid contract address")
            return

        self.retreived_contract = self.w3.eth.contract(
            address = _address,
            abi = self.abi)

        try:
            finger_print = self.retreived_contract.functions.getFingerprint().call()
            
            if ( finger_print != self.fingerprint ):
                self._master_gui.error_box1("Some old version of Vote App contract at this address.\n" +
                                            "How odd hhmm")
                return
        except Exception as err:
            self._master_gui.error_box1("No Vote App contract at this address!")
            return

        #get contact details form chain
        name = self.retreived_contract.caller().vote_name()
        self.open_time = self.retreived_contract.caller().open_time()
        self.close_time = self.retreived_contract.caller().close_time()
        candidate_count = self.retreived_contract.caller().candidate_count()
        self._master_gui.tab_4.candidates_dict = {}
        for i in range(candidate_count):
            candidate = self.retreived_contract.functions.getCandidate(i+1).call()
            self._master_gui.tab_4.candidates_dict[self.decodeBytes32(candidate)] = i+1

        #update Vote Tab with retreived values
        self._master_gui.tab_4.vote_name.set(name)
        self._master_gui.tab_4.start.set(datetime.fromtimestamp(self.open_time).strftime("%d/%m/%Y-%H:%M:%S"))
        self._master_gui.tab_4.end.set(datetime.fromtimestamp(self.close_time).strftime("%d/%m/%Y-%H:%M:%S"))

        self._master_gui.tab_4.refresh()

    def vote(self, _contract_address, candidate_id, candidate_name):
        try:
            checksum_contract_address = self.w3.toChecksumAddress(_contract_address)
            checksum_voter_address = self.w3.toChecksumAddress(self.keystore['address'])
            vote_contract = self.w3.eth.contract(abi = self.abi, address = checksum_contract_address)

            finger_print = vote_contract.functions.getFingerprint().call()
            if ( finger_print != self.fingerprint ):
                self._master_gui.error_box1("Some old version of Vote App contract at this address.\n" +
                                            "How odd hhmm")
                return
            
            txn = {'from' : checksum_voter_address,
               'nonce' : self.w3.eth.getTransactionCount(checksum_voter_address),
               'gas' : self.gas,
               'gasPrice' : self.w3.toWei('40', 'gwei')}
            prepared_transaction = vote_contract.functions.placeAVote(candidate_id).buildTransaction(txn)
            signed = self.sign(prepared_transaction)
            tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
            tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
            if (tx_receipt['status'] == 1):
                self._master_gui.success_box1('Vote placed for:\n' + candidate_name)
            else:
                self._master_gui.error_box1('Transaction failed\n\nVote not placed!\n\nAre you sure the vote is open?')
        except exceptions.SolidityError as err:
            print("Solidity error")
            self._master_gui.error_box1(err)
        except SignError as err:
            self._master_gui.error_box1(err.args[0])
        except Exception as err:
            print("Normal eror")
            self._master_gui.error_box1(err.args[0])

    def decodeBytes32(self, encoded):
        decoded = encoded.hex().rstrip("0")
        if len(decoded) % 2 != 0:
            decoded = decoded + '0'
        decoded = bytes.fromhex(decoded).decode('utf8')
        return(decoded)

    def checkIfOpen(self):
        now = datetime.now().timestamp()
        if (self.open_time != None):
            if ( (now >= self.open_time) and (now < self.close_time) ):
                return True
            else:
                return False

    def checkIfClosed(self):
        now = datetime.now().timestamp()
        if (self.closed_time != None):
            if (now > self.closed_time):
                return True
            else:
                return False

    def checkIfClosed1(self, open_t, close_t):
        now = datetime.now().timestamp()
        if (close_t == None ):
            self._master_gui.error_box1("Contract details not retreived")
            return False
        elif (now < close_t):
            self._master_gui.error_box1("Vote closes at:\n"
                                        + datetime.fromtimestamp(close_t).strftime("%d/%m/%Y-%H:%M:%S") )
            return False
        else:
            return True

    def retreive_results(self, vote_address):
        
        retreived_contract = self.w3.eth.contract(
            address = vote_address,
            abi = self.abi)

        try:
            finger_print = self.retreived_contract.functions.getFingerprint().call()
            
            if ( finger_print != self.fingerprint ):
                self._master_gui.error_box1("Some old version of Vote App contract at this address.\n" +
                                            "How odd hhmm")
                return
        except Exception as err:
            self._master_gui.error_box1("No Vote App contract at this address!")
            return

        #get contact details form chain
        name = self.retreived_contract.caller().vote_name()
        open_time = self.retreived_contract.caller().open_time()
        close_time = self.retreived_contract.caller().close_time()
        
        if not self.checkIfClosed1(open_time, close_time):
            return
        

        candidate_count = retreived_contract.caller().candidate_count()
        self._master_gui.tab_5.candidates_dict = {}
        #get candidate to id mapping
        for i in range(candidate_count):
            candidate = retreived_contract.functions.getCandidate(i+1).call()
            self._master_gui.tab_5.candidates_dict[i+1] = self.decodeBytes32(candidate)
            self._master_gui.tab_5.results_dict.setdefault(i+1,0)

        #update Vote Tab with retreived values
        self._master_gui.tab_5.vote_name.set(name)
        self._master_gui.tab_5.start.set(datetime.fromtimestamp(self.open_time).strftime("%d/%m/%Y-%H:%M:%S"))
        self._master_gui.tab_5.end.set(datetime.fromtimestamp(self.close_time).strftime("%d/%m/%Y-%H:%M:%S"))

        #get voter's count
        self._master_gui.tab_5.voter_count = retreived_contract.caller().voter_count()
        for i in range(self._master_gui.tab_5.voter_count):
            (vote, address) = retreived_contract.functions.getVote(i+1).call()
            current = self._master_gui.tab_5.results_dict.setdefault(vote, 0)
            self._master_gui.tab_5.results_dict[vote] = current + 1

    
class SignError(Exception):
    pass
                           
"""
    def connect_old(self, provider):
        self.w3 = Web3(Web3.HTTPProvider(provider))
        self.my_contract = self.w3.eth.contract(abi = self.abi, bytecode = self.bytecode)
        address = self.w3.toChecksumAddress(self.key_store['address'])
        txn = {'from' : address,
               'nonce' : self.w3.eth.getTransactionCount(address),
               'gas' : self.gas,
               'gasPrice' : self.w3.toWei(self.gas_price, 'gwei')}
        construct_txn = self.my_contract.constructor().buildTransaction(txn)
        signed = self.sign(construct_txn)
        self.tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        self.tx_receipt = self.w3.eth.waitForTransactionReceipt(self.tx_hash)
        return self.tx_receipt['contractAddress']
"""       

"""  
import json
>>> with open('test_son', 'w') as handle:
	handle.write(json.dumps([abi, 'idle0x00f1e5fF2b58e219Fd1F67f53a300bf3c24d61eF']))


	urllib.request.urlopen('https://raw.githubusercontent.com/marcinmasternak/vote_app/master/abi')
<http.client.HTTPResponse object at 0x7f85ce8d9580>
>>> stream = urllib.request.urlopen('https://raw.githubusercontent.com/marcinmasternak/vote_app/master/abi')
>>> x = stream.read()
Deployed test vote address (on ganache so valid only until restart)

Just contr for testing:
0x3a58C3136254c69373E23B5dde225AA6c09e0814

Infura
0xcbb2e40D3247e0765E8d8B6421F1d2fBaf1C34B3
https://ropsten.infura.io/v3/4773b05b3c0249faae8f90f659c0a96d


"""
