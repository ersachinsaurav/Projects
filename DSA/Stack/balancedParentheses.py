from Stack import Stack


def matchParenthesesPairs(closingParen, openingParen):
    parensPairs = {
        ')': '(',
        '}': '{',
        ']': '[',
    }

    if parensPairs[closingParen]:
        return parensPairs[closingParen] == openingParen
    else:
        return False


def isParenthesesBalanced(string):
    parensStack = Stack()
    for char in string:
        if char in ['(', '{', '[']:
            parensStack.push(char)
        if char in [')', '}', ']']:
            if parensStack.getSize() == 0:
                return False
            if False == matchParenthesesPairs(char, parensStack.pop()):
                return False
    return True


if __name__ == '__main__':
    print(isParenthesesBalanced("({a+b})"))
    print(isParenthesesBalanced("))((a+b}{"))
    print(isParenthesesBalanced("((a+b))"))
    print(isParenthesesBalanced("((a+g))"))
    print(isParenthesesBalanced("))"))
    print(isParenthesesBalanced("[a+b]*(x+2y)*{gg+kk}"))
