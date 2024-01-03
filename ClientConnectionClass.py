class ClientConnection:
    def __init__(self,client_socket,client_address,timeout):
        self.client_socket = client_socket
        self.client_address = client_address
        self.timeout = timeout
    
    
    def get_client_socket(self):
        return self.client_socket
    def get_client_address(self):
        return self.client_address
    def get_timeout(self):
        return self.timeout
    
    def set_client_socket(self,client_socket):
        self.client_socket = client_socket
    def set_client_address(self,client_address):
        self.client_address = client_address
    def set_timeout(self,timeout):
        self.timeout = timeout
    
    def __str__(self):
        return self.client_socket + " " + self.client_address + " " + self.timeout
