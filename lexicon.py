import re
from typing import List, Mapping, NewType, cast
from resources import nst

Word = str
Syllable = NewType("Syllable", str)
Sentence = List[Word]
Transcription = List[Syllable]

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


def tokenize(s: str) -> Sentence:
    return re.findall(r"[\w\d']+", s.replace("\\n", "").replace("'", "").lower())


### TRANSCRIPTION


def try_resolve_missing_word_transcription(lex, w: str) -> str:
    # can I find the same word without trailing r?
    if w.endswith("r"):
        try:
            return lex.at[w[:-1], "trans_1"] + "r"
        except KeyError:
            pass

    # can I find the same word without trailing d?
    if w.endswith("d"):
        try:
            return lex.at[w[:-1], "trans_1"] + "d"
        except KeyError:
            pass

    # can I find the same word without trailing s?
    if w.endswith("s"):
        try:
            return lex.at[w[:-1], "trans_1"] + "s"
        except KeyError:
            pass

    return "UNK"


def transcribe_word(lex, w: Word) -> str:
    try:
        return lex.at[w, "trans_1"]
    except KeyError:
        return try_resolve_missing_word_transcription(lex, w)


# def transcribe_sentence(lex, s: Sentence) -> List[Syllable]:
#     return " ".join([transcribe_word(lex, w) for w in tokenize(s)])


### SYLLABLE

flatten = lambda l: [item for sublist in l for item in sublist]


def get_syllables(lex, w: Word) -> Transcription:
    return cast(List[Syllable], re.split(r"[\s$]", transcribe_word(lex, w)))


def is_unstressable(syl: Syllable) -> bool:
    return syl.startswith("?")


def is_stressed_syllable(syl: Syllable) -> bool:
    return syl.startswith('"') or syl.startswith("%") or syl.startswith("?")


def get_stressed_syllable_idx(syllables: List[Syllable]) -> int:
    print("get_stresed_syllables_idx", syllables)
    return [i for i, syl in enumerate(syllables) if is_stressed_syllable(syl)][-1]


def get_nucleus(syl: Syllable) -> str:
    # longest matching vowel / diphtong?
    matches = []
    for v in VOWELS:
        if v in syl:
            matches.append(v)
    # returns longest string
    print("finding max in", syl)
    return max([[i, x] for i, x in enumerate(matches)], key=lambda x: len(x[1]))[1]


def get_onset(syl: Syllable) -> str:
    # all consonants up to nucleus
    nucleus = get_nucleus(syl)
    return syl[: syl.find(nucleus)]


def get_coda(syl: Syllable) -> str:
    # everything after nucleus
    nucleus = get_nucleus(syl)
    return syl[syl.find(nucleus) + len(nucleus) :]


def get_rime(syl: Syllable) -> str:
    return get_nucleus(syl) + get_coda(syl)


### RHYMING


def get_rhyme_component_from_sentence(lex, s: str) -> str:
    print("rhyme sentence", s)
    ws = tokenize(s)
    if len(ws) == 0:
        return "UNK"
    print("tokens", ws)
    last_word = ws[-1]
    syllables = get_syllables(lex, last_word)
    print("syllables", syllables)
    if len(syllables) == 1 and syllables[0] == "UNK":
        return "UNK"
    stress = syllables[get_stressed_syllable_idx(syllables) :]
    rime = get_rime(stress[0])
    return "".join([rime] + cast(List[str], stress[1:]))


# def is_rhyme(lex, w1, w2):
#     w1_syl = get_syllables(lex, w1)
#     w2_syl = get_syllables(lex, w2)
#     if w1_syl[0] == "UNK" or w2_syl[0] == "UNK":
#         return False
#     w1_stress = w1_syl[get_stressed_syllable_idx(w1_syl) :]
#     w2_stress = w2_syl[get_stressed_syllable_idx(w2_syl) :]
#     if "".join(w1_stress).lstrip('"').lstrip("%") == "".join(w2_stress).lstrip(
#         '"'
#     ).lstrip("%"):
#         return False
#     return [get_rime(w1_stress[0])] + w1_stress[1:] == [
#         get_rime(w2_stress[0])
#     ] + w2_stress[1:]


# def is_rhyming_sentences(lex, s1, s2):
#     ws1 = tokenize(s1)
#     ws2 = tokenize(s2)
#     if is_rhyme(lex, ws1[-1], ws2[-1]):
#         return True


### PROSE


def is_iambic_pentametre(lex, sentence: str):
    tokens = tokenize(sentence)
    syllables = flatten([get_syllables(lex, w) for w in tokens])
    if len(syllables) > 14 or len(syllables) < 6:
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
