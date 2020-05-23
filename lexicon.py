import re

from resources import nst

DIPHTONGS = ["a*U", "E*U"]

STOPS = ["p", "b", "t", "t`", "d", "d`", "k", "g"]

NASALS = ["m", "N", "n", "n`"]

FRICATIVES = ["f", "v", "s’", "s`", "s", "x", "h"]


APPROX = ["r", "l", "l`", "j"]

VOWELS = [
    "i:",
    "I",
    "u0",
    "}:",
    "a",
    "A:",
    "u:",
    "U",
    "E:",
    "E",
    "y:",
    "Y",
    "e:",
    "e",
    "2:",
    "9",
    "o:",
    "O",
    "@",
] + DIPHTONGS

CONSONANTS = STOPS + NASALS + FRICATIVES + APPROX

SYLLABLE_SEPARATOR = "$"


def tokenize(s):
    return re.findall(r"[\w\d]+", s.replace("\\n", "").lower())


### TRANSCRIPTION


def transcribe_word(lex, w):
    try:
        return lex.at[w, "trans_1"]
    except KeyError:
        return "UNK"


def transcribe_sentence(lex, s):
    return " ".join([transcribe_word(lex, w) for w in tokenize(s)])


### SYLLABLE


def get_syllables(lex, s):
    return re.split(r"[\s$]", transcribe_sentence(lex, s))


def count_syllables(lex, s):
    return len(get_syllables(lex, s))


def is_unstressable(syl):
    return syl.startswith("?")


def is_stressed_syllable(syl):
    return syl.startswith('"') or syl.startswith("%") or syl.startswith("?")


def get_stressed_syllable_idx(syllables):
    return [i for i, syl in enumerate(syllables) if is_stressed_syllable(syl)][-1]


def get_onset(syl):
    # all consonants up to nucleus
    nucleus = get_nucleus(syl)
    return syl[: syl.find(nucleus)]


def get_nucleus(syl):
    # longest matching vowel / diphtong?
    matches = []
    for v in VOWELS:
        if v in syl:
            matches.append(v)
    # returns longest string
    return max([[i, x] for i, x in enumerate(matches)], key=lambda x: x[1])[1]


def get_coda(syl):
    # everything after nucleus
    nucleus = get_nucleus(syl)
    return syl[syl.find(nucleus) + len(nucleus) :]


def get_rime(syl):
    return get_nucleus(syl) + get_coda(syl)


### RHYMING


def is_rhyme(lex, w1, w2):
    w1_syl = get_syllables(lex, w1)
    w2_syl = get_syllables(lex, w2)
    if w1_syl[0] == "UNK" or w2_syl[0] == "UNK":
        return False
    w1_stress = w1_syl[get_stressed_syllable_idx(w1_syl) :]
    w2_stress = w2_syl[get_stressed_syllable_idx(w2_syl) :]
    if "".join(w1_stress).lstrip('"').lstrip("%") == "".join(w2_stress).lstrip(
        '"'
    ).lstrip("%"):
        return False
    return [get_rime(w1_stress[0])] + w1_stress[1:] == [
        get_rime(w2_stress[0])
    ] + w2_stress[1:]


def is_rhyming_sentences(lex, s1, s2):
    ws1 = tokenize(s1)
    ws2 = tokenize(s2)
    if is_rhyme(lex, ws1[-1], ws2[-1]):
        return True


### PROSE


def is_iambic_pentametre(lex, transcribed_sentence):
    syllables = get_syllables(lex, transcribed_sentence)
    if len(syllables) > 13 or len(syllables) < 6:
        return False
    last_was_stressed = None
    for syllable in syllables:
        if last_was_stressed is None:
            last_was_stressed = is_stressed_syllable(syllable)
            continue
        elif last_was_stressed and (
            is_unstressable(syllable) or not is_stressed_syllable(syllable)
        ):
            last_was_stressed = False
            continue
        elif not last_was_stressed and (
            is_unstressable(syllable) or is_stressed_syllable(syllable)
        ):
            last_was_stressed = True
            continue
        else:
            return False
    return True
