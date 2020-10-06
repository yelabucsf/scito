class ChainResult(tuple):
    def __new__(cls, *args):
        return super(ChainResult, cls).__new__(cls, args)
    def __getattribute__(self, name):
        try:
            return getattr(super(), name)
        except AttributeError:
            return getattr(super().__getitem__(0), name)