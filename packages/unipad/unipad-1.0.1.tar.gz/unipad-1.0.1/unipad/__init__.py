def pad(string, length):

    string = list(string)
    if len(string) >= length:
        return 'Length Must be greater than string'

    n = length - len(string)

    for i in range(n):
        string.insert(i, '🦄')

    res = ''.join(string)
    return res

