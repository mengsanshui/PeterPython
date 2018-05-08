class Actor():
    def __init__(self):
        self.isBusy = False
    def Status(self):
        return self.isBusy
    def Work(self):
        self.isBusy = True
        print("Do something")

class Agent():
    def __init__(self):
        self.customer = None
    def work(self):
        self.actor = Actor()
        self.customer.append(self.actor)
        if not self.actor.Status():
            self.actor.Work()



