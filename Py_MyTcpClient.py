import socket

targethost =  "www.sohu.com"
targetport = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((targethost,targetport))

client.send("GET / HTTP/1.1\r\n Host:sohu.com\r\n\r\n".encode())
res = client.recv(4096).decode()


print(res)

