import SensorClass

class SensorGroupClass:
    def __init__(self, name, location_type, mac_address, connection_status, sensors):
        self.name = name
        self.location_type = location_type
        self.mac_address = mac_address
        self.connection_status = connection_status
        self.sensors = [] # list of SensorClass objects
        for sensor in sensors:
            self.sensors.append(SensorClass.SensorClass(sensor["name"],sensor["sensor_type"],1,0))
         
    
    def get_name(self):
        return self.name
    def get_location_type(self):
        return self.location_type
    def get_mac_address(self):
        return self.mac_address
    def get_connection_status(self):
        return self.connection_status
    def get_sensors(self):
        return self.sensors
    
    def set_name(self, name):
        self.name = name
    def set_location_type(self, location_type):
        self.location_type = location_type
    def set_mac_address(self, mac_address):
        self.mac_address = mac_address
    def set_connection_status(self, connection_status):
        self.connection_status = connection_status
    def set_sensors(self, sensors):
        self.sensors = sensors

    def __str__(self):
        return self.name + " " + self.location_type + " " + self.mac_address + " " + self.connection_status + " " + self.sensors