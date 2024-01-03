import socket
import threading
from time import sleep  
import json
#optional messages: ["nothing","disconnect", "close", "network", "lastPred", "curAct", "chgPass"]

class AdminThread(threading.Thread):
    def __init__(self,client_socket,client_address,timeout, queueSend, queueRecieve):
        threading.Thread.__init__(self)
        self.addressList = [client_address]
        self.socketList = [client_socket]
        self.timeout = timeout
        self.adminMessage = "nothing"
        self.send_to_server = queueSend
        self.recieve_from_server = queueRecieve
    
    def run(self):
        receriveThread=threading.Thread(target=self.adminRecieve)
        sendThread=threading.Thread(target=self.adminSend)
        receriveThread.start()
        sendThread.start()
        sleep(5)

    """ TODO: this function should recieve the value of the sensorgroup 
        (called from main server) in the desired format and send it 
        to the client
    """
    def get_sensor_status(self):
        self.send_to_server.put("network")
        servermsg = self.recieve_from_server.get()
        return servermsg
    

    def get_last_prediction(self):
        self.send_to_server.put("lastPred")
        servermsg = self.recieve_from_server.get()
        return servermsg
    

    def get_current_action(self):
        self.send_to_server.put("curAct")
        servermsg = self.recieve_from_server.get()
        return servermsg

    
    def change_admin_password(self, new_password):
        try:
            file = open("config.json", "r")
        except IOError:
            print("File couldn't be found")

        data = json.load(file)
        data["passwords"]["admin"] = new_password
        file.close()

        try:
            file = open("config.json", "w")
        except IOError:
            print("File couldn't be found")
        json.dump(data, file)
        file.close()

        send_to_server.put("chgPass-"+new_password)



    def adminRecieve(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode() #data = disconnect, close, network, lastPred, curAct, chgPass
                if data == "close":
                    self.adminMessage="nothing"
                else:
                    self.adminMessage = data
            except ConnectionResetError:
                print("Connection closed")
                self.client_socket.close()
                break
            sleep(2)

    def adminSend(self):
        while True:
            if self.adminMessage != "nothing":
                msg = self.adminMessage.split("-")
                if msg[0] == "network":
                    sensor_values = self.get_sensor_status()
                    self.client_socket.send(sensor_values.encode())
                elif msg[0] == "lastPred":
                    prediction = self.get_last_prediction()
                    self.client_socket.send(prediction.encode())
                    self.adminMessage = "nothing"
                elif msg[0] == "curAct":
                    action = self.get_current_action()
                    self.client_socket.send(action.encode())
                elif msg[0] == "chgPass":
                    self.change_admin_password(msg[1])
                    self.client_socket.send("password changed".encode())
                    self.adminMessage = "nothing"
            sleep(1)