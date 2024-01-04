
import socket
from threading import Thread
import time
from queue import Queue
import AdminThread
from ServerClass import ServerClass
import UserThread


#create socket for external connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "127.0.0.1"
PORT = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))

print("Server is started")
print("Waiting for connections")


if __name__ == "__main__":
    #initialize the queue for interthread communication
    queue_user = Queue()
    queue_update_user = Queue()
    queue_admin_send = Queue()
    queue_admin_recieve = Queue()
    queue_user_recieve = Queue()
    #initialize & start the server thread
    serverThread = ServerClass(queue_user,queue_admin_recieve, queue_admin_send,queue_update_user)
    serverThread.start()
    newUserThread=0
    newAdminThread=0
    i=0
    while True:
        print(i)
        server.listen()
        clientsocket, address = server.accept()
        login=clientsocket.recv(1024).decode()
        login = login.split("-")

        #check the usertype & password
        if login[0] == "admin" and login[1] == "123":
            print(f"Connection from {address} has been established!")
            #assueme that admin always closes connection after they are done checking what is wrong before connecting again
            newAdminThread = AdminThread.AdminThread(clientsocket, address, 5, queue_admin_send, queue_admin_recieve)
            newAdminThread.start()
            serverThread.set_true_admin_connection()

        elif login[0] == "user" and login[1] == "123":
            print(f"Connection from {address} has been established!")
            clientsocket.send("connectionsuccess\n".encode())
            #check if there is an existing userthread
            print("hello-1")
            if serverThread.get_user_connection():
                newUserThread.add_connection(clientsocket, address, 5)
                serverThread.set_true_user_connection()
            #if userthread is closed create a new one
            else:
                print("hello0")
                newUserThread = UserThread.UserThread(clientsocket, address, 5, queue_user, queue_update_user)
                newUserThread.start()
                print("hello")
                serverThread.set_true_user_connection()
                print("hello2")
            

        else:  
            print("Connection failed")
            clientsocket.send("connectionfailed".encode())
            clientsocket.close()
        print("hello2")
        i+=1

    serverThread.join()

