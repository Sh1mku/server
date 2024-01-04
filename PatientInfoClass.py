class PatientInfo:
    def __init__(self,name,surname,title,telephone,home_address):
        self.name = name
        self.surname = surname
        self.title = title
        self.telephone = telephone
        self.home_address = home_address

    def get_name(self):
        return self.name
    def get_surname(self):
        return self.surname
    def get_title(self):
        return self.title
    def get_telephone(self):
        return self.telephone
    def get_home_address(self):
        return self.home_address
    
    def set_name(self,name):
        self.name = name
    def set_surname(self,surname):
        self.surname = surname
    def set_title(self,title):
        self.title = title
    def set_telephone(self,telephone):
        self.telephone = telephone
    def set_home_address(self,home_address):
        self.home_address = home_address
        
    def __str__(self):
        return self.title + " " + self.name + " " + self.surname + " " + self.telephone + " " + self.home_address