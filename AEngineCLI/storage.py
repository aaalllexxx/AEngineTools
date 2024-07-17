class GlobalStorage:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
           cls.__instance = super(GlobalStorage, cls).__new__(cls)
        return cls.__instance