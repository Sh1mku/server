from socket import *

HOST = "127.0.0.1"           # Host IP
PORT = 6000                   # available port
socket = socket(AF_INET, SOCK_STREAM)
socket.connect((HOST, PORT))      
msg = socket.send("Hello".encode()) # sending the message to the server          
while True:     # starting the connection to the server
    serverMsg = socket.recv(1024).decode() 
    print(serverMsg)                                 # printing the message from the server
    msg = input("admin-98765")              # entering the message
    socket.send(msg.encode())               # sending the message to the server