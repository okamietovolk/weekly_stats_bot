def timeCong(number, time):
    numgroups = (0, 5, 6, 7, 8, 9), [1], (2, 3, 4)
    conjgs = {
            'minutes': ('минут', 'минуту', 'минуты'),
            'hours': ('часов', 'час', 'часа'),
            'seconds': ('секунд', 'секунда', 'секунды')
            }
    con = list(zip(numgroups, conjgs[time]))
    if int(repr(number)[-2]) == 1:
        return con[0][1]
    last_digit = int(repr(number)[-1])
    for group in con:
        if last_digit in group[0]:
            return group[1]



