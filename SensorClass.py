import time
import SensorValueClass

class SensorClass:
    def __init__(self, name, sensor_type, connection_status, sensor_value):
        self.name = name
        self.sensor_type = sensor_type
        self.connection_status = connection_status
        self.sensor_value=SensorValueClass.SensorValueClass(sensor_value,time.localtime())
    
    def get_name(self):
        return self.name
    def get_sensor_type(self):
        return self.sensor_type
    def get_connection_status(self):
        return self.connection_status
    def get_sensor_value(self):
        return self.sensor_value
    
    def set_name(self, name):
        self.name = name
    def set_sensor_type(self, sensor_type):
        self.sensor_type = sensor_type
    def set_connection_status(self, connection_status):
        self.connection_status = connection_status
    def set_sensor_value(self, sensor_value):
        self.sensor_value = sensor_value

    def __str__(self):
        return self.name + " " + self.sensor_type + " " + self.connection_status + " " + self.sensor_value