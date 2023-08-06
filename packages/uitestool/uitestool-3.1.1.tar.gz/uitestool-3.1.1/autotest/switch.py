class Switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *args):
        # 字符串比较
        if self.fall or not args:
            return True
        # 数值比较
        elif self.value in args:
            # self.fall = True
            return True
            # else:
            #     return False