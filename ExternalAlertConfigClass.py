class ExternalAlertConfig:
    def __init__(self,full_name,gsm_number,email_address):
        self.full_name = full_name
        self.gsm_number = gsm_number
        self.email_address = email_address
    def get_full_name(self):
        return self.full_name
    def get_gsm_number(self):
        return self.gsm_number
    def get_email_address(self):
        return self.email_address
    def set_full_name(self,full_name):
        self.full_name = full_name
    def set_gsm_number(self,gsm_number):
        self.gsm_number = gsm_number
    def set_email_address(self,email_address):
        self.email_address = email_address
    def __str__(self):
        return self.full_name + " " + self.gsm_number + " " + self.email_address
