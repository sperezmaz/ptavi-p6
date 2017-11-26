#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente UDP que abre un socket a un servidor."""
import sys
import socket

metodos = ['invite', 'ack', 'bye']
# Constantes. Dirección IP del servidor y contenido a enviar
try:
    METODO = sys.argv[1]
    address_port = sys.argv[2]
    NAME = address_port.split('@')[0]
    resto = address_port.split('@')[1] 
    SERVER = resto.split(':')[0] 
    PUERTO = int(resto.split(':')[1]) 

except:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")

line1 = METODO.upper() + " sip:" + NAME + "@" + SERVER + ' SIP/2.0\r\n'
line = line1 + '\r\n\r\n'
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PUERTO))
    print("Enviando:", line)
    my_socket.send(bytes(line, 'utf-8'))  # lo pasamos a bytes
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))  # pasa a string los bytes

print("Socket terminado.")
