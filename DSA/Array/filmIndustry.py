class filmIndustry:
    def __init__(self):
        self.heros = ['spider man', 'thor',
                      'hulk', 'iron man', 'captain america']

    def getNumberOfHeroes(self):
        return len(self.heros)

    def addNewHero(self, name, position='last'):
        if position == 'last':
            self.heros.append(name)
        return self.heros

    def removeHero(self, name):
        self.heros.remove(name)
        return self.heros

    def addHeroAfterSomeone(self, hero, precedingHero):
        precedingHeroIndex = self.heros.index(precedingHero)
        self.heros.insert(precedingHeroIndex+1, hero)
        return self.heros

    def addHeroBeforeSomeone(self, hero, succeedingHero):
        succeedingHeroIndex = self.heros.index(succeedingHero)
        self.heros.insert(succeedingHeroIndex, hero)
        return self.heros

    def sortHeros(self):
        # Bubble sort algorithm
        n = len(self.heros)
        for i in range(n):
            for j in range(0, n - i - 1):
                # Compare adjacent elements and swap if needed
                if self.heros[j] > self.heros[j + 1]:
                    self.heros[j], self.heros[j +
                                              1] = self.heros[j + 1], self.heros[j]
        return self.heros

    def replaceHero(self, existingHeros, replacementHeros):
        existingHeroStartIndex = self.heros.index(existingHeros[0])
        existingHeroEndIndex = self.heros.index(existingHeros[-1])
        self.heros[existingHeroStartIndex:existingHeroEndIndex +
                   1] = replacementHeros
        return self.heros


hollywood = filmIndustry()
print(hollywood.getNumberOfHeroes())
print(hollywood.addNewHero('black panther'))
print(hollywood.removeHero('black panther'))
print(hollywood.addHeroAfterSomeone('black panther', 'hulk'))
print(hollywood.replaceHero(['thor', 'hulk'], ['doctor strange']))
print(hollywood.sortHeros())

# hollywood.heros[1:3] = ['doctor strange', 'Sachin', 'Rahul', 'Shyam']
