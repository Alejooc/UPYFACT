
import os

class Facturacion:
    def __init__(self, json):
        self.json = json

    # Función para convertir el JSON en el formato de archivo plano
    def json_to_flat_file(self,json_data):
        flat_file_content = ""
        for data_princi in json_data:
            # Agregar registros de items
            for item in data_princi["items"]:
                nro_fc = str(item.get("NRO_FC", "0")).zfill(6)
                item_id = str(item.get("ITEMS", "0")).zfill(6)
                precio_und = str(item.get("PRECIO_UNI", "0")).zfill(9)
                valor_bruto= str(item.get("VLRTOT_BRU", "0")).zfill(9)
                cant_1= str(item.get("CANT_1", "0")).zfill(6)
                flat_file_content += f'{str(item.get("TIPO_REG"))}{str(item.get("FECHA"))}{str(item.get("CO"))}{str(item.get("CAJA"))}{str(item.get("NTD_CAJA"))}{str(item.get("TIPO_FC"))}{str(nro_fc)}{str(item_id).zfill(4)}   000{str(cant_1)}000+{str(item.get("LIPRE"))}        {str(precio_und)}00+00{str(valor_bruto)}00+{str(item.get("DSCTO1", "0")).zfill(15)}+{str(item.get("TASA_IVA", "0")).zfill(4)}{str(item.get("VLRIVA"))}00+{str(item.get("VLRNET"))}00+{str(item.get("MOTIVO", "0")).zfill(2)}   000000000{str(item.get("IND_ITEMS"))}\n'

            # Agregar registro de recaudo
            recaudo = data_princi["recaudo"]
        
            flat_file_content += f'{recaudo["TIPO_REG"]}{recaudo["FECHA"]}{recaudo["CO"]}{recaudo["CAJA"]}{recaudo["NTD_CAJA"]}{recaudo["TIPO_REC"]}{recaudo["MEDPAG"]}{recaudo["IND_IE"]}                                      {recaudo["REFERENCIA"]:<10}0.0                 0000000000000+0000000000000+1  100000               {str(recaudo.get("VALOR", "0")).zfill(17)}00+00000000000000000+               {recaudo["OBSERVACION"]:<20}\n'

        return flat_file_content

    # Generar el archivo plano
    async def generate_flat_file(self,file_name, json_data):
        flat_file_content = self.json_to_flat_file(json_data)
        directory = "./trm_cajas"
        ruta = os.path.join(directory, file_name)
        with open(ruta, 'w') as f:
            f.write(flat_file_content)
