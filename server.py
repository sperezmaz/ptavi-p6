#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Cliente UA que funciona como servidor. Envia el audio via RTP al otro UA."""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    def handle(self):
        """handle method of the server class."""
        # Escribe dirección y puerto del cliente (de tupla client_address)
        line = self.rfile.read()
        print(line.decode('utf-8'))
        message = line.decode('utf-8').split()
        metodo = message[0]
        ip_client = self.client_address[0]
        if metodo == "INVITE":
            self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
            self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        elif metodo == "ACK":
            # aEjecutar es un string con lo que se ha de ejecutar en la shell
            aEjecutar1 = 'mp32rtp -i ' + ip_client + ' -p 23032 < '
            aEjecutar = aEjecutar1 + FICHERO_AUDIO
            print("Vamos a ejecutar", aEjecutar)
            os.system(aEjecutar)
        elif metodo == "BYE":
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        elif metodo not in ["INVITE", "ACK", "BYE"]:
            self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
        else:
            self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")


if __name__ == "__main__":
    try:
        IP = sys.argv[1]
        PORT_SERV = int(sys.argv[2])
        FICHERO_AUDIO = sys.argv[3]
    except:
        sys.exit("Usage: python3 server.py IP port audio_file")
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((IP, PORT_SERV), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()  # espera en un bucle
    except KeyboardInterrupt:  # ^C
        print("Finalizado servidor")
