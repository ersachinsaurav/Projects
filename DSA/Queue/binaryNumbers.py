from Queue import Queue


def generateBinaries(limit):
    binariesQueue = Queue()
    binariesQueue.enqueue('1')

    for _ in range(limit):
        binariesQueue.enqueue(binariesQueue.peek() + '0')
        binariesQueue.enqueue(binariesQueue.peek() + '1')
        print(binariesQueue.peek())
        binariesQueue.dequeue()


generateBinaries(20)
