class MemoryBuffer:
    def __init__(self):
        self.logs = []

    def add(self, msg):
        self.logs.append(msg)

    def get_all(self):
        return self.logs[-5:]
