import json
import time
import paramiko

def load_json(file_path):
    """Carga datos desde un archivo JSON."""
    try:
        with open(file_path, 'r') as archivo:
            return json.load(archivo)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None

def create_ssh_client(hostname, port, username, password):
    """Crea y devuelve un cliente SSH."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
    except Exception as e:
        print(f"Error creating SSH client: {e}")
        return None
    return ssh

def send_command(shell, command, wait_time=0.1):
    """Envía un comando al shell y espera un tiempo especificado."""
    shell.send(command)
    time.sleep(wait_time)
    if shell.recv_ready():
        response = shell.recv(9999).decode(errors='ignore')
        print(response, end='')
        return response
    return ''

def main():
    ssh_details = {
        "hostname": '192.168.0.150',
        "port": 1634,
        "username": 'root',
        "password": 'sistemasaris2022-/*'
    }
    json_file_path = 'json.json'
    
    datos = load_json(json_file_path)
    if datos is None:
        return
    
    if 'items' in datos and 'VLRNET' in datos['items'][0]:
        for item in datos['items']:
            item['VLRNET'] = str(int(item['VLRNET']))

    ssh = create_ssh_client(**ssh_details)
    if ssh is None:
        return

    shell = ssh.invoke_shell(term='linux')

    try:
        # Enviar comandos iniciales
        send_command(shell, 'cd /u/uno/uno85c/lab85\n')
        send_command(shell, 'sh UNO\n')
        send_command(shell, "KAREN\n")
        send_command(shell, "5441\n")

        # Navegar por el menú
        send_command(shell, "OALRF\n")
        send_command(shell, "01\n")  # Centro de operación 01
        send_command(shell, "\u000d")  # ENTER
        send_command(shell, "CF\u000d")  # Cliente CF (Consumidor Final)
        send_command(shell, "062\u000d")  # Vendedor

        while True:
            try:
                if shell.recv_ready():
                    salida = shell.recv(99999).decode(errors='ignore')
                    print(salida, end='')

                    if "FACTURACION DE ITEMS - INGRESO" in salida:
                        for items in datos['items']:
                            # Enviar la secuencia F6
                            send_command(shell, "\x1B[17~")
                            send_command(shell, "1\n")
                            # Enviar los detalles del ítem
                            texto = f"{items['ITEMS']}\u000d{items['CANT_1']}\u000d{items['VLRNET']}\u000d"
                            send_command(shell, texto)
                            send_command(shell, "\u000d")
                        time.sleep(0.5)
                        send_command(shell, '\x1B')
                        send_command(shell, '3')
                        time.sleep(0.5)
                    if "[ INFORMACION DEL RECAUDO ]" in salida:
                        texto = f"{datos['recaudo']['MEDPAG']}"
                        send_command(shell, texto)
                        send_command(shell, "\u000d")
                        break
                        if datos['recaudo']['MEDPAG'] == '022':
                            break
                        else:
                            totalFactura = f"{datos['recaudo']['VALOR']}"
                            send_command(shell, totalFactura)
                            send_command(shell, "\u000d")
                            send_command(shell, "1")
                            send_command(shell, "\u000d \u000d \u000d")

                            break
                    
                if shell.exit_status_ready():
                    break
                time.sleep(1)
            except Exception as e:
                print("Error:", e)
                break
    finally:
        ssh.close()
        

if __name__ == "__main__":
    main()
