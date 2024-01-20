def getFirstOccurence(lst, target, position):
    if target == lst[position]:
        if 0 <= position-1 and target == lst[position-1]:
            return 'left'
        else:
            return 'found'
    elif target > lst[position]:
        return 'right'
    else:
        return 'left'


def getLastOccurence(lst, target, position):
    if target == lst[position]:
        if position < len(lst)-1 and target == lst[position+1]:
            return 'right'
        else:
            return 'found'
    elif target > lst[position]:
        return 'right'
    else:
        return 'left'


def binarySearch(lst, target, position=''):
    if len(lst) != 0:
        low = 0
        high = len(lst) - 1

        while low <= high:
            mid = (low + high)//2

            if position == 'last':
                result = getLastOccurence(lst, target, mid)
            else:
                result = getFirstOccurence(lst, target, mid)

            if result == 'found':
                return mid
            elif result == 'left':
                high = mid - 1
            else:
                low = mid + 1
    return -1


def testBinarySearch():
    lst = [1, 2, 2, 2, 2, 2, 2]

    print(binarySearch(lst, 2, 'first'))  # Output: 1
    print(binarySearch(lst, 2, 'last'))  # Output: 6
    print(binarySearch(lst, 7))  # Output: -1
    print(binarySearch(lst, 2))  # Output: 1


if __name__ == '__main__':
    testBinarySearch()
