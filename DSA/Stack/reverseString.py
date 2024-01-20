import Stack

string = Stack.Stack()


def putStringIntoStack(str):
    for char in str:
        string.push(char)


def getReversedString():
    str = ''
    while string.getSize() > 0:
        str += string.pop()
    return str


str = input()
putStringIntoStack(str)
print(getReversedString())
