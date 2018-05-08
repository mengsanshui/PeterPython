import socket
import threading

host = "127.0.0.1"
port = 80

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

def handle_client(client_socket):
    # print out what the client sends
    request = client_socket.recv(1024).decode()
    print("[*] Received: %s" % request)
    # send back a packet
    client_socket.send("ACK!")
    client_socket.close()

while True:
    client, addr = server.accept()
    print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()
