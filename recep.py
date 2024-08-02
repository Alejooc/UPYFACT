import time
import paramiko
import json
import re
class Recepcion:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh = None

    def conectar(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

    def desconectar(self):
        if self.ssh:
            self.ssh.close()
    def limpiar_salida(self,salida):
        salida_limpia = re.sub(r'\x1b[^m]*m', '', salida)  # Eliminar caracteres de escape
        salida_limpia = re.sub(r'\r', '', salida_limpia)  # Eliminar retornos de carro
        lineas = [linea.strip() for linea in salida_limpia.split('\n') if linea.strip()]  # Eliminar líneas en blanco
        return '\n'.join(lineas)

    def interactuar_con_consola(self):
        salida_global = ""
        shell = self.ssh.invoke_shell()
        while True:
            try:
                if shell.recv_ready():
                    salida = shell.recv(4096).decode(errors='ignore')
                    salida_global += salida
                    print(salida, end='')
                    if "Codigo de Usuario" in salida:
                        shell.send("PRUEBA\n")
                        time.sleep(1)
                    if "Codigo de Seguridad" in salida:
                        shell.send("PRUEBA\n")
                        time.sleep(1)
                    if "Otros" in salida:
                        shell.send("OA")
                        time.sleep(1)
                        shell.send("ITV")
                        time.sleep(4)
                        shell.send("202405031\n\nS\n1")
                    if "FIN REPORTE" in salida:
                        time.sleep(2)
                        break
                if shell.exit_status_ready():
                    break
                time.sleep(1)
            except Exception as e:
                print("Error:", e)
                break

        self.desconectar()
        salida_global_limpia = self.limpiar_salida(salida_global)
        return json.dumps({"output": salida_global_limpia}, indent=4)
    
    def enviar_texto(self, shell, texto):
        shell.send(texto)
        time.sleep(1)
