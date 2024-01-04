from socket import *
from time import sleep

HOST = "127.0.0.1"           # Host IP
PORT = 8888                   # available port
socket = socket(AF_INET, SOCK_STREAM)
socket.connect((HOST, PORT))      
 # sending the message to the server          
# starting the connection to the server                            # printing the message from the server
msg = "user-123"              # entering the message
socket.send(msg.encode())               # sending the message to the server

servermsg=socket.recv(1024).decode()
print(servermsg)
while True:
    print("A")
    msg = "chgPass-222"              # entering the message
    socket.send(msg.encode())  
    sleep(2)