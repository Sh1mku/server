class SensorValueClass:
    def __init__(self, value, timestamp):
        self.value = value
        self.timestamp = timestamp
    
    def get_value(self):
        return self.value
    def get_timestamp(self):
        return self.timestamp

    def set_value(self, value):
        self.value = value