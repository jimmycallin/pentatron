import csv
import sys
import pandas as pd
import re
import numpy as np
from joblib import Memory

memory = Memory("/tmp/", verbose=3)

nst_path = "resources/nst/swe030224NST.pron"

COLUMNS = [
    "orthography",
    "parts_of_speech",
    "morphology",
    "decomposition",
    "decomposition_pos",
    "source",
    "lang",
    "is_garbage",
    "domain",
    "is_acronym",
    "acronym_expansion",
    "trans_1",
    "trans_2",
    "trans_3",
    "trans_4",
    "trans_5",
    "trans_6",
    "trans_7",
    "trans_8",
    "trans_9",
    "trans_10",
    "trans_11",
    "trans_12",
    "trans_13",
    "trans_14",
    "trans_15",
    "trans_16",
    "trans_autogenerated",
    "set_id",
    "set_name",
    "stylistic_information",
    "inflector_role",
    "lemma",
    "inflection_rule",
    "morph_label",
    "compounder_code",
    "semantic_info",
    "disp_1",
    "disp_2",
    "disp_3",
    "disp_4",
    "disp_5",
    "disp_6",
    "disp_7",
    "disp_8",
    "disp_9",
    "frequency",
    "original_orthography",
    "comment_field",
    "update_info",
    "unique_id",
]


class _nst_dialect(csv.Dialect):
    """Describe the usual properties of Excel-generated CSV files."""

    delimiter = ";"
    doublequote = True
    skipinitialspace = False
    lineterminator = "\r\n"
    quoting = csv.QUOTE_NONE

def to_nst_format(transcriptions):
    nst_format = {}
    for orthography, transcription in transcriptions.items():
        arr = [float("NaN")] * 51
        arr[0] = orthography
        arr[3] = orthography
        arr[11] = transcription
        nst_format[orthography] = arr
    return nst_format
    
@memory.cache
def load_lexicon(path):
    """
    Returns NST lexicon as pandas.DataFrame.
    """
    print("Reading NST lexicon from {}".format(path))
    function_words = ["i", "att", "den", "det", "så", "och", "men", "för", "som", "då", "när", "min", "din", "vår", "han", "hon", "hans", "dess", "nog", "med", "kan", "hur", "var", "när", "vem"]
    missing = pd.DataFrame.from_dict(to_nst_format({
        "på": 'po:',
        "efter": 'Ef$ter',
        "av": 'A:v',
        "som": 'sOm',
        "den": 'dE:n',
        "det": 'de:t',
        "2018": '"tvo: "t}:$sen ""A:$t`On',
        "trump": 'tru0mp',
        "2019": '"tvo: "t}:$sen ""nI$tOn',
        "shl": '"Es "ho: "El',
        "flera": '""fle:$ra',
        "2017": '"tvo: "t}:$sen ""xu0$tOn',
        "10": '""ti:$U',
        "få": '"fo:',
        "5": '"fEm',
        "1": '"Et',
        "zlatan": '""fla:$tan',
        "bra": '"brA:',
        "7": '"x}:',
        "utanför": '""}:$tan$%f2:r',
        "sd": '"Es "dE',
        "än": '"E:n',
        "sveriges": '"svEr$jes',
        "trumps": 'tru0mp',
        "bort": '"bOt`',
        "mer": '"mEr',
        "löfven": 'l2:$"ve:n',
        "stort": '"stu:t`',
        "bakom": '""bA:%kOm',
        "2": '"tvo:',
        "6": '"sEks',
        "hittad": '""hI$tad',
        "kim": '"kIm',
        "15": '""fEm$tOn',
        "9": '""ni:$U',
        "8": '""O$ta',
        "20": '""s\'}:$gU',
        "3": '"tre:',
        "12": '"tOlv',
        "topptipset": '"tOp "tIp$set',
        "mest": '"mEst',
        "11": '""El$va',
        "v64": '"ve: sek$stI$U$""fy:$ra',
        "30": '""trE$tI',
        "4": '""fy:$ra',
        "många": '""mON$a'
    }), orient="index", columns=COLUMNS)
    df = pd.read_csv(
        path,
        encoding="utf-8",
        header=None,
        dialect=_nst_dialect,
        dtype={10: np.str_, 9: np.str_},
    )
    df.columns = COLUMNS
    df["orthography"] = df["orthography"].str.lower()
    for fw in function_words:
        fw_trans1 = df.loc[df.orthography == fw, "trans_1"]
        df.loc[df.orthography == fw, "trans_1"] = "?{}".format(fw_trans1)
    return df.append(missing, sort=True).drop_duplicates(subset="orthography").set_index("orthography").sort_index()