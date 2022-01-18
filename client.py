import threading
import socket
# receives a string pointing to the alias list on the server:
alias = input('Choose an alias >>> ')
# create a client socket:
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connects to the server:
client.connect(('127.0.0.1', 59000))

# The function handles data received by each instance of the client: 
def client_receive():
    while True:
        try:
            # receives data from the server:
            message = client.recv(1024).decode('utf-8')
            # sends the 'alias' string back to the server:
            if message == 'alias?':
                client.send(alias.encode('utf-8'))
            # receives the message from another instance of a client:
            else:
                print(message)
        # handles exceptions in 
        except:
            print('Error!')
            # Close the socket upon an exception:
            client.close()
            break

# The function handles data sent by each instance of the client: 
def client_send():
    while True:
        # receives data in string format:
        message = f'{alias}: {input("")}'
        # converts and sends data from the client in byte format:
        client.send(message.encode('utf-8'))

# receives data for each client instance:
receive_thread = threading.Thread(target = client_receive)
receive_thread.start()

# sends data from each client instance:
send_thread = threading.Thread(target = client_send)
send_thread.start()