from queue import Queue
import PatientInfoClass
import SensorGroupClass
import SensorClass
import ClientConnectionClass
import ExternalAlertConfigClass
import ActivityPredictionClass

from threading import Thread
from datetime import datetime
import json

class ServerClass(Thread):
    def __init__(self,userqueue,adminreceivequeue,adminsendqueue):
        Thread.__init__(self)
        self.sensor_groups = [] # list of SensorGroupClass objects
        self.last_prediction = None
        self.external_alert_list = [] # list of ExternalAlertConfigClass objects
        self.patient_info = None
        self.connection_user= False
        self.connection_admin = False
        self.queue = userqueue
        self.send_to_admin = adminreceivequeue
        self.recieve_from_admin = adminsendqueue
        self.last5minQueue = Queue()
        self.last10min = []


    def run(self):
        
        self.initialize()
        get5minBeforeThread = Thread(target=self.get5minBefore)
        get5minBeforeThread.start()

        #TODO: must be changed to read from the sensors
        try:
            file = open("S1-ADL1_sensors_data.txt", "r")
        except IOError:
            print("File couldn't be found")
            exit(1)

        while True:
            data = self.get_sensor_values(file)
            

            anomaly = self.get_anomaly(data) #TODO: (anomaly,result1,result2) must return both results from models and anomaly/noAnomaly(will be implemented next week) 
            self.last_prediction = anomaly
            self.last5minQueue.put(anomaly)
           
            if anomaly[0] == True :
                time = datetime.now()
                self.send_external_alert(anomaly,time)

                if self.connection_user:
                    anomaly = anomaly + (time,)
                    self.queue.put(anomaly)
        file.close()


    def initialize(self):
        try:
            file = open("config.json", "r")
        except IOError:
            print("File couldn't be found")
            exit(1)
        data = json.load(file)
        # self.admin_password = data["passwords"]["admin"]
        # self.user_password = data["passwords"]["user"]

        for sensor_group in data["sensor_groups"]:
            self.sensor_groups.append(SensorGroupClass.SensorGroup(sensor_group["name"],sensor_group["connection_status"],sensor_group["sensors"]))
        
        for external_alert in data["external_alert_configs"]:
            
            self.external_alert_list.append(ExternalAlertConfigClass.ExternalAlertConfig(external_alert["full_name"],external_alert["gsm_number"],external_alert["email_address"]))

        self.patient_info = PatientInfoClass.PatientInfo(data["patient_info"]["name"],data["patient_info"]["surname"],data["patient_info"]["title"],data["patient_info"]["telephone"],data["patient_info"]["home_address"])
        
        file.close()

    def set_true_user_connection(self):
        self.connection_user = True 

    def set_false_user_connection(self):
        self.connection_user = False          

    def set_true_admin_connection(self):
        self.connection_admin = True

    def set_false_admin_connection(self):
        self.connection_admin = False 

    def get_sensor_values(self,file):
        return file.readline()

    #TODO: must return both results and prediction(will be implemented next week)
    def get_anomaly(self,data):
        pass
    
    #TODO: must send the anomaly to the external alert system(to be decided)
    def send_external_alert(self,anomaly,time):
        pass
    
    def get5minBefore(self):
        last5min = []
        sizeFirstHalf = 0
        sizeSecondHalf = 900
        upload = 0
        last10array = []
        while True:
            if self.last5minQueue.qsize():
                lastPrediction = self.last5minQueue.get()
                lastPrediction.split(",")

                if lastPrediction[0] == "True":
                    sizeSecondHalf = 0
                    upload = 1

                if sizeSecondHalf < 900:
                    last10array.clear()
                    last10array = last10array + last5min
                    last10array.append(lastPrediction)
                    sizeSecondHalf += 1


                if sizeFirstHalf == 900:
                    last5min.pop(0)
                    last5min.append(lastPrediction)
                else:
                    last5min.append(lastPrediction)
                    sizeFirstHalf += 1

                if upload == 1 and sizeSecondHalf == 900:
                    self.last10min = last10array
                    upload = 0


    def admin_handler(self):
        while True:
            if not self.recieve_from_admin.empty():
                data = self.recieve_from_admin.get()
                if data == "network":
                    pass
                elif data == "lastPred":
                    self.send_to_admin.put(self.last10min)
                elif data == "curAct":
                    self.send_to_admin.put(self.last_prediction)

    def get_group_names(self):
        return [sensor_group.get_name() for sensor_group in self.sensor_groups]
    
    def get_group_status(self,group_name):

        for sensor_group in self.sensor_groups:
            if sensor_group.get_name() == group_name:
                return sensor_group.get_connection_status()
        print("Group not found")
        return None
    
    def get_group_values(self,group_name,timestamp):  #TODO: must return a dict of sensor values & names
        pass


    def get_admin_password(self):
        return self.admin_password
    
    def get_user_password(self):
        return self.user_password
    
    def get_sensor_groups(self):
        return self.sensor_groups
    
    def get_last_prediction(self):
        return self.last_prediction
    
    def get_client_connections(self):
        return self.client_connections

    def set_password(self, password):
        self.password = password
    def set_sensor_groups(self, sensor_groups):
        self.sensor_groups = sensor_groups
    def set_last_prediction(self, last_prediction):
        self.last_prediction = last_prediction
    def set_client_connections(self, client_connections):
        self.client_connections = client_connections

    def __str__(self):
        return self.password + " " + self.sensor_groups + " " + self.last_prediction + " " + self.client_connections
    