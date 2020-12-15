def strsort(_input: str) -> str:
    """Sorts input string into unicode order
    'cba' => 'abc'
    """
    result = []
    for word in _input.split(" "):
        letters = [l for l in word]
        result.append("".join(sorted(letters)))
    return " ".join(result)
