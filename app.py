from lexicon import tokenize
from resources import nst
import lexicon
import pandas as pd
from random import random
from joblib import Memory
from collections import Counter, defaultdict
from typing import Sequence, Mapping, Set

memory = Memory("/tmp/", verbose=1)


@memory.cache
def load_headlines():
    df = pd.read_json("./resources/headlines.json", lines=True)
    df["title"] = df._source.apply(lambda x: x["search"]["title"].replace("\n", " "))
    return df["title"].tolist()


def print_pairs(pair1, pair2):
    print(pair1[0])
    print(pair2[0])
    print(pair1[1])
    print(pair2[1])


def index_iambic_headlines(lex, headlines) -> Mapping[str, Set[str]]:
    headline_index = defaultdict(set)
    total = 0
    for title in sorted(headlines, key=lambda k: random()):
        if not lexicon.is_iambic_pentametre(lex, title):
            continue
        rhyme_component = lexicon.get_rhyme_component_from_sentence(lex, title)
        print(f"added {title} to {rhyme_component}")
        total += 1
        headline_index[rhyme_component].add(title)
    print("total sentences", total)
    return headline_index


# NEXT TIME
# - keep working on the types
# - clean up
# - maybe figure out storing
# - the remove identical rhymes function could use some work



def pick_two(sentences: Sequence[str]) -> Sequence[str]:
    first = sentences[0]
    first_t = tokenize(first)[-1]
    second = None
    for s in sentences[1:]:
        if tokenize(s)[-1] != first_t:
            second = s
            break
    if second is None:
        raise KeyError("Couldn't find nonidentical hits")

    return first, second


def headlines_rhyme(lex, headlines):
    missing_words = Counter()
    pairs = []
    index = index_iambic_headlines(lex, headlines)
    last_rhyming_pair = None
    for rime, sentences in index.items():
        if len(sentences) <= 1:
            continue
        try:
            rhyme_pair = pick_two(list(sentences))    
            if last_rhyming_pair is not None:
                print("---PAIR FOUND---")
                print_pairs(rhyme_pair, last_rhyming_pair)
            last_rhyming_pair = rhyme_pair
        except KeyError:
            continue

    print("number of rimes", len(index.keys()))
    # print("index", index)
    # for title1 in sorted(headlines, key=lambda k: random()):
    # transcribed1 = lexicon.transcribe_sentence(lex, title1)
    # if "UNK" in transcribed1:
    #     for t, w in zip(lexicon.tokenize(title1), transcribed1.split(" ")):
    #         if w == "UNK":
    #             missing_words[t] += 1
    #     continue
    # if not lexicon.is_iambic_pentametre(lex, title1):
    #     continue
    # for title2 in sorted(headlines, key=lambda k: random()):
    #     if title1 == title2:
    #         continue
    #     transcribed2 = lexicon.transcribe_sentence(lex, title2)
    #     if "UNK" in transcribed2:
    #         continue
    #     if not lexicon.is_iambic_pentametre(lex, title2):
    #         continue
    #     if lexicon.is_rhyming_sentences(lex, title1, title2):
    #         print(title1.replace("\n", " "))
    #         print(title2.replace("\n", " "))
    #         print()
    #         pairs.append([title1, title2])
    #         if len(pairs) == 2:
    #             print("-----PAIRS FOUND--------")
    #             print_pairs(pairs[0], pairs[1])
    #             print()
    #             pairs = []
    #         break
    print("MISSING", str(missing_words.most_common(40)))


if __name__ == "__main__":
    lex = nst.load_lexicon(nst.nst_path)
    headlines_rhyme(lex, load_headlines())
