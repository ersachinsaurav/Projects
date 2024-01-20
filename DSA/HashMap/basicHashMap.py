class HashMap:
    def __init__(self) -> None:
        self.MAX = 10
        self.array = [None for i in range(self.MAX)]

    def getHashKey(self, key):
        hashKey = 0
        for char in key:
            hashKey += ord(char)
        return hashKey % self.MAX

    # def setItem(self, key, value):
    # override Python's __setitem__
    def __setitem__(self, key, value):
        hashKey = self.getHashKey(key)
        self.array[hashKey] = value

    # def getItem(self, key):
    def __getitem__(self, key):
        hashKey = self.getHashKey(key)
        return self.array[hashKey]

    # def deleteItem(self, key):
    def __delitem__(self, key):
        hashKey = self.getHashKey(key)
        self.array.pop(hashKey)


hashMap = HashMap()
# hashMap.setItem('name', 'Sachin')
hashMap['name'] = 'Sachin'
# print(hashMap.getItem('name'))
print(hashMap['name'])
# hashMap.deleteItem('name')
del hashMap['name']
# print(hashMap.getItem('name'))
print(hashMap.array)
