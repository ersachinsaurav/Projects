monthlyExpenses = {
    'jan': 2200,
    'feb': 2350,
    'mar': 2600,
    'apr': 2130,
    'may': 2190
}


def getExpensesByMonth(targetMonth):
    return monthlyExpenses[targetMonth]


def getExpensesDifferenceBetweenTwoMonth(firstMonth, secondMonth):
    difference = monthlyExpenses[secondMonth] - monthlyExpenses[firstMonth]

    if difference >= 0:
        return f"+{difference}"
    else:
        return f"{difference}"


def getMonthlyExpensesSumTillMonth(targetMonth):

    totalExpenses = 0

    for month, amount in monthlyExpenses.items():
        totalExpenses += amount

        if month == targetMonth:
            break

    return totalExpenses


def addUpdateMonthlyExpenses(targetMonth, amount, type='deposit'):
    if targetMonth in monthlyExpenses:
        if type == 'expense':
            monthlyExpenses.update(
                {targetMonth: (monthlyExpenses[targetMonth] + amount)})
        else:
            monthlyExpenses.update(
                {targetMonth: (monthlyExpenses[targetMonth] - amount)})
    else:
        monthlyExpenses.update({targetMonth: amount})
    return monthlyExpenses


def getAnnualExpenses():
    return monthlyExpenses


def getMonthByExpenses(targetAmount):
    for month, amount in monthlyExpenses.items():
        if amount == targetAmount:
            return month
    return None


'''
    1. In Feb, how many dollars you spent extra compare to January?
    2. Find out your total expense in first quarter (first three months) of the year.
    3. Find out if you spent exactly 2000 dollars in any month
    4. June month just finished and your expense is 1980 dollar. Add this item to our monthly expense list
    5. You returned an item that you bought in a month of April and
    got a refund of 200$. Make a correction to your monthly expense list
    based on this
'''

print(getExpensesDifferenceBetweenTwoMonth('jan', 'feb'))
print(getMonthlyExpensesSumTillMonth('mar'))
print(getMonthByExpenses(2000))
print(addUpdateMonthlyExpenses('jun', 1980))
print(addUpdateMonthlyExpenses('apr', 200, 'deposit'))
