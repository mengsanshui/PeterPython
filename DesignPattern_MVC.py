class Model(object):
    def __init__(self):
        self.services = {'SMS':"Test sms",
                        'EMAIL':"Test email"
                        }
    def get_services(self):
        return self.services.keys()

class View(object):
    def list_services(self, services):
        for i in services:
            print('Services is %s'% i)

class Controler(object):
    def __init__(self):
        self.model = Model()
        self.view = View()

    def get_services(self,):
        services = self.model.get_services()
        return (self.view.list_services(services))

class Client(object):
    con = Controler()
    con.get_services()

if __name__ == '__main__':

    c = Client()



