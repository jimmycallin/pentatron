import csv
import logging
import pandas as pd

logger = logging.getLogger(__name__)

nst_path = "resources/nst/swe030224NST.pron"

def read_lexicon(path):
    """
    Returns NST lexicon as a {'orthography': 'transcription'}.
    """
    logger.info("Reading NST lexicon from {}".format(path))
    columns = {0: 'orthography', 11: 'transcription'}
    df = pd.read_csv(path, sep=';', header=None, quoting=csv.QUOTE_NONE)
    df.rename(columns=columns, inplace=True)
    return df[['orthography', 'transcription']].set_index('orthography').to_dict()

if __name__ == '__main__':
    print(read_lexicon(nst_path))
