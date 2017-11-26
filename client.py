#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente UDP que abre un socket a un servidor."""
import sys
import socket

# Constantes. Dirección IP del servidor y contenido a enviar
try:
    METODO = sys.argv[1].upper()
    address_port = sys.argv[2]
    NAME = address_port.split('@')[0]
    resto = address_port.split('@')[1] 
    SERVER = resto.split(':')[0] 
    PUERTO = int(resto.split(':')[1]) 

except:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")

line = METODO + " sip:" + NAME + "@" + SERVER + " SIP/2.0\r\n\r\n"
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PUERTO))
    if METODO == "INVITE" or METODO == "BYE":
        print("Enviando:", line)
        my_socket.send(bytes(line, 'utf-8'))  # lo pasamos a bytes
        data = my_socket.recv(1024)
        condicion1 = data.decode('utf-8').split(" ")[-1]
        if condicion1 == "OK\r\n\r\n" and METODO != "BYE":
            print('Recibido -- ', data.decode('utf-8'))
            line_ack = "ACK sip:" + NAME + "@" + SERVER + " SIP/2.0\r\n\r\n"
            my_socket.send(bytes(line_ack, 'utf-8'))
            data = my_socket.recv(1024)
            print('Recibido -- ', data.decode('utf-8'))
    else:
        print("Método no válido")
print("Socket terminado.")
