from collections import deque


class Stack:
    def __init__(self):
        self.container = deque()

    def push(self, data):
        self.container.append(data)

    def pop(self):
        return self.container.pop()

    def peek(self):
        return self.container[-1]

    def isEmpty(self):
        return len(self.container) == 0

    def getIndex(self, targetValue):
        return self.container.index(targetValue)

    def getSize(self):
        return len(self.container)
