class Array:
    def __init__(self):
        self._data = []

    def append(self, item):
        self._data.append(item)

    def insert(self, index, item):
        self._data.insert(index, item)

    def remove(self, item):
        if item in self._data:
            self._data.remove(item)

    def pop(self, index=-1):
        return self._data.pop(index)

    def get(self, index):
        return self._data[index]

    def length(self):
        return len(self._data)

    def to_list(self):
        return self._data[:]
