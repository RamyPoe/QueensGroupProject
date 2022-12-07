import select, socket, traceback, time
from queue import Queue
from database import Database
from cipher import Cipher
import config, protocol
import hashlib, rsa, pickle
from math import ceil

# Constant for sending messages
FORMAT = 'utf-8'
# TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Non-blocking IO
server.setblocking(0)
# IP, PORT
ADDR = ('localhost', config.PORT) if config.LOCALHOST else (socket.gethostbyname(socket.gethostname()), config.PORT)
server.bind(ADDR)
# Number of Unaccepted connections before refusing new ones (5)
server.listen(5)
# Debug
print("[SERVER] " + str(ADDR))
print("[SERVER] Listening for connections...\n")

# For communication
inputs = [server]
outputs = []
message_queues = {}

# For storing data
db = Database()

#==================================================================================================

""" High level bundle for conn, cipher, username """
class ClientBundle:
    def __init__(self, conn, cipher):
        self.conn = conn
        self.cipher = cipher
        self.username = ""
    
    def fileno(self): return self.conn.fileno()
    def send(self, msg): self.conn.send(self.cipher.encrypt(msg))
    def recv(self, bytes): return cipher.decrypt(self.conn.recv(bytes)).decode(FORMAT)
    def close(self): self.conn.close()
    def logged_in(self): return True if self.username != "" else False


""" Disconnect client and remove traces """
def disconnect(s):
    global inputs, outputs, message_queues

    if s in outputs:
        outputs.remove(s)
    inputs.remove(s)
    s.close()
    del message_queues[s]
    print("[CLIENT] Disconnected...\n")


""" Return hash string for given string """
def compute_hash(data : str) -> str:
    return hashlib.sha224(data.encode(FORMAT)).hexdigest()


""" Sets everything up for message to be sent to socket """
def send_msg(s, msg, encode = True):
    global message_queues, outputs

    # Add msg to queue
    if encode: message_queues[s].enqueue(msg.encode(FORMAT))
    else: message_queues[s].enqueue(msg)
    
    # Add socket to write list
    if s not in outputs:
        outputs.append(s)

""" Cuts message into portions to be encrypted and sent, allows for larger messages """
def send_byte_dump(s, out : bytes):
    # Send number of blocks for receiver
    send_msg(s, str ( ceil ( len(out) / s.cipher._max_msg ) ) )

    while out:
        # Cut portion to be encrypted
        buff = out[:s.cipher._max_msg]
        out = out[s.cipher._max_msg:]
        # Add portion to queue to send
        send_msg(s, buff, encode=False)

""" Receives portions of messages and stiches them together """
def recv_byte_dump(s, num_blocks : int):
    if config.VERBOSE_OUTPUT: print(f"[DUMP] Number of Blocks: {num_blocks}")
    # Must wait until data is received
    s.conn.settimeout(0.3)
    # Read all pieces and put together
    buff = b''
    for i in range(num_blocks):
        buff += s.cipher.decrypt ( s.conn.recv(1024) )
    # Fix socket for non-blocking
    s.conn.setblocking(False)
    # Return de-serialized
    return pickle.loads( buff )

#==================================================================================================



while inputs:
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs)

    for s in readable:
        if s is server:
            # Accept new client
            connection, client_address = s.accept()

            # Complete cipher handshake
            cipher = Cipher()
            connection.setblocking(True)
            new_key = connection.recv(2048).decode(FORMAT)
            cipher.addKeyFromString(new_key)
            connection.send(cipher.getPublicKey().encode(FORMAT))
            if config.VERBOSE_OUTPUT: print("[CLIENT KEY] " + str(cipher.encryptKey)); print("[SERVER KEY] " + str(cipher.publicKey))
            
            # Bundle connection with cipher
            client = ClientBundle(connection, cipher)

            # Set to non-blocking IO
            connection.setblocking(False)
            # Add to list of connected clients
            inputs.append(client)
            # Add queue for client
            message_queues[client] = Queue()
            #Debug
            print("[CLIENT] Got new connection")

        else:
            try:
                # Read msg
                data = s.recv(2048)

                if data:
                    # Print msg
                    if config.VERBOSE_OUTPUT: print(f"[CLIENT MESSAGE] {data}")
                    
                    #Get code for processing
                    op_code = int ( data.split(":")[0] )
                    data = data.split(":")[1]

                    # Process
                    match (op_code):
                        case protocol.REGISTER_REQ:
                            # Seperate username and password
                            username, password = data.split(",")
                            password = compute_hash(password)
                            # Cannot register, user already exists
                            if db.keyExists(username):
                                send_msg(s, str(protocol.REGISTER_FAIL))
                                print(f"[REGISTER] Client failed to register, user \"{username}\" already exists")
                            else:
                                # Add to database using default values
                                db.addKey(username, [password] + db.keyDump("MockUser"))
                                send_msg(s, str(protocol.REGISTER_SUCCESS))
                                print(f"[REGISTER] New Client registered: {username}")


                        case protocol.LOGIN_REQ:
                            # Seperate username and password
                            username, password = data.split(",")
                            password = compute_hash(password)
                            # Cannot login, user doesn't exist
                            if not db.keyExists(username):
                                send_msg(s, str(protocol.LOGIN_FAIL))
                                print(f"[LOGIN] Client failed to login, user \"{username}\" does not exist")
                            else:
                                if (db.getPassHash(username) != password):
                                    send_msg(s, str(protocol.LOGIN_FAIL))
                                    print(f"[LOGIN] Client failed to login, user \"{username}\" has wrong password")
                                else:
                                    # Let the user know login was successfull so they can recv the buffer
                                    send_msg(s, str(protocol.LOGIN_SUCCESS))
                                    print(f"[LOGIN] Client \"{username}\" successfully logged in")
                                    # Set user as logged in locally
                                    s.username = username
                                    # Serialize using pickle
                                    out = pickle.dumps( db.keyDump ( username ) )
                                    # Send data
                                    send_byte_dump(s, out)
                                    print(f"[LOGIN] Sending client's user data...")

                        case protocol.UPDATE_INFO:
                            # Receive what client has to send
                            data_type = int ( data.split(';')[0] )
                            new_data = recv_byte_dump(s, int(data.split(';')[1]))

                            # Only update info if client is logged in
                            if s.logged_in():
                                if config.VERBOSE_OUTPUT: print(f"[SERVER] Got new user data: {new_data}")
                                print(f"[SERVER] Updating user data for \"{s.username}\"")
                                db.updateKey(s.username, new_data, data_type)

                            else:
                                print("[SERVER] Client may not update data before logging in")

                                    


                

                else:
                    # Disconnect client, can't send nothing
                    disconnect(s)
            
            except rsa.pkcs1.DecryptionError:
                # Can't decrypt bad message
                disconnect(s)
            except ConnectionResetError:
                # Client force quit
                disconnect(s)

            except Exception as e:
                # Display error
                print(f"[CLIENT ERROR] {e}")
                print(traceback.format_exc())
                # Disconnect client
                disconnect(s)


    for s in writable:
        
        if ( not message_queues[s].isEmpty() ):
            # Get next message in queue
            next_msg = message_queues[s].dequeue()
                            
            try:
                #Bugs out when you send things too fast
                time.sleep(0.005)
                # No error, send message
                if config.VERBOSE_OUTPUT: print(f"[SERVER] Sending data: {next_msg}")
                s.send(next_msg)

            except Exception as e:
                print(f"[SERVER] Sending failed! {e}")
                print(traceback.format_exc())
                outputs.remove(s)

        else:
            outputs.remove(s)


    # Disconnect those that throw errors
    for s in exceptional:
        # Disconnect Client
        disconnect(s)