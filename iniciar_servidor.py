import os
import webbrowser
import subprocess
import time

def iniciar_servidor():
    ruta_directorio = r'C:\Users\JAMES\Desktop\trabajo\Base_datos_Empresa'
    
    os.chdir(ruta_directorio)
    
    subprocess.Popen('git pull', shell=True)
    
    time.sleep(2)
    
    subprocess.Popen('python manage.py runserver', shell=True)
    
    time.sleep(2)
    
    webbrowser.open('http://127.0.0.1:8000')

if __name__ == "__main__":
    iniciar_servidor()
