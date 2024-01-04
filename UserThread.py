import socket
from threading import *
from time import sleep
from ClientConnectionClass import *
import json


class UserThread(Thread):
    def __init__(self, client_socket, client_address, timeout, queue, update_server_queue):
        Thread.__init__(self)
        self.connection_list = [ClientConnection(client_socket, client_address, timeout)]
        self.timeout = timeout
        self.queue = queue
        self.userThreads = []
        self.update_server_queue = update_server_queue

    def run(self):
        print("User thread started")
        # start the first thread

        self.userThreads.append(
            Thread(target=self.userRecieve, args=(self.connection_list[0].client_socket, self.update_server_queue)))
        self.userThreads[0].start()
        # if queue is not empty send the message to all clients

        while True:
            
            if not self.queue.empty():

                msg = self.queue.get()
                i = 0

                for connection in self.connection_list:
                    print("sending to: ", i)

                    try:
                        connection.client_socket.send(msg.encode())
                    except ConnectionResetError:
                        # if ConnectionResetError occurs, close the connection
                        print("Connection closed")
                        self.connection_list.pop(i)
                        self.userThreads.pop(i)
                        self.connection_list[i].client_socket.close()
                    i += 1
            if self.get_size_connection_list() == 0:
                self.update_server_queue.put("disconnect")
                break
            # if get_size_socket_list() == 0:
            #     self.client_socket.close()
            #     break

    def add_connection(self, client_socket, client_address, timeout):
        self.connection_list.append(ClientConnection(client_socket, client_address, timeout))
        self.userThreads.append(Thread(target=self.userRecieve, args=(client_socket, self.update_server_queue)))
        self.userThreads[-1].start()

    def get_size_connection_list(self):
        return len(self.connection_list)

    def change_password(self, new_password, update_server_queue):
        try:
            file = open("config.json", "r")
        except IOError:
            print("File couldn't be found")

        data = json.load(file)
        data["passwords"]["user"] = new_password
        file.close()

        try:
            file = open("config.json", "w")
        except IOError:
            print("File couldn't be found")

        json.dump(data, file, indent=4)

        file.close()

        update_server_queue.put("chgPass-" + new_password)

    def change_patient_info(self, new_info, update_server_queue):
        try:
            file = open("config.json", "r")
        except IOError:
            print("File couldn't be found")

        data = json.load(file)
        data["patient_info"]["name"] = new_info[1]
        data["patient_info"]["surname"] = new_info[2]
        data["patient_info"]["title"] = new_info[3]
        data["patient_info"]["telephone"] = new_info[4]
        data["patient_info"]["home_address"] = new_info[5]
        file.close()

        try:
            file = open("config.json", "w")
        except IOError:
            print("File couldn't be found")

        json.dump(data, file, indent=4)

        file.close()

        update_server_queue.put("-".join(data))

    def userRecieve(self, client_socket, update_server_queue):
        while True:
            try:

                data = client_socket.recv(1024).decode()
                data = data.split("-")
                if data[0] == "disconnect":
                    i=0
                    for connection in self.connection_list:
                        if connection.client_socket == client_socket:
                            self.connection_list.pop(i)
                            self.userThreads.pop(i)
                            break
                        i+=1
                    client_socket.close()
                    break
                elif data[0] == "chgPass":
                    # call function to change password
                    self.change_password(data[1], update_server_queue)
                    client_socket.send("success".encode())
                elif data[0] == "chgPat":
                    # call function to change patient info
                    self.change_patient_info(data, update_server_queue)
                    client_socket.send("success".encode())

            except ConnectionResetError:
                print("Connection closed")
                client_socket.close()
                break
            sleep(2)