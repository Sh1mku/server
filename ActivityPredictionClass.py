class  ActivityPrediction:
    def __init__(self,timestamp,activity_type,confidence_level):
        self.timestamp = timestamp
        self.activity_type = activity_type
        self.confidence_level = confidence_level
    
    def get_timestamp(self):
        return self.timestamp
    def get_activity_type(self):
        return self.activity_type
    def get_confidence_level(self):
        return self.confidence_level
    
    def set_timestamp(self,timestamp):
        self.timestamp = timestamp
    def set_activity_type(self,activity_type):
        self.activity_type = activity_type
    def set_confidence_level(self,confidence_level):
        self.confidence_level = confidence_level
    
    def __str__(self):
        return self.timestamp + " " + self.activity_type + " " + self.confidence_level