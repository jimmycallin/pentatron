from resources import nst
import lexicon
import pandas as pd
from random import random
from joblib import Memory
from collections import Counter

memory = Memory("/tmp/", verbose=1)

@memory.cache
def load_headlines():
    df = pd.read_json("./resources/headlines.json", lines=True)
    df["title"] = df._source.apply(lambda x: x["search"]["title"])
    return df["title"].tolist()


# next time!
# it seems like it actually can find iambic pentametres now
# unfortunately it's too strict
# function words should count as both
# also relax the syllable length a bit


def is_iambic_pentametre(lex, transcribed_sentence):
    syllables = lexicon.get_syllables(lex, transcribed_sentence)
    if len(syllables) > 12 or len(syllables) < 9:
        return False
    last_was_stressed = None
    for syllable in syllables:
        if last_was_stressed is None:
            last_was_stressed = lexicon.is_stressed_syllable(syllable)
            continue
        elif last_was_stressed and (lexicon.is_unstressable(syllable) or not lexicon.is_stressed_syllable(syllable)):
            last_was_stressed = False
            continue
        elif not last_was_stressed and (lexicon.is_unstressable(syllable) or lexicon.is_stressed_syllable(syllable)):
            last_was_stressed = True
            continue
        else:
            return False
    return True



def headlines_rhyme(lex, headlines):
    missing_words = Counter()
    for title1 in sorted(headlines, key=lambda k: random()):
        transcribed1 = lexicon.transcribe_sentence(lex, title1)
        if "UNK" in transcribed1:
            for t, w in zip(lexicon.tokenize(title1), transcribed1.split(" ")):
                if w == "UNK":
                    missing_words[t] += 1
            continue
        if not is_iambic_pentametre(lex, title1):
            continue
        for title2 in sorted(headlines, key=lambda k: random()):
            if title1 == title2:
                continue
            transcribed2 = lexicon.transcribe_sentence(lex, title2)
            if "UNK" in transcribed2:
                continue
            if not is_iambic_pentametre(lex, title2):
                continue
            if lexicon.is_rhyming_sentences(lex, title1, title2):
                print(title1.replace("\n", " "))
                print(title2.replace("\n", " "))
                print()
                break
    print("MISSING", str(missing_words.most_common(40)))


if __name__ == "__main__":
    lex = nst.load_lexicon(nst.nst_path)
    headlines_rhyme(lex, load_headlines())
