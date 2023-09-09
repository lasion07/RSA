# Import socket module
import socket			

from RSA_optimized import RSA_NHOM6

# Create a socket object
s = socket.socket()		

# Define the port on which you want to connect
port = 12345			

# connect to the server on local computer
s.connect(('127.0.0.1', port))

rsa = RSA_NHOM6()

rsa.load_key('keys/server_public_key.txt', 'keys/client_private_key.txt')

message = ''

while True:
    # Enter message
    message = input("->")

    if message == 'quit':
        break

    # Send message to server
    s.send(rsa.encode(message).encode())
    
    # Recieve message from server
    data = s.recv(1024).decode()
    print(data)


# close the connection
s.close()	
	
