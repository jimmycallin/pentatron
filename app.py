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


def print_pairs(pair1, pair2):
    print(pair1[0])
    print(pair2[0])
    print(pair1[1])
    print(pair2[1])


def headlines_rhyme(lex, headlines):
    missing_words = Counter()
    pairs = []
    for title1 in sorted(headlines, key=lambda k: random()):
        transcribed1 = lexicon.transcribe_sentence(lex, title1)
        if "UNK" in transcribed1:
            for t, w in zip(lexicon.tokenize(title1), transcribed1.split(" ")):
                if w == "UNK":
                    missing_words[t] += 1
            continue
        if not lexicon.is_iambic_pentametre(lex, title1):
            continue
        for title2 in sorted(headlines, key=lambda k: random()):
            if title1 == title2:
                continue
            transcribed2 = lexicon.transcribe_sentence(lex, title2)
            if "UNK" in transcribed2:
                continue
            if not lexicon.is_iambic_pentametre(lex, title2):
                continue
            if lexicon.is_rhyming_sentences(lex, title1, title2):
                print(title1.replace("\n", " "))
                print(title2.replace("\n", " "))
                print()
                pairs.append([title1, title2])
                if len(pairs) == 2:
                    print("PAIRS FOUND")
                    print_pairs(pairs[0], pairs[1])
                    pairs = []
                break
    print("MISSING", str(missing_words.most_common(40)))


if __name__ == "__main__":
    lex = nst.load_lexicon(nst.nst_path)
    headlines_rhyme(lex, load_headlines())
