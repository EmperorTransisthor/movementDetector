import socket


def send(data: str):
    host = "127.0.0.1"
    port = 20000

    sock = socket.socket()
    sock.connect((host, port))

    sock.send(bytearray(data, "utf-8"))

    sock.close()
