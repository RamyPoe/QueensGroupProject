import socket
import time, threading
from cipher import Cipher
import protocol
import pickle
from math import ceil

class Network:
    
    """ Constructor """
    def __init__(self):
        # Constant
        self.FORMAT = 'utf-8'
        # Create a TCP/IP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Cipher for encrypted traffic
        self.cipher = Cipher()

        # self.status is one of:
        #   - 0         (Not connected)
        #   - 1         (Failed to connect)
        #   - 2         (Connected)
        self.status = 0


    """ Connects to server, must be done before all other operations """
    def connect_to(self, ip : str, port : int):
        try:
            # Connect the socket to the port where the server is listening
            print( f"[CONNECTING] IP: {ip} \t PORT: {port}" )
            self._sock.connect((ip, port))
            self.handshake()
            self.status = 2
        except:
            self.status = 1


    """ Exchanges keys with Server after connecting """
    def handshake(self):
        self._sock.send(self.cipher.getPublicKey().encode(self.FORMAT))
        new_key = self._sock.recv(2048).decode(self.FORMAT)
        self.cipher.addKeyFromString(new_key)
        print()
        

    """ Sends msg to server over socket """
    def send(self, msg : str):
        try:
            print(f"[NETWORKING] Message bytes: {len(msg.encode(self.FORMAT))}")
            self._sock.send(self.cipher.encrypt(msg.encode(self.FORMAT)))
        except Exception as e:
            print(f"[NETWORK] Send failed! {e}")
    

    """ Blocks until message is sent, returns the message """
    def recv(self):
        msg = self._sock.recv(2048)
        return self.cipher.decrypt(msg).decode(self.FORMAT)

    """ Returns list of data that server has for the user """
    def recvPersonalData(self):
        # Number of pieces msg has been split into
        num_blocks = int ( self.recv() )
        print(f"[DUMP] Number of Blocks: {num_blocks}")

        # Read all pieces and put together
        buff = b''
        for i in range(num_blocks):
            buff += self.cipher.decrypt ( self._sock.recv(1024) )
        # Return de-serialized
        return pickle.loads( buff )
    
    """ Sends updated data to be stored on server """
    def updatePersonalData(self, data, data_type):
        if not data_type in [protocol.APPOINMENTS, protocol.HEALTHCARD, protocol.INFORMATION, protocol.VACCINES]: raise ValueError("Invalid argument for type of data")
        # Get right data
        data = data[protocol.DATA_INDEXES[data_type]]
        # Turn data into bytes
        out = pickle.dumps ( data )
        # Let server know we are trying to update, along the number of blocks to receive it
        self.send(f"{protocol.UPDATE_INFO}:{data_type};" + str ( ceil ( len(out) / self.cipher._max_msg ) ) )

        while out:
            # Cut portion to be encrypted
            buff = out[:self.cipher._max_msg]
            out = out[self.cipher._max_msg:]
            # Send portion to Server
            time.sleep(0.005)
            self._sock.send( self.cipher.encrypt ( buff ) )

    """ Sends request to register to server, username and password should be well regexed """
    def register(self, username : str, password : str):
        out = str( protocol.REGISTER_REQ ) + ":" + username + "," + password
        self.send(out)
        response = int ( self.recv() )
        
        match (response):
            case protocol.REGISTER_FAIL:
                print("[REGISTER] Failed!")

            case protocol.REGISTER_SUCCESS:
                print("[REGISTER] Successfull!")
        
        return response

    """ Send login request to server with credentials, returns server response code """
    def login(self, username : str, password : str):
        # Formulate request for server
        out = str( protocol.LOGIN_REQ ) + ":" + username + "," + password
        self.send(out)
        response = int ( self.recv() )

        # Print appropriate response
        match (response):
            case protocol.LOGIN_FAIL:
                print("[LOGIN] Failed!")
                

            case protocol.LOGIN_SUCCESS:
                print("[LOGIN] Successfull!")
                return response
    

        return response      

class MockNetwork:
    def __init__(self, b : bool): self.status = 2 if b else 1
    def connect_to(self, ip : str, port : int): pass
    def handshake(self): pass
    def send(self, msg : str): pass    
    def recv(self): pass
    def recvPersonalData(self): pass
    def updatePersonalData(self, data): pass
    def register(self, username : str, password : str): pass
    def login(self, username : str, password : str): return protocol.LOGIN_SUCCESS, [' ', ' ', ' ', ' ']
        

def run_background(func, *_args):
    t = threading.Thread(target=func, args=_args)
    t.start()


#----------------------------------+
# ╭━━━┳━╮╭━┳━━━┳━╮╭━┳━━━┳╮╱╱╭━━━╮  |
# ┃╭━━┻╮╰╯╭┫╭━╮┃┃╰╯┃┃╭━╮┃┃╱╱┃╭━━╯  |
# ┃╰━━╮╰╮╭╯┃┃╱┃┃╭╮╭╮┃╰━╯┃┃╱╱┃╰━━╮  |
# ┃╭━━╯╭╯╰╮┃╰━╯┃┃┃┃┃┃╭━━┫┃╱╭┫╭━━╯  |
# ┃╰━━┳╯╭╮╰┫╭━╮┃┃┃┃┃┃┃╱╱┃╰━╯┃╰━━╮  |
# ╰━━━┻━╯╰━┻╯╱╰┻╯╰╯╰┻╯╱╱╰━━━┻━━━╯  |
#----------------------------------+

"""
import networking
import protocol
import time

net = networking.Network()

net.connect_to('localhost', 9848)
code, info = net.login("test3@gmail.com", "abc")

time.sleep(1)

print(f"[DATA] {info}")
net.updatePersonalData([data.decode(), data.decode()], protocol.HEALTHCARD)
"""
