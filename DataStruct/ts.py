class ts:
    __slots__ = ['ts','index']

    # 时间序列的基类
    length=0

    def __init__(self,name):
        self.name=name

    def getLongth(self):
        return self.length