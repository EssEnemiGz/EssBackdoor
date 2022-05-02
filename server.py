from socket import *
from subprocess import check_output
import JustASocketLibrary.jsl as jsl
import base64 
import time

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind( ("localhost", 1414) )
s.listen(5)

print("Esperando conexiones...")
cnn, addr = s.accept()
print(f"Nueva conexión de -> {addr[0]}")

try:
    while 1:
        msg = input("$ ")

        if msg == "exit":
            cnn.send(msg.encode())
            cnn.close()
            exit()

        elif msg == "":
            continue

        elif msg.split()[0] == "descargar" and len(msg) > 1:
            try:
                verification = msg.split()[1]
                print("Descarga completada.")
            except IndexError:
                continue

            cnn.send(msg.encode())
            
            try:
                jsl.recvFile(cnn)
            except IndexError:
                print("No se encontró el nombre del archivo a descargar.")
            except FileNotFoundError:
                print("El archivo no existe.")

        elif msg.split()[0] == "descargar" and len(msg) == 1:
            print("Faltó información.")
            continue 

        elif msg.split()[0] == "subir":
            cnn.send("subir".encode())
            try:
                jsl.sendFile(msg.split()[1], cnn)
            except IndexError:
                print("No se encontró el nombre del archivo a subir")
            except FileNotFoundError:
                print("No se encontró el archivo")
        else:
            cnn.send(msg.encode())
            result = cnn.recv(1024).decode()
            print(result)
except KeyboardInterrupt:    
    s.close()

