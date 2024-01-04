from socket import *

HOST = "127.0.0.1"           # Host IP
PORT = 8888                   # available port
socket = socket(AF_INET, SOCK_STREAM)
socket.connect((HOST, PORT))


socket.send("admin-123".encode())
msg=socket.recv(1024).decode()
print(msg)

