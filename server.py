# first of all import the socket library
import socket

from RSA_optimized import RSA_NHOM6

# next create a socket object
s = socket.socket()
print ("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345			

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))		
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)	
print ("socket is listening")	

# Establish connection with client.
c, addr = s.accept()
print('Got connection from', addr )

rsa = RSA_NHOM6()

rsa.load_key('keys/client_public_key.txt', 'keys/server_private_key.txt')

# a forever loop until we interrupt it or
# an error occurs
while True:
    # Recieve message from client
    data = c.recv(1024).decode()

    if not data:
        break

    print('\n-----NEW MESSAGE----')
    print('Cipher text: \n', data)
    plaintext = rsa.decode(data)
    print('Plain text: \n', plaintext)

    # Send message to client
    c.send(f'Server recieved: {plaintext}'.encode())

c.close()
