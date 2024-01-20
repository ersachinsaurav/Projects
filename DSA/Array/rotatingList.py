def findDirectionOfLowestValue(list, mid, high, searchType='position', target=''):
    if ('position' == searchType and mid > 0 and list[mid-1] > list[mid]) or ('value' == searchType and mid > 0 and target == list[mid]):
        return 'mid'
    elif list[mid] > list[high]:
        return 'right'
    else:
        return 'left'


def findNumberInRotatedSortedListUsingBinarySearch(list, target):
    if 0 != len(list):
        low = 0
        high = len(list) - 1
        while low <= high:
            mid = (low + high) // 2
            direction = findDirectionOfLowestValue(
                list, mid, high, 'value', target)

            if 'mid' == direction:
                return 'Found'
            elif 'left' == direction:
                high = mid - 1
            else:
                low = mid + 1
    return 'Not found'


def findNumberOfRotationsUsingBinarySearch(list):
    # TODO update this to handle repeating values
    if 0 != len(list):
        low = 0
        high = len(list) - 1
        while low <= high:
            mid = (low + high) // 2
            direction = findDirectionOfLowestValue(list, mid, high)

            if 'mid' == direction:
                return mid
            elif 'left' == direction:
                high = mid - 1
            else:
                low = mid + 1
    return 0


def findNumberOfRotationsUsingLinearSearch(list):
    if 0 != len(list):
        position = 1
        while position < len(list):
            if list[position-1] > list[position]:
                return position
            position += 1
    return 0


# testing code
lst = [1, 2, 3, 4, 5, 6, 7, 8]
rotatedList = [7, 8, 1, 2, 3, 4, 5, 6]
print(findNumberOfRotationsUsingLinearSearch(rotatedList))
print(findNumberOfRotationsUsingBinarySearch(rotatedList))
print(findNumberInRotatedSortedListUsingBinarySearch(rotatedList, 2))

lst = [-1, 0, 1, 2, 3, 4, 5]
rotatedList = [1, 2, 3, 4, 5, -1, 0]
print(findNumberOfRotationsUsingBinarySearch(rotatedList))
print(findNumberOfRotationsUsingBinarySearch(rotatedList))
print(findNumberInRotatedSortedListUsingBinarySearch(rotatedList, 9))
