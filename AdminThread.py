import socket
import threading
from time import sleep  
import json
#optional messages: ["nothing","disconnect", "close", "network", "lastPred", "curAct", "chgPass"]

class AdminThread(threading.Thread):
    def __init__(self,client_socket,client_address,timeout, queueSend, queueRecieve):
        threading.Thread.__init__(self)
        self.client_address = client_address
        self.client_socket = client_socket
        self.timeout = timeout
        self.adminMessage = "nothing"
        self.send_to_server = queueSend
        self.recieve_from_server = queueRecieve
    
    def run(self):
        receriveThread=threading.Thread(target=self.adminRecieve)
        sendThread=threading.Thread(target=self.adminSend)
        receriveThread.start()
        sendThread.start()
        if self.adminMessage == "disconnect":
            self.client_socket.close()
            receriveThread.join()
            sendThread.join()
            return
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
        json.dump(data, file, indent=4)
        file.close()

        self.send_to_server.put("chgPass-" + new_password)


    def adminRecieve(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode() #data = disconnect, close, network, lastPred, curAct, chgPass
                if data == "close":
                    self.adminMessage="nothing"
                else:
                    self.adminMessage = data
                    print(f"Data receivedaa {self.adminMessage}")
            except ConnectionResetError:
                print("Connection closed")
                self.client_socket.close()
                break
            sleep(1)

    def adminSend(self):
        print("Sending data")
        self.client_socket.send("connectionsuccess\n".encode())
        while True:
            if self.adminMessage != "nothing":
                msg = self.adminMessage.split("-")
                if msg[0] == "disconnect":
                    self.client_socket.close()
                    self.send_to_server.put("disconnect")
                    self.killThread()
                elif msg[0] == "network":
                    sensor_values = self.get_sensor_status()
                    print(f"Sending Network as {sensor_values}")
                    self.client_socket.send(sensor_values.encode())
                elif msg[0] == "lastPred":
                    prediction = self.get_last_prediction()
                    print(f"Sending lastPred as {prediction}")
                    self.client_socket.send(prediction.encode())
                    self.adminMessage = "nothing"
                elif msg[0] == "curAct":
                    action = self.get_current_action()
                    print("current action: ", action)
                    action=action+"\n"
                    self.client_socket.send(action.encode())
                elif msg[0] == "chgPass":
                    self.change_admin_password(msg[1])
                    self.client_socket.send("admin password changed".encode())
                    self.adminMessage = "nothing"
            sleep(1)

    def killThread(self):
        self.killThread = True