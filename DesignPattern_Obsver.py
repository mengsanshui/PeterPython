class Observer():
    def __init__(self):
        self.__observer = []
    def Regsiter(self, observer):
        self.__observer.append(observer)
    def NotifyALL(self, *args, **kwargs):
        for observer in self.__observer:
            observer.action(self, *args, **kwargs)

class ObserverOne():
    def __init__(self, Observer):
        Observer.Regsiter(self)
    def action(self, Observer, *args):
        print("Invoke ObserverOne method")




