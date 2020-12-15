def pig_latin(_input: str) -> str:
    """Takes a string as input, assumed to be an English word.
    1. For words that begin with consonant sounds, all letters before the
    initial vowel are placed at the end of the word sequence.
    2. When words begin with consonant clusters (multiple consonants that
    form one sound), the whole sound is added to the end when speaking or
    writing.
    3. For words that begin with vowel sounds, the vowel is left alone,
    and most commonly 'yay' is added to the end.
    Returns the translation of this word into Pig Latin.
    """
    words = []
    suffix_vowel = "way"
    suffix_consonant = "ay"
    vowels = "aeiou"
    for word in _input.lower().split():
        if word[0] in vowels:
            words.append(word + suffix_vowel)
        else:
            result = word[1:] + word[0] + suffix_consonant
            words.append(result)
    return " ".join(words)
