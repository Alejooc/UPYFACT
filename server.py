from typing import Union, List, Any
from fastapi import FastAPI
import uvicorn
from datetime import datetime
from recep import Recepcion
from facturacion import Facturacion
from electronica import Electronica
import pytz
from core import Core

class Server:
    def __init__(self):
        self.app = FastAPI()
        self.env_loader = Core()
        self.configure_routes()

    def configure_routes(self):
        @self.app.get("/")
        def read_root():
            return {"Hello": "World"}
        
        @self.app.post("/test")
        async def test(data: List[Any]):
            ssh_details = {
                    "hostname": '192.168.0.150',
                    "port": 1634,
                    "username": 'root',
                    "password": 'sistemasaris2022-/*'
            }
            electronica = Electronica(ssh_details, data)
            api = electronica.run()
            return {"resp": api}

        @self.app.get("/items/{item_id}")
        def read_item(item_id: int, q: Union[str, None] = None):
            return {"item_id": item_id, "q": q}

        @self.app.post("/facturacion/")
        async def receive_json(data: List[Any]):
            # Definir la zona horaria para Bogotá, Colombia
            zona_horaria = pytz.timezone('America/Bogota')

            # Obtener la fecha y hora actual en la zona horaria especificada
            fecha_actual = datetime.now(zona_horaria)

            # Formatear la fecha en el formato YYYYMMDD
            fecha_formateada = fecha_actual.strftime("%Y%m%d")
            facturacion = Facturacion("nombre")
            await facturacion.generate_flat_file(fecha_formateada + ".PO1", data)
            return {"message": "Se ha generado el archivo POJ", "type": 1, "name_poj": fecha_formateada}
        
        @self.app.post("/electronica/")
        async def receive_json2(data: List[Any]):
            ssh_details = {
                    "hostname": self.env_loader.get_host_ssh(),
                    "port": self.env_loader.get_port_ssh(),
                    "username": self.env_loader.get_user_ssh(),
                    "password": self.env_loader.get_pass_ssh()
            }
            electronica = Electronica(ssh_details, data)
            electronica.run()
            return {"message": "Json electronicas", "type": 1}

        @self.app.get("/recepcion/")
        def recepcion_poj():
            
            receiver = Recepcion(hostname='192.168.0.150', port="1634", username='alejandro', password='alejandro123*')
            receiver.conectar()
            
            recepcionar_facturas = receiver.interactuar_con_consola()

            receiver.desconectar()
            return {"recepcion": 1,"cg1_resp":recepcionar_facturas}

    def run(self, host="127.0.0.1", port=8000):
        uvicorn.run(self.app, host=host, port=port)

