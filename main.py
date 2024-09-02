import requests
from server import Server
from colorama import init, Fore, Style
from core import Core

def check_endpoint(url,data=None):
    try:
        response = requests.post(url,data=data)
        # Verifica si el status code es 200, lo que indica que la solicitud fue exitosa
        if response.status_code == 200:
            return Fore.GREEN + f"Online." + Style.RESET_ALL
        else:
            return Fore.RED +  f"Offline. Código de estado: {response.status_code}" + Style.RESET_ALL
    except requests.exceptions.RequestException as e:
        # Captura cualquier error que ocurra durante la solicitud
        return Fore.RED + f"Error al intentar acceder al endpoint {url}: {e}" + Style.RESET_ALL
    
def main():
    texto_grande = """
 ____    ______  ____    ______         __  __  __  __  _____      
/\  _`\ /\  _  \/\  _`\ /\__  _\       /\ \/\ \/\ \/\ \/\  __`\    
\ \ \L\_\ \ \L\ \ \ \/\_\/_/\ \/       \ \ \ \ \ \ `\\ \ \ \/\ \   
 \ \  _\/\ \  __ \ \ \/_/_ \ \ \  ______\ \ \ \ \ \ , ` \ \ \ \ \  
  \ \ \/  \ \ \/\ \ \ \L\ \ \ \ \/\______\ \ \_\ \ \ \`\ \ \ \_\ \ 
   \ \_\   \ \_\ \_\ \____/  \ \_\/______/\ \_____\ \_\ \_\ \_____
    \/_/    \/_/\/_/\/___/    \/_/         \/_____/\/_/\/_/\/_____/                                                                                                        
    """
    print("\033[91m" + texto_grande + "\033[0m")
    # Para iniciar el servidor, puedes hacer lo siguiente:
    print(Fore.RED + "VERSION: 1.0.0" + Style.RESET_ALL)
    print(Fore.CYAN + "INFO: Waiting for application startup" + Style.RESET_ALL)
    env_loader = Core()
    debug = env_loader
    if debug.get_debug():
        print(Fore.CYAN + "ENVIROMENT: DESARROLLO" + Style.RESET_ALL)
    else:
        print(Fore.RED + "ENVIROMENT: PRODUCTION" + Style.RESET_ALL)

    print(Fore.CYAN + f"LICENCIA: {debug.get_companyName()}" + Style.RESET_ALL)
    #print(Fore.CYAN + f"LOGS: {debug.get_logs()}" + Style.RESET_ALL)
    print(Fore.CYAN + f"CLIENT ENDPOINT: {check_endpoint(debug.get_endpointClient())}" + Style.RESET_ALL)

    
   
if __name__ == "__main__":
        main()
        server = Server()
        server.run()
       


