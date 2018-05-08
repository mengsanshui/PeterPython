class Adapter:
    def __init__(self, adapterone):
        self.adapter =  adapterone
    def function(self):
        self.adapeter.require_function()
    def __getattr__(self, attr):
        return getattr(self.adapter, attr)

