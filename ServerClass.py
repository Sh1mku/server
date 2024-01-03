from queue import Queue
from time import sleep
import PatientInfoClass
import SensorGroupClass
import SensorClass
import ClientConnectionClass
import ExternalAlertConfigClass
import ActivityPredictionClass
import model
import numpy as np
import pandas as pd
# import tensorflow as tf
# from tensorflow import keras
import sklearn 
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import classification_report
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
# from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.optimizers import Adam



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
        self.admin_password = None
        self.user_password = None


    def run(self):
        
        # self.initialize()
        get5minBeforeThread = Thread(target=self.get5minBefore)
        get5minBeforeThread.start()

        #TODO: must be changed to read from the sensors

        start_column = 1
        end_column = 250

        # Generate column names as a range of numbers 
        column_names = list(range(start_column, end_column + 1))
        df_subset = pd.read_csv('test_subset.csv')

        while True:
    
            # send each row to the anomaly detector but as a pandas dataframe
            for index, row in df_subset.iterrows():
            
                data = pd.DataFrame(row[1:].values.reshape(1, -1), columns=column_names)
                anomaly, locomotion_activity, confidence_locomotion = self.get_anomaly(data) #TODO: (anomaly,result1,result2) must return both results from models and anomaly/noAnomaly(will be implemented next week) 
                print(anomaly, locomotion_activity, confidence_locomotion)
                sleep(1) #TODO: must be changed to 1 second
                self.last_prediction = ", ".join([str(anomaly), locomotion_activity, str(confidence_locomotion)])
                self.last5minQueue.put(self.last_prediction)
            
                if anomaly:
                    time = datetime.now()
                    self.send_external_alert(anomaly,time)

                    if self.connection_user:
                        anomaly = anomaly + (time,)
                        self.queue.put(anomaly)
            
     


    def initialize(self):
        try:
            file = open("config.json", "r")
        except IOError:
            print("File couldn't be found")
            exit(1)
        data = json.load(file)
        self.admin_password = data["passwords"]["admin"]
        self.user_password = data["passwords"]["user"]

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

    def get_sensor_values(self):
        pass
       
    #TODO: must return both results and prediction(will be implemented next week)
    def get_anomaly(self,data):
        anomaly, locomotion_activity, confidence_locomotion, _, _ = model.anomaly_detector(data)
        return anomaly, locomotion_activity, confidence_locomotion
    
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
                data = data.split("-")
                if data[0] == "network":
                    pass
                elif data[0] == "lastPred":
                    self.send_to_admin.put(self.last10min)
                elif data[0] == "curAct":
                    self.send_to_admin.put(self.last_prediction)
                elif data[0] == "chgPass":
                    self.change_admin_password(data[1])

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
    
    def get_external_alert_list(self):
        return self.external_alert_list 
    
    def get_patient_info(self):
        return self.patient_info
    
    def get_user_password(self):
        return self.user_password
    
    def get_admin_password(self):
        return self.admin_password
    
    def change_admin_password(self, new_password):

        self.admin_password = new_password

    def change_user_password(self, new_password):
        self.user_password = new_password


queue_user = Queue()
queue_admin_send = Queue()
queue_admin_recieve = Queue()
serverThread = ServerClass(queue_user,queue_admin_recieve, queue_admin_send )
serverThread.start()