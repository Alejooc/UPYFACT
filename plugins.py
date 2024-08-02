import os
import importlib
import json

class GestorPlugins:
    def __init__(self):
        self.plugins = {}
    
    def cargar_plugins(self):
        ruta_plugins = 'plugins'
        for nombre_archivo in os.listdir(ruta_plugins):
            if nombre_archivo.endswith('.py'):
                nombre_modulo = nombre_archivo[:-3]
               
                self.plugins[nombre_modulo] = nombre_archivo
    
    def mostrar_plugins_cargados(self):
        print("Plugins cargados:")
        for nombre, modulo in self.plugins.items():
            print(f"{nombre}")
    
    @staticmethod
    def contar_plugins():
        # Cargar el archivo de configuración JSON
        with open('plugins/config.json', 'r') as archivo_config:
            data = json.load(archivo_config)
        
        # Contar la cantidad de plugins
        cantidad_plugins = len(data['plugins'])
        return cantidad_plugins

def main():
    gestor_plugins = GestorPlugins()
    gestor_plugins.cargar_plugins()
    gestor_plugins.mostrar_plugins_cargados()

    cantidad = GestorPlugins.contar_plugins()
    print(f"La cantidad de plugins creados es: {cantidad}")

if __name__ == "__main__":
    main()