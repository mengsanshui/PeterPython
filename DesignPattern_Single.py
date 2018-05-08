class Single:
    __Instance = None
    def __init__(self):
        if not Single.__Instance:
            print("No __Instance create")
        else:
            print("__Instace already created")

    @classmethod
    def get_instace(cls):
        if not cls.__Instance:
            cls.__Instance = Single()
        return cls.__Instance

