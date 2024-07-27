from collections import *


# password validation function
# password must contain alpha upper or lowe 26 chars and 3 int and 1 special char
def validate(string):
    if len(string) < 10:
        return 'Atleast Length should be 10.'
    if len(string) > 16:
        return 'Password size should be 16 or less than 16 characters.'
    lower, specials = set([i for i in 'abcdefghijklmnopqrstuvwxyz']), set([i for i in '"!@#$%^&*(){}|?><.,+=~"'])
    numbers, upper = set([str(i) for i in range(0, 10)]), set([i.upper() for i in 'abcdefghijklmnopqrstuvwxyz'])
    table = defaultdict(int)
    for i in string:
        if i in numbers:
            table['no'] += 1
        elif i in lower or i in upper:
            table['char'] += 1
        else:
            if i in specials:
                table['special'] += 1
    if table['no'] < 1:
        return 'Atleast 1 digit is required.'
    if table['char'] < 8:
        return 'Atleast 8 character is required.'
    if table['special'] < 1:
        return 'Atleast 1 Special character is required.'
    return 'Valid'
