def ubbi_dubbi(_input: str) -> str:
    """Insert 'ub' after each syllable onset.
    "Hello" -> "hubellubo"
    """
    result = []
    vowels = "aeiou"
    for l in _input:
        if l in vowels:
            result.append('ub' + l)
            continue
        result.append(l)
    return ''.join(result)
