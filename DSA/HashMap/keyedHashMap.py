class HashMap:
    def __init__(self) -> None:
        self.MAX = 10
        self.array = [[] for i in range(self.MAX)]

    def getHashKey(self, key):
        hashKey = 0

        for char in key:
            hashKey += ord(char)
        return hashKey % self.MAX

    def __setitem__(self, key, value):
        hashKey = self.getHashKey(key)
        keyExists = False

        for index, element in enumerate(self.array[hashKey]):
            if element and element[0] == key:
                self.array[hashKey][index] = (key, value)
                keyExists = True
                break
        if not keyExists:
            self.array[hashKey].append((key, value))

    def __getitem__(self, key):
        hashKey = self.getHashKey(key)

        for index, element in enumerate(self.array[hashKey]):
            if element and element[0] == key:
                return self.array[hashKey][index][1]

    def __delitem__(self, key):
        hashKey = self.getHashKey(key)
        for index, element in enumerate(self.array[hashKey]):
            if element and element[0] == key:
                self.array[hashKey].pop(index)


hashMap = HashMap()
hashMap['name'] = 'Sachin'
hashMap['naem'] = 'Ale'
hashMap['name'] = 'Sachin Saurav'
print(hashMap.array)

print(hashMap['name'])
# print(hashMap['naem'])

# del hashMap['naem']
# del hashMap['name']

# print(hashMap['name'])
# print(hashMap['naem'])
