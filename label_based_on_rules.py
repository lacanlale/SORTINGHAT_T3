from pandas.api.types import infer_dtype
import pandas as pd
import numpy as np
import re


def is_url(row, reg, pat):
    samples = row[6:]
    for sample in samples:
        if reg.match(str(sample).strip()) and len(re.sub(pat, '', str(sample).strip())) == 0:
            return True
    return False


def is_datetime(row):
    samples = row[6:]
    for sample in samples:
        try:
            _ = pd.Timestamp(sample)
            return True
        except ValueError:
            try:
                _ = pd.Timestamp(int(sample))
                return True
            except ValueError:
                continue
    return False


def is_email(row, reg):
    samples = row[6:]
    for sample in samples:
        if reg.match(str(sample)):
            return True
    return False


def is_num(row, reg):
    samples = row[6:]
    for sample in samples:
        try:
            _ = float(str(sample))
            return True
        except ValueError:
            if reg.match(str(sample).lower()):
                return True
    return False

    
df = pd.read_csv("data/needs_extraction_data/labelled_data.csv")
identifiers = df[['num_nans', '%_nans', 'mean_word_count',
       'std_dev_word_count', 'has_delimiters', 'sample_1', 'sample_2',
       'sample_3', 'sample_4', 'sample_5']].rename(columns={'%_nans' : 'perc_nans'}).fillna('NANVAL!')

rulebook_preds = []

url_pat = r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
url_reg = re.compile(url_pat)

list_pat =  r"((\d|\w|\')+(,|>|;|:|\-|`\.|\||\*){1}\s?(\d|\w|\')+){2,}"
list_reg = re.compile(list_pat)

num_pat = r"([\$|\w]?(\d|\d\.\d|\d\,\d)+\s?[\$|\w]?)"
num_reg = re.compile(num_pat)

email_pat = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b"
email_reg = re.compile(email_pat)

for row in identifiers.itertuples():
    if float(row.perc_nans) >= 0.90:
        rulebook_preds.append('Custom Object')
    elif float(row.mean_word_count) <= 2.0:
        if is_datetime(row):
            rulebook_preds.append('Datetime')
        elif is_email(row, email_reg):
            rulebook_preds.append('Custom Object')
        elif is_url(row, url_reg, url_pat):
            rulebook_preds.append('URL')
        elif is_num(row, num_reg):
            rulebook_preds.append('Numbers')
        else:
            rulebook_preds.append('Custom Object')
    elif float(row.std_dev_word_count) < 10.0:
        if row.has_delimiters == True:
            rulebook_preds.append('List')
        else:
            rulebook_preds.append('Custom Object')
    else:
        rulebook_preds.append('Sentence')

df['y_pred'] = rulebook_preds 
df.to_csv('data/needs_extraction_data/rulebook_labelled.csv', index=False)