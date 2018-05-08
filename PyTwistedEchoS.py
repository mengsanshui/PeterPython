
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic

class PubProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        for c in self.factory.clients:
            source = u"<{}>".format(self.transport.getHost()).encode("ascii ")
            c.sendLine(source + line)

class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()
    def buildProtocol(self, addr):
        return PubProtocol(self)

reactor.listenTCP(8888, PubFactory())
reactor.run()
