import sys
import socket
import argparse

host = 'localhost'
data_payload = 2048
backlog = 5

def echo_server(port):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    server_addr = (host, port)
    sock.bind(server_addr)
    sock.listen(backlog)

    while True:
        client, cliaddr = sock.accept()
        data = client.recv(data_payload)
        if data:
            print("Recieve Data: %s from %s" % (data, cliaddr))
            client.send(data)
            print("Sent %s bytes back to % s " % (data, cliaddr))

        client.close()


if __name__ == '__main__':
    arg = argparse.ArgumentParser('TCP server example')
    arg.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = arg.parse_args()
    port = given_args.port
    echo_server(port)




