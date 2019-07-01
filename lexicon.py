import re

from resources import nst 

DIPHTONGS = ["a*U", "E*U"]

STOPS = ["p",
         "b",
         "t",
         "t`",
         "d",
         "d`",
         "k",
         "g"]

NASALS = ["m",
          "N",
          "n",
          "n`"]

FRICATIVES = ["f",
              "v",
              "s’",
              "s`",
              "s",
              "x",
              "h"]


APPROX = ["r",
          "l",
          "l`",
          "j"]

VOWELS = ["i:",
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
          "@"] + DIPHTONGS

CONSONANTS = STOPS + NASALS + FRICATIVES + APPROX

SYLLABLE_SEPARATOR = "$"

# lex = nst.load_lexicon()

### TRANSCRIPTION

def transcribe_word(lex, w):
  try:
    return lex.loc[w.lower()].iloc[0].trans_1
  except:
    return "UNK"

def transcribe_sentence(lex, s):
    return " ".join([transcribe_word(lex, w) for w in s.split(" ")])

### SYLLABLE

def get_syllables(lex, s):
    return re.split(r"[\s$]", transcribe_sentence(lex, s))

def count_syllables(lex, s):
    return len(get_syllables(lex, s))

def is_stressed_syllable(syl):
  return syl.startswith("\"") or syl.startswith("%")

def get_stressed_syllable_idx(syllables):
    return [i for i, syl in enumerate(syllables) if is_stressed_syllable(syl)][-1]

def get_onset(syl):
    # all consonants up to nucleus
    nucleus = get_nucleus(syl)
    return syl[:syl.find(nucleus)]

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
    return syl[syl.find(nucleus) + len(nucleus):]


def get_rime(syl):
    return get_nucleus(syl) + get_coda(syl)

### RHYMING

def is_rhyme(lex, w1, w2):
    w1_syl = get_syllables(lex, w1)
    w2_syl = get_syllables(lex, w2)
    if w1_syl[0] == "UNK" or w2_syl[0] == "UNK":
        return False
    w1_stress = w1_syl[get_stressed_syllable_idx(w1_syl):]
    w2_stress = w2_syl[get_stressed_syllable_idx(w2_syl):]
    if "".join(w1_stress).lstrip("\"").lstrip("%") == "".join(w2_stress).lstrip("\"").lstrip("%"):
        return False
    return [get_rime(w1_stress[0])] + w1_stress[1:] == [get_rime(w2_stress[0])] + w2_stress[1:]

def is_rhyming_sentences(lex, s1, s2):
    ws1 = s1.split(" ")
    ws2 = s2.split(" ")
    if is_rhyme(lex, ws1[-1], ws2[-1]):
        return True



### PROSE

def is_function_word(w):
  return False
  # PN KN DT PP

def get_syllable_stress(lex, syl, w):
  if is_function_word(w):
    return "both"
  elif is_stressed_syllable(syl):
    return "stressed"
  else:
    return "unstressed"

def is_iambic_pentameter(lex, s):
  syls = get_syllables(lex, s)
  # 1. get all syllables
  # 2. map all syllables to stressed/unstressed/both
  # 3. verify first syllable is unstressed/both
  # 4. make sure following is stressed/both
  # 5. and so on
  # 6. verify number of iambic feet are 5
  return syls

