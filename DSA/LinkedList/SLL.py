class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    def insertAtBegining(self, data):
        node = Node(data, self.head)
        self.head = node

    def displayLinkedList(self):
        if self.head is None:
            print('Linked list is empty')
            return

        iterator = self.head
        llstr = ''

        while iterator:
            llstr += str(iterator.data) + ('-->' if iterator.next else '')
            iterator = iterator.next

        print(llstr)

    def insertAtEnd(self, data):
        if self.head is None:
            self.head = Node(data)
            return

        iterator = self.head
        while iterator.next:
            iterator = iterator.next

        iterator.next = Node(data)

    def bulkInsertAtEnd(self, dataList):
        for data in dataList:
            self.insertAtEnd(data)

    def bulkInsertAtBegining(self, dataList):
        for data in dataList:
            self.insertAtBegining(data)

    def getLinkedListLength(self):
        length = 0
        iterator = self.head
        while iterator:
            length += 1
            iterator = iterator.next

        return length

    def removeAtPosition(self, targetPosition):
        if targetPosition < 1 or targetPosition > self.getLinkedListLength():
            print('Invalid target position')
            return

        if targetPosition == 1:
            self.head = self.head.next
            return

        position = 1
        iterator = self.head
        while iterator:
            if position == targetPosition - 1:
                iterator.next = iterator.next.next
                break

            iterator = iterator.next
            position += 1

    def inserAtPosition(self, targetPosition, data):
        if targetPosition < 1 or targetPosition > self.getLinkedListLength() + 1:
            print('Invalid target position')
            return

        if targetPosition == 1:
            self.insertAtBegining(data)
            return

        position = 1
        iterator = self.head
        while iterator:
            if position == targetPosition - 1:
                iterator.next = Node(data, iterator.next)
                break

            iterator = iterator.next
            position += 1

    def removeByValue(self, targetValue):
        if self.head is None:
            print('LinkedList is empty')
            return

        if self.head.data == targetValue:
            self.head = self.head.next
            return

        previousNode = self.head
        currentNode = self.head.next

        while currentNode:
            if currentNode.data == targetValue:
                previousNode.next = currentNode.next
                return

            previousNode = currentNode
            currentNode = currentNode.next

        print('Value doesn\'t exist in linked list')

    def insertAfterValue(self, targetValue, insertValue):
        if self.head is None:
            print('LinkedList is empty')
            return

        currentNode = self.head
        while currentNode:
            if currentNode.data == targetValue:
                currentNode.next = Node(insertValue, currentNode.next)
                return

            currentNode = currentNode.next

        print('Value doesn\'t exist in linked list')

    def insertBeforeValue(self, targetValue, insertValue):
        if self.head is None:
            print('LinkedList is empty')
            return

        if self.head.data == targetValue:
            self.head = Node(insertValue, self.head)
            return

        previousNode = self.head
        currentNode = self.head.next
        while currentNode:
            if currentNode.data == targetValue:
                previousNode.next = Node(insertValue, currentNode)
                return

            previousNode = currentNode
            currentNode = currentNode.next

        print('Value doesn\'t exist in linked list')

    def getPositionByvalue(self, targetValue):
        if self.head is None:
            print('LinkedList is empty')
            return

        position = 1
        iterator = self.head
        while iterator:
            if iterator.data == targetValue:
                return position

            iterator = iterator.next
            position += 1


if __name__ == '__main__':
    ll = LinkedList()
    ll.bulkInsertAtEnd([11, 12, 13, 14, 15])
    ll.removeAtPosition(4)
    ll.removeByValue(15)
    ll.insertAfterValue(15, 16)
    ll.insertBeforeValue(10, 16)
    ll.displayLinkedList()
    print(ll.getPositionByvalue(10))
    print(ll.getPositionByvalue(13))
    print(ll.getPositionByvalue(15))
