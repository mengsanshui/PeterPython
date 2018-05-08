import sys
import socket
import argparse

host = 'localhost'

def echo_client(port):
    sock = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    server_addr = (host, port)
    sock.connect(server_addr)
    while True:
        try:
            message = "Test message. This will be echoed"
            sock.sendall( message.encode('utf-8') )
            amount_received = 0
            amount_expected = len(message)
            while amount_received < amount_expected:
                data = sock.recv(16)
                amount_received += len(data)
                print("Received: %s" % data)
        except socket.error as e:
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            print("Closing connection to the server")
            sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP Client Example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)

