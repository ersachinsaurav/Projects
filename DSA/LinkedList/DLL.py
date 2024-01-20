class Node:
    def __init__(self, previous=None, data=None, next=None):
        self.previous = previous
        self.data = data
        self.next = next


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        if self.head is None:
            return True
        return False

    def insertAtBegining(self, data):
        node = Node(None, data, self.head)
        if self.isEmpty():
            self.tail = node
        else:
            self.head.previous = node

        self.head = node

    def insertAtEnd(self, data):
        node = Node(self.tail, data, None)
        if self.isEmpty():
            self.head = node
        else:
            self.tail.next = node

        self.tail = node

    def insertBeforeValue(self, targetValue, insertValue):
        if self.isEmpty():
            return print('Linked list is empty')

        currentNode = self.head
        while currentNode.data != targetValue:
            currentNode = currentNode.next
        if currentNode:
            if currentNode.previous:
                node = Node(currentNode.previous,
                            insertValue, currentNode)
                currentNode.previous.next = node
            else:
                node = Node(None, insertValue, currentNode)
                self.head = node
            currentNode.previous = node
            return
        print('Value not found in linked list')

    def insertAfterValue(self, targetValue, insertValue):
        if self.isEmpty():
            return print('Linked list is empty')

        currentNode = self.head
        while currentNode.data != targetValue:
            currentNode = currentNode.next
        if currentNode:
            if currentNode.next:
                node = Node(currentNode.next.previous,
                            insertValue, currentNode.next)
                currentNode.next.previous = node
            else:
                node = Node(currentNode, insertValue, None)
                self.tail = node
            currentNode.next = node
            return
        print('Value not found in linked list')

    def insertAtPosition(self, targetPosition, insertValue):
        if targetPosition < 1 or targetPosition > self.getLength():
            print('Invalid target position')
            return

        if targetPosition == 1:
            self.insertAtBegining(insertValue)
        elif targetPosition == self.getLength():
            self.insertAtEnd(insertValue)
        else:
            currentNode = self.head
            position = 1
            while currentNode:
                if position == targetPosition:
                    node = Node(currentNode.previous, insertValue, currentNode)
                    currentNode.previous.next = node
                    currentNode.previous = node
                    return
                currentNode = currentNode.next
                position += 1

    def getLength(self):
        length = 0
        iterator = self.head
        while iterator:
            length += 1
            iterator = iterator.next

        return length

    def displayLinkedList(self):
        if self.isEmpty():
            return print('Linked list is empty')

        iterator = self.head
        strData = ''

        while iterator:
            strData += str(iterator.data) + ('<-->' if iterator.next else '')
            iterator = iterator.next

        print(strData)

    def displayReversedLinkedList(self):
        if self.isEmpty():
            return print('Linked list is empty')

        iterator = self.tail
        strData = ''

        while iterator:
            strData += str(iterator.data) + \
                ('<-->' if iterator.previous else '')
            iterator = iterator.previous

        print(strData)

    def removeAtPosition(self, targetPosition):
        if self.isEmpty():
            return print('Linked list is empty')

        if targetPosition < 1 or targetPosition > self.getLength():
            print('Invalid target position')
            return

        if targetPosition == 1:
            self.head = self.head.next
            if self.head:
                self.head.previous = None
            else:
                self.tail = None
        else:
            currentNode = self.head
            position = 1
            while position < targetPosition:
                currentNode = currentNode.next
                position += 1

            if currentNode:
                currentNode.previous.next = currentNode.next
                if currentNode.next:
                    currentNode.next.previous = currentNode.previous
                else:
                    self.tail = currentNode.previous

    def removeByValue(self, targetValue):
        if self.isEmpty():
            print('Linked list is empty')
            return

        currentNode = self.head
        while currentNode and currentNode.data != targetValue:
            currentNode = currentNode.next

        if currentNode:
            # Element is in between head and tail
            if currentNode.previous and currentNode.next:
                currentNode.previous.next = currentNode.next
                currentNode.next = currentNode.next.next

            # Element is tail
            elif currentNode.previous and currentNode.next is None:
                currentNode.previous.next = None
                self.tail = None

            # Element is head
            else:
                self.head = currentNode.next
                if currentNode.next:
                    currentNode.next.previous = None

            return

        print('Value not found in linked list')

    def updateValueAtPosition(self, targetPosition, updatedValue):
        if self.isEmpty():
            return print('Linked list is empty')

        if targetPosition < 1 or targetPosition > self.getLength():
            print('Invalid target position')
            return

        currentNode = self.head
        for position in range(1, targetPosition + 1):
            if position == targetPosition:
                currentNode.data = updatedValue
                return
            currentNode = currentNode.next


if __name__ == '__main__':
    dll = DoublyLinkedList()
    dll.insertAtBegining(20)
    dll.insertAtBegining(10)
    dll.insertAtEnd(30)
    dll.displayLinkedList()
    dll.updateValueAtPosition(1, 15)
    dll.updateValueAtPosition(2, 35)
    dll.updateValueAtPosition(3, 45)
    dll.displayLinkedList()

    dll.removeByValue(10)
    # dll.displayLinkedList()

    # dll.removeByValue(20)
    # dll.displayLinkedList()

    # dll.removeByValue(30)
    # dll.displayLinkedList()
