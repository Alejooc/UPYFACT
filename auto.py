import json
import time
import paramiko
with open('fcelectronica.json', 'r') as archivo:
    contenido = archivo.read()
    datos = json.loads(contenido)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='192.168.0.150', port="1634", username='alejandro', password='alejandro123*')

    shell = ssh.invoke_shell()
    while True:
        try:
            if shell.recv_ready():
                salida = shell.recv(99999).decode(errors='ignore')
                print(salida, end='')
                for moduleauto in datos['code']:
                    if moduleauto['type'] == "conditional":
                        if moduleauto['find'] in salida:
                            if moduleauto['time'] > 0:
                                time.sleep(moduleauto['time'])
                            if moduleauto['sendomando'] =="F6":
                                shell.send('\x1B[17~')
                            else:
                                shell.send(moduleauto['input'])
                            if moduleauto['break']:
                               break
                            
                    elif moduleauto['type'] == "send":
                        shell.send(moduleauto['input'])
                
            if shell.exit_status_ready():
                break
            time.sleep(1)
        except Exception as e:
            print("Error:", e)
            break

       # ssh.close()