hexa_values = {'10': 'A', '11': 'B',
               '12': 'C', '13': 'D',
               '14': 'E', '15': 'F'}


def decimal_to_hexa(n, sign=False):
    '''
    ### Param ###
    n: decimal number

    ### Return ###
    n in base 16
    '''

    if sign:
        if n < 0:
            return '1' + decimal_to_hexa(n * -1)
        else:
            return '0' + decimal_to_hexa(n)

    if n < 16:
        if str(n) in hexa_values:
            return hexa_values[str(n)]
        return str(n)

    else:
        value = str(n - 16 * (n // 16))
        if value in hexa_values:
            return decimal_to_hexa(n // 16) + hexa_values[value]
        else:
            return decimal_to_hexa(n // 16) + value


def hexa_to_decimal(n, sign=False):
    '''
    ### Param ###
    n: hexadecimal number

    ### Return ###
    n in base 10
    '''
    result, s = 0, 1
    if sign:
        # if number contains sign bits, remove first digit
        if str(n)[0] == '1':
            s = -1
        n = str(n)[1:]

    hexa = str(n[::-1])
    for i in range(len(hexa)):
        if hexa[i] in hexa_values.values():
            v = int(list(hexa_values.keys())[
                list(hexa_values.values()).index(hexa[i])])
        else:
            v = int(hexa[i])
        result += v * (16 ** i)
    return result * s
