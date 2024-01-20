class TreeNode:
    def __init__(self, name, designation=None):
        self.name = name
        self.designation = designation
        self.subordinates = []
        self.manager = None

    def addSubordinate(self, subordinate):
        subordinate.manager = self
        self.subordinates.append(subordinate)

    def getNodeLevel(self):
        level = 0
        managerNode = self.manager
        while managerNode:
            level += 1
            managerNode = managerNode.manager
        return level

    def displayTree(self, showName=True, showDesignation=True, level=None):

        if not showName and not showDesignation:
            print('Pass desired flags to display the tree')
            return

        if level is None or self.getNodeLevel() < level:
            spaces = ' ' * self.getNodeLevel() * 3
            prefix = spaces + '|--' if self.manager else ''

            if showName and showDesignation:
                print(f"{prefix} {self.name} {'(' + self.designation + ')'}")
            elif showName and not showDesignation:
                print(f"{prefix} {self.name}")
            else:
                print(f"{prefix} {self.designation}")

        if self.subordinates:
            for subordinate in self.subordinates:
                subordinate.displayTree(showName, showDesignation, level)


def buildEmployeeTree():
    root = TreeNode('Sachin Saurav', 'CEO')

    cto = TreeNode('Ghulam Ale Mustafa', 'CTO')
    iHead = TreeNode('Vishwa', 'Infra Head')
    iHead.addSubordinate(TreeNode('Dhaval', 'Cloud Manager'))
    iHead.addSubordinate(TreeNode('Abhijit', 'DevOps  Manager'))

    aHead = TreeNode('Dhaval', 'App Head')

    cto.addSubordinate(iHead)
    cto.addSubordinate(aHead)

    hrHead = TreeNode('Gladys Dokka', 'HR Head')
    hrHead.addSubordinate(TreeNode('Udit Kumar', 'Recruitment Manager'))
    hrHead.addSubordinate(TreeNode('Utkarsh Kumar', 'Policy Manager'))

    root.addSubordinate(cto)
    root.addSubordinate(hrHead)

    return root


if __name__ == '__main__':
    root = buildEmployeeTree()
    root.displayTree()
    print()
    root.displayTree(True, False)
    print()
    root.displayTree(False)
    print()
    root.displayTree(False, True, 2)
