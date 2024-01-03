import socket
from threading import *
from ClientConnectionClass import *
class UserThread(Thread):
    def __init__(self,client_socket,client_address,timeout,queue):
        Thread.__init__(self)
        self.connection_list = [ClientConnection(client_socket,client_address,timeout)]
        self.queue = queue
    
    def run(self):
        #if queue is not empty send the message to all clients

        while True:
            if not self.queue.empty():
                
                msg = self.queue.get()
                i=0
                
                for connection in self.connection_list:
                    print("sending to: ", i)
                        
                    try:
                        connection.client_socket.send(msg.encode())
                    except ConnectionResetError:
                        #if ConnectionResetError occurs, close the connection
                        print("Connection closed")
                        self.connection_list.pop(i)
                        self.connection_list[i].client_socket.close()
                    i+=1
    
            # if get_size_socket_list() == 0:
            #     self.client_socket.close()
            #     break


    def add_connection(self,client_socket,client_address,timeout):
        self.connection_list.append(ClientConnection(client_socket,client_address,timeout))
    
    def get_size_connection_list(self):
        return len(self.connection_list)
