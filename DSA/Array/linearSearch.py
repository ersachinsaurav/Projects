def linearSearch(lst, target):
    if len(lst) != 0:
        for i in range(len(lst)):
            if lst[i] == target:
                return i
    return -1

def testLinearSearch():
    lst = [1, 2, 3, 4, 5, 6]

    print(linearSearch(lst, 5))
    print(linearSearch(lst, 7))

if __name__ == "__main__":
    testLinearSearch()
