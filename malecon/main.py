import json
import time
import paramiko
import requests
import logging

class Listados:
    def __init__(self, ssh_details):
        self.ssh_details = ssh_details
        self.datos = None
        self.ssh = None
        self.shell = None
        self.json_data=[]
        
    def create_ssh_client(self):
        """Crea y devuelve un cliente SSH."""
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(**self.ssh_details)
        except Exception as e:
            print(f"Error creating SSH client: {e}")
            self.ssh = None

    def send_command(self, command, wait_time=0.1):
        """Envía un comando al shell y espera un tiempo especificado."""
        self.shell.send(command)
        time.sleep(wait_time)
        if self.shell.recv_ready():
            response = self.shell.recv(9999).decode(errors='ignore')
            #print(response, end='')
            return response
        return ''
    
    def run(self):
        self.create_ssh_client()
        if self.ssh is None:
            return

        self.shell = self.ssh.invoke_shell(term='linux')
        try:
            self.send_command('cd /u/uno/uno85c/lab85\n')
            self.send_command('sh UNO\n')
            self.send_command("MASTER\n")
            self.send_command("SI\n")
            self.send_command("CVCPL\n")
            try:
                while True:
                        try:
                            if self.shell.recv_ready():
                                salida = self.shell.recv(99999).decode(errors='ignore')
                                #print(salida, end='')
                                if "LISTAS DE PRECIOS - LISTADO" in salida:
                                   # self.send_command("\u000d")
                                    time.sleep(1)
                                    self.send_command("\x1b[B \x1b[B \x1b[B \x1b[B \x1b[B \x1b[B")
                                    time.sleep(1)
                                    self.send_command("\u000d")
                                    self.send_command("\u000d")
                                    self.send_command("2\u000d")
                                    self.send_command("\u000d\u000d0 1\u000d\u000d")
                                    self.send_command("X")
                                    self.send_command("\u000d")
                                    self.send_command("\u000d")
                                    self.send_command("S")
                                    self.send_command("\u000d")
                                    
                                if "FIN DEL PROCESO" in salida:
                                    break
                            if self.shell.exit_status_ready():
                                break
                            time.sleep(1)
                        except Exception as e:
                            print("Error:", e)
                            break   
            except Exception as e:
                print("Error en el bucle principal:", e)
        finally:
            self.ssh.close()            

if __name__ == "__main__":
    ssh_details = {
        "hostname": '170.238.239.119',
        "port": 1634,
        "username": 'root',
        "password": 'malecon2024*./-'
    }
    run = Listados(ssh_details)
    run.run()
