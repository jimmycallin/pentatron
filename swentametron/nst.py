import csv
import sys
import logging
import pandas as pd

logger = logging.getLogger(__name__)

nst_path = "resources/nst/swe030224NST.pron"

class Lexicon():
    def __init__(self, path):
        self.path = path
        self.lexicon = _load_resource(path)

    def transcribe(self, token):
        return self.lexicon.get(token, "UNKNOWN")

    def count_syllables(self, transcription):
        pass


def _load_resource(path):
    """
    Returns NST lexicon as a {'orthography': 'transcription'}.
    """
    logger.info("Reading NST lexicon from {}".format(path))
    columns = {0: 'orthography', 11: 'transcription'}
    df = pd.read_csv(path, sep=';', header=None, quoting=csv.QUOTE_NONE)
    df.rename(columns=columns, inplace=True)
    return df[['orthography', 'transcription']].set_index('orthography').to_dict()['transcription']



if __name__ == '__main__':
    tokens = [s.lower() for s in sys.argv[1:]]
    lexicon = Lexicon(nst_path)
    print(" ".join(map(lexicon.transcribe, tokens)))
