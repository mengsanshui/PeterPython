from twisted.internet import protocol, reactor, endpoints
from sys import stdout

host = 'localhost'
port = 8888
class Echo(protocol.Protocol):
    def dataReceived(self, data):
        stdout.write(data)

class EchoClientFactory(protocol.ClientFactory):
    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        return Echo()

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)

reactor.connectTCP(host, port, EchoClientFactory())
reactor.run()
