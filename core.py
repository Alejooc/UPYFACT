from dotenv import load_dotenv
import os

class Core:
    def __init__(self):
        load_dotenv()

    def get_debug(self):
        return os.getenv("DEBUG")
    
    def get_endpointClient(self):
        return os.getenv("ENDPOINT_CLIENT")
    
    def get_companyName(self):
        return os.getenv("COMPANY")
    
    def get_logs(self):
        return os.getenv("LOGS")
    
    def get_host_ssh(self):
        return os.getenv("SSH_HOST")
    
    def get_port_ssh(self):
        return os.getenv("SSH_PORT")
    
    def get_user_ssh(self):
        return os.getenv("SSH_USER")
    
    def get_pass_ssh(self):
        return os.getenv("SSH_PASSWORD")
