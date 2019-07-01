from resources import nst
import lexicon
import pandas as pd


def load_headlines():
    df = pd.read_json("./resouces/headlines.json", lines=True)
    df['title'] = df._source.apply(lambda x: x['search']['title'])
    return df['title']


def is_iambic_pentametre():
    return True

lex = nst.load_lexicon(nst.nst_path)


def headlines_rhyme(lex, headlines):
    for title1 in headlines:
        if "UNK" in lexicon.transcribe_sentence(lex, title1) or lexicon.count_syllables(lex, title1) > 8:
            continue
        if not is_iambic_pentametre(lexicon.transcribe_sentence(lex, title1)):
            continue
        for title2 in headlines:
            if title1 == title2:
                continue
            if "UNK" in lexicon.transcribe_sentence(lex, title2) or lexicon.count_syllables(lex, title2) > 10:
                continue
            if not is_iambic_pentametre(lexicon.transcribe_sentence(lex, title2)):
                continue
            if lexicon.is_rhyming_sentences(lex, title1, title2):
                print(title1.replace("\n", " "))
                print(title2.replace("\n", " "))
                print()
                break

if __name__ == "__main__":
    headlines_rhyme(lex, load_headlines().tolist())
