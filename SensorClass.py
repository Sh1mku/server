import SensorValueClass

class SensorClass:
    def __init__(self, name, sensor_type, connection_status, sensor_values):
        self.name = name
        self.sensor_type = sensor_type
        self.connection_status = connection_status
        self.sensor_values= sensor_values # list of SensorValueClass objects
    
    def get_name(self):
        return self.name
    def get_sensor_type(self):
        return self.sensor_type
    def get_connection_status(self):
        return self.connection_status
    def get_sensor_values(self):
        return self.sensor_values
    
    def set_name(self, name):
        self.name = name
    def set_sensor_type(self, sensor_type):
        self.sensor_type = sensor_type
    def set_connection_status(self, connection_status):
        self.connection_status = connection_status
    def set_sensor_values(self, sensor_values):
        self.sensor_values = sensor_values

    def __str__(self):
        return self.name + " " + self.sensor_type + " " + self.connection_status + " " + self.sensor_values