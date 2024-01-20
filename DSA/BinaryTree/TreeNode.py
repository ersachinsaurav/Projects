class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.rootNode = None

    def insertElement(self, data):
        if not self.rootNode:
            self.rootNode = TreeNode(data)
        else:
            self._insertElement(data, self.rootNode)

    def _insertElement(self, data, currentNode):
        if data < currentNode.data:
            if currentNode.left is None:
                currentNode.left = TreeNode(data)
            else:
                self._insertElement(data, currentNode.left)
        elif data > currentNode.data:
            if currentNode.right is None:
                currentNode.right = TreeNode(data)
            else:
                self._insertElement(data, currentNode.right)

    def findMax(self, currentNode=None):
        if currentNode is None:
            currentNode = self.rootNode

        if not currentNode:
            return None  # Tree is empty

        if currentNode.right:
            return self.findMax(currentNode.right)
        else:
            return currentNode.data


# Example usage
if __name__ == "__main__":
    binaryTree = BinaryTree()
    elementsToInsert = [8, 3, 10, 1, 6, 14, 4, 7, 13]

    for element in elementsToInsert:
        binaryTree.insertElement(element)

    max_value = binaryTree.findMax()
    print("Maximum value in the binary tree:", max_value)
