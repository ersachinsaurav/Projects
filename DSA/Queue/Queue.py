from collections import deque


class Queue:
    def __init__(self):
        self.container = deque()

    def enqueue(self, data):
        self.container.appendleft(data)

    def dequeue(self):
        return self.container.pop()

    def isEmpty(self):
        return len(self.container) == 0

    def getSize(self):
        return len(self.container)

    def peek(self):
        return self.container[-1]


if __name__ == '__main__':
    que = Queue()
    que.enqueue(1)
    que.enqueue(3)
    que.enqueue(4)
    que.enqueue(5)
    print(que.container)
    print(que.container.pop())
