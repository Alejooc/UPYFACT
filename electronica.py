import json
import time
import paramiko
import requests
import logging
from core import Core
from tqdm import tqdm
class Electronica:
    def __init__(self, ssh_details, json_file_path):
        self.ssh_details = ssh_details
        self.json_file_path = json_file_path
        self.datos = None
        self.ssh = None
        self.shell = None
        self.json_data=[]
        self.env_loader = Core()
        
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
    
    def gen_json_rest(self,order,factura,caja,error):
        nuevo_dato = {
            "order": order,
            "factura": factura,
            "caja": caja,
            "error":error
        }
        self.json_data.append(nuevo_dato)


    def send_json_to_endpoint(self):
        """Envía los datos JSON a un endpoint externo."""
        try:
            response = requests.post(self.env_loader.get_endpointClient(), json=self.json_data)
            response.raise_for_status()
            return {"type":1,"msg":"Facturas generadas en cg1.","facturas":self.json_data,"api":response.text}
        except Exception as e:
            return {"error":e,"type":2}


    def run(self):
        msgfiaml=''
        # Configuración básica de logging
        if self.env_loader.get_logs():
            logging.basicConfig(filename='logs.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')
        
        if self.json_file_path is None:
            return
    
       
        factura = int(self.json_file_path[0]['items'][0]['NRO_FC'])
        caja= int(self.json_file_path[0]['items'][0]['NTD_CAJA'])
        centroOperacion = f"{self.json_file_path[0]['recaudo']['CO']}\n"
        numCaja= f"{self.json_file_path[0]['recaudo']['CAJA']}\n"
        
        self.create_ssh_client()
        if self.ssh is None:
            return

        self.shell = self.ssh.invoke_shell(term='linux')
        
        # Enviar comandos iniciales
        try:
            self.send_command('cd /u/uno/uno85c/cajas\n')
            self.send_command('sh UNO\n')
            self.send_command("KAREN\n")
            self.send_command("5441\n")
            time.sleep(0.5)
            # Navegar por el menú
            self.send_command("OALRF\n")
            self.send_command("\x1B") #ESC reiniciamos par aingresar el CO 
            self.send_command(centroOperacion)  # / CO 
            self.send_command(numCaja)  # / CAJA 
            self.send_command( "\u000d")  # ENTER
        
            try:
                for jsonFacturas in tqdm(self.json_file_path, desc="Procesando facturas"):
                    if 'items' in jsonFacturas and 'VLRNET' in jsonFacturas['items']:
                        for item in jsonFacturas['items']:
                            item['VLRNET'] = str(int(item['VLRNET']))

                    try:
                        time.sleep(0.5)
                        self.send_command("CF\u000d")  # Cliente CF (Consumidor Final)
                        time.sleep(0.5)
                        self.send_command("062\u000d")  # Vendedor
                        
                    
                        while True:
                            try:
                                if self.shell.recv_ready():
                                    salida = self.shell.recv(99999).decode(errors='ignore')
                                   # print(salida, end='')
                                    #logging.debug(salida)  # Esto se guardará en logs.txt
                                    if "FACTURACION DE ITEMS - INGRESO" in salida:
                                        for items in jsonFacturas['items']: 
                                            # Enviar la secuencia F6
                                            self.send_command("\x1B[17~")
                                            self.send_command("1")
                            
                                            
                                            # Enviar los detalles del ítem
                                            precio_uni = int(items['PRECIO_UNI'])
                                            
                                            if precio_uni > 0 or int(items['OBSEQUIO']) == 1 and int(items['OBSEQUIO'])== 0:

                                                VLRIVA_sin_ceros = items['VLRIVA'].lstrip('0')

                                                if int(items['CANT_1']) > 1: # validamos si es mayor a UNO dividimos el iva por la cantidad de items
                                                    
                                                    valor_iva = int(VLRIVA_sin_ceros)/int(items['CANT_1'])
                                                else:
                                                    valor_iva = int(VLRIVA_sin_ceros)

                                                if items['OBSEQUIO'] == 1: # logica obsequios
                                                    self.send_command("\x1b[[C") #F6
                                                    texto = f"{items['ITEMS']}\u000d{items['CANT_1']}\u000d1\u000d"
                                                else:
                                                    # Suma el precio unitario y el IVA calculado
                                                    total_con_iva = precio_uni + valor_iva
                                                    texto = f"{items['ITEMS']}\u000d{items['CANT_1']}\u000d{total_con_iva}\u000d"
                                                
                                                self.send_command(texto)
                                                self.send_command("\u000d")
                                        
                                        time.sleep(0.5)
                                        self.send_command('\x1B')
                                        self.send_command('3')
                                        time.sleep(0.5)
                                        
                                    if "[ INFORMACION DEL RECAUDO ]" in salida:
                                        texto = f"{jsonFacturas['recaudo']['MEDPAG']}"
                                        self.send_command(texto)
                                        self.send_command("\u000d")
                                        
                                        if jsonFacturas['recaudo']['MEDPAG'] == '022':
                                            self.send_command("\u000d")
                                            self.send_command("\u000d")
                                            self.send_command("\u000d")
                                            self.send_command("S")
                                            self.send_command("\u000d")
                                            self.send_command("0")
                                            
                                            time.sleep(25) # 10 SEGUNDOS... CUADRAR ESTO
                                            self.gen_json_rest(jsonFacturas['recaudo']['OBSERVACION'],factura,caja,0) # order,factura,caja
                                            factura +=1
                                            caja +=1
                                            break
                                        else:
                                            totalFactura = f"{jsonFacturas['recaudo']['VALOR']}"
                                            self.send_command(totalFactura)
                                            self.send_command("\u000d")
                                            self.send_command("1")
                                            self.send_command("\u000d \u000d \u000d")
                                            self.send_command("\u000d")
                                            self.send_command("\u000d")
                                            self.send_command("\u000d")
                                            self.send_command("S")
                                            self.send_command("\u000d")
                                            self.send_command("0")
                                            if "NO EXISTE SALDO EFECTIVO EN CAJA" in salida:
                                                self.gen_json_rest(jsonFacturas['recaudo']['OBSERVACION'],factura,caja,1) # order,factura,caja
                                                logf = f"Error al facturar Orden: {jsonFacturas['recaudo']['OBSERVACION']}"
                                                logging.debug(logf)  # Esto se guardará en logs.txt
                                            else:
                                                time.sleep(25) # 30 SEGUNDOS... CUADRAR ESTO
                                                self.gen_json_rest(jsonFacturas['recaudo']['OBSERVACION'],factura,caja,0) # order,factura,caja
                                                logf = f"Se facturo Orden: {jsonFacturas['recaudo']['OBSERVACION']} Factura # {factura}"
                                                logging.debug(logf)  # Esto se guardará en logs.txt
                                                factura +=1
                                                caja +=1
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
            
        except Exception as e:
            print("Error en el bucle principal:", e)   

        endpoint_resp = self.send_json_to_endpoint() # envia json generado a endpoint
        return {"api":endpoint_resp}
        