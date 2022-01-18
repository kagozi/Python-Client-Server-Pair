'Server-Client-Client Room Connection'
import socket
import threading

host = '127.0.0.1'
#choose a port that is not reserved: check by running netstat on cmd:
port = 59000    
#AF_INET is an address family that is used to designate the type of addresses that your socket can communicate with:
#SOCK_STREAM means that it is a TCP socket:
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind() assigns an IP address and a port number to a socket instance:
server.bind((host, port))
# listen() makes a socket ready for accepting connections:
server.listen() 
# we create a list of clients and aliases to store the endpoints and aliases respectively:
clients = []
aliases = []

#send a message from the server to all the clients:
# send() sends data from one socket to another socket
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle client connection:
def handle_client(client):
    while True:
        try:
            #.recv() enables the client to receive data from the server:
            message = client.recv(1024)
            # the broadcast() function is called here to send the message:
            broadcast(message)
        except:
            # incase a client breaks from the connection:
            index = clients.index(client)
            clients.remove(client)
            clients.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

# Function to handle communication:
def receive():
    while True:
        print('Server is running and listening...')
        # An accept() object accepts an incoming connection request from a TCP client. Called on the server socket:
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        # receive data from/through the server:
        alias = client.recv(1024)
        # the lists are updated each time a new client joins the connection:
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        # represents an activity that is run in a separate thread of control:
        thread = threading.Thread(target = handle_client, args=(client,))
        # start the activity of the thread object:
        thread.start()

# starts the server if the module is run internally:
if __name__ == "__main__":
    receive()


