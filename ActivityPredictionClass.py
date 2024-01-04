class  ActivityPrediction:
    def __init__(self,anomaly,locomotion,locomotion_confidence_level,scalar_locomotion,scalar_locomotion_confidence_level,timestamp):
        self.anomaly = anomaly
        self.locomotion = locomotion
        self.locomotion_confidence_level = locomotion_confidence_level
        self.scalar_locomotion = scalar_locomotion
        self.scalar_locomotion_confidence_level = scalar_locomotion_confidence_level
        self.timestamp = timestamp

    
    def get_anomaly(self):
        return self.anomaly
    def get_locomotion(self):
        return self.locomotion
    def get_locomotion_confidence_level(self):
        return self.locomotion_confidence_level
    def get_scalar_locomotion(self):
        return self.scalar_locomotion
    def get_scalar_locomotion_confidence_level(self):
        return self.scalar_locomotion_confidence_level
    def get_timestamp(self):
        return self.timestamp
    
    def set_anomaly(self,anomaly):
        self.anomaly = anomaly

    def set_locomotion(self,locomotion):
        self.locomotion = locomotion
    def set_locomotion_confidence_level(self,locomotion_confidence_level):
        self.locomotion_confidence_level = locomotion_confidence_level
    def set_scalar_locomotion(self,scalar_locomotion):
        self.scalar_locomotion = scalar_locomotion
    def set_scalar_locomotion_confidence_level(self,scalar_locomotion_confidence_level):
        self.scalar_locomotion_confidence_level = scalar_locomotion_confidence_level
    def set_timestamp(self,timestamp):
        self.timestamp = timestamp

    def __str__(self):
        return "Anomaly: " + str(self.anomaly) + " Locomotion: " + str(self.locomotion) + " Locomotion Confidence Level: " + str(self.locomotion_confidence_level) + " Scalar Locomotion: " + str(self.scalar_locomotion) + " Scalar Locomotion Confidence Level: " + str(self.scalar_locomotion_confidence_level) + " Timestamp: " + str(self.timestamp)