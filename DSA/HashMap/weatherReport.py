class WeatherReport:
    def __init__(self):
        self.MAX = 10
        self.array = [[] for i in range(self.MAX)]

    def generateHashKey(self, key):
        hashKey = 0
        for char in key:
            hashKey += ord(char)
        return hashKey % 10

    def setItem(self, key, value):
        hashKey = self.generateHashKey(key)
        for index, element in enumerate(self.array[hashKey]):
            if element and element[0] == key:
                self.array[hashKey][index] = (key, value)
                return

        self.array[hashKey].append((key, value))

    def getItem(self, key):
        hashKey = self.generateHashKey(key)
        for index, element in enumerate(self.array[hashKey]):
            if element and element[0] == key:
                return self.array[hashKey][index][1]

    def deleteItem(self, key):
        hashKey = self.generateHashKey(key)
        for index, element in enumerate(self.array[hashKey]):
            if element and element[0] == key:
                self.array[hashKey].pop(index)

    def getAverageTemperatureBetweenDays(self, month, firstDay, lastDay):
        if firstDay > lastDay:
            return ('First day should be lesser than last day')

        avgTemp = 0
        days = 0
        for day in range(firstDay, lastDay + 1):
            key = str(month) + ' ' + str(day)
            avgTemp += self.getItem(key)
            days += 1

        return avgTemp / days if days != 0 else 0

    def getMaxTemperatureBetweenDays(self, month, firstDay, lastDay):
        if firstDay > lastDay:
            return ('First day should be lesser than last day')

        maxTemp = 0
        for day in range(firstDay, lastDay + 1):
            key = str(month) + ' ' + str(day)
            maxTemp = self.getItem(key) if self.getItem(
                key) > maxTemp else maxTemp

        return maxTemp

    def bulkInsertTemperatureByMonthAndDays(self, month, days=30, temperatures=[]):
        if days != len(temperatures):
            return ('Number of days and temperatures are not equal')

        for day in range(days):
            key = str(month) + ' ' + str(day + 1)
            self.setItem(key, temperatures[day])


report = WeatherReport()

report.bulkInsertTemperatureByMonthAndDays('jan', 10, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
print(report.getItem('jan 1'))
report.setItem('jan 11', 32)
print(report.getAverageTemperatureBetweenDays('jan', 1, 10))
print(report.getMaxTemperatureBetweenDays('jan', 7, 5))
