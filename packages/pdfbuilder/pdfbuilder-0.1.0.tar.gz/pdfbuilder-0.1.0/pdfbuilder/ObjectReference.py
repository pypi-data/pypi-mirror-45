class ObjectReference:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return '%d 0 R' % self.id
