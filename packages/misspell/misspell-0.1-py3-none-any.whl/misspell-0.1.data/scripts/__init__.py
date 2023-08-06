#!python

from random import choice as random_choice, randint

NEIGHBORS = {
    'a': 'qwszx',
    'b': 'vghn',
    'c': 'xdfv',
    'd': 'wersfxcv',
    'e': '2345wrsdf',
    'f': 'ertdgcvb',
    'g': 'rtyfhvbn',
    'h': 'tyugjbnm',
    'i': '789uojkl',
    'j': 'yuihknm,',
    'k': 'uiojlm,.',
    'l': 'iopk,.',
    'm': 'jkn,',
    'n': 'bhjm',
    'o': '890-ipkl',
    'p': "0-o[l'",
    'q': '`12was',
    'r': '345etdfg',
    's': 'qweadzxc',
    't': '456ryfgh',
    'u': '78yihjk',
    'v': 'cfgb',
    'w': '123qeasd',
    'x': 'zasdc',
    'y': '67tughj',
    'z': 'asx',
    '-': '0=p[',
    '.': 'l',
}

NEIGHBORS_UNICODE = {
    'a': 'á',
    'c': 'č',
    'd': 'ď',
    'e': 'ěé',
    'i': 'íǐ',
    'n': 'ňń',
    'o': 'óǒ',
    'r': 'řŕ',
    's': 'šś',
    't': 'ť',
    'u': 'ǔú',
    'v': 'ǘǚ',
    'y': 'ý',
    'z': 'žź',
    'ě': 'qwe',
    'š': 'wer',
    'č': 'ert',
    'ř': 'rty',
    'ž': 'tyu',
    'ź': 'tyu',
    'ý': 'yzui',
    'ž': 'tyzu',
    'á': 'uio',
    'í': 'iop',
}

def make_typo(string: str, unicode: bool=False) -> str:
    string = str(string)
    if not string:
        return ''

    if all([c.lower() not in NEIGHBORS for c in string]):
        if not unicode:
            return string
        if all([c.lower() not in NEIGHBORS_UNICODE for c in string]):
            return string

    choices = NEIGHBORS
    if unicode:
        for key in NEIGHBORS_UNICODE:
            if key in choices:
                choices[key] += NEIGHBORS_UNICODE.get(key, '')
            else:
                choices[key] = NEIGHBORS_UNICODE.get(key, '')

    while True:
        index = randint(0, max(0, len(string) - 1))
        random_char = string[index]
        char_lower = random_char.lower()

        if char_lower in NEIGHBORS or unicode and char_lower in NEIGHBORS_UNICODE:
            break

    ret = list(string)
    if random_char != char_lower:
        ret[index] = ret[index].upper() # preserve case

    ret[index] = random_choice(choices[random_char.lower()])
    return ''.join(ret)

def make_typos(string: str, percent: (int, float)=5, unicode=False):
    num_of_typos = int(max(1, len(string) / 100 * percent))
    for num in range(0, num_of_typos):
        string = make_typo(string, unicode=unicode)
    return string

