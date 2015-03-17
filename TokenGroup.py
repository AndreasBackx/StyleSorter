class TokenGroup(object):

    def __init__(self):
        self.tokenList = []

    def __add__(self, b):
        if type(b) is tuple:
            self.tokenList.append(b)
        else:
            self.tokenList.extend(b.tokenList)
        return self

    def __repr__(self):
        return str(self.tokenList)
