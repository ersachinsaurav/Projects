class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    def getNodeLevel(self):
        level = 0
        parentNode = self.parent
        while parentNode:
            level += 1
            parentNode = parentNode.parent
        return level

    def displayTree(self):
        spaces = ' ' * self.getNodeLevel() * 3
        prefix = spaces + '|--' if self.parent else ''
        print(prefix + self.data)
        if self.children:
            for child in self.children:
                child.displayTree()


def buildProductTree():
    root = TreeNode('Electronics')

    laptop = TreeNode('Laptop')

    laptop.addChild(TreeNode('Surface'))
    laptop.addChild(TreeNode('ThinkPad'))

    mac = TreeNode('Mac')
    mac.addChild(TreeNode('M1'))
    mac.addChild(TreeNode('M2'))

    laptop.addChild(mac)

    cellPhone = TreeNode('Cell Phone')
    cellPhone.addChild(TreeNode('iPhone'))
    cellPhone.addChild(TreeNode('Google Pixel'))
    cellPhone.addChild(TreeNode('Vivo'))

    tv = TreeNode('TV')
    tv.addChild(TreeNode('Samsung'))
    tv.addChild(TreeNode('LG'))

    root.addChild(laptop)
    root.addChild(cellPhone)
    root.addChild(tv)

    return root


root = buildProductTree()
root.displayTree()
