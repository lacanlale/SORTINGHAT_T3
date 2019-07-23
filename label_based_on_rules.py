from pandas.api.types import infer_dtype
import pandas as pd
import numpy as np
import re


def is_url(row, reg):
    samples = row[6:]
    for sample in samples:
        if reg.match(str(sample)):
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


def is_list(row, reg):
    samples = row[6:]
    for sample in samples:
        if reg.match(str(sample).lower()):
            return True
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

    
df = pd.read_csv("data/needs_extraction_data/date_and_time_combined.csv")
identifiers = df[['num_nans', '%_nans', 'mean_word_count',
       'std_dev_word_count', 'has_delimiters', 'sample_1', 'sample_2',
       'sample_3', 'sample_4', 'sample_5']].rename(columns={'%_nans' : 'perc_nans'}).fillna('NANVAL!')

rulebook_preds = []

url_pat = r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"
url_reg = re.compile(url_pat)

list_pat =  r"((.?)+[,>;:\-~`\.\|\*\_]\s+(.?)+){2,}"
list_reg = re.compile(list_pat)

num_pat = r"([\$|\w]?(\d|\d\.\d|\d\,\d)+\s?[\$|\w]?)"
num_reg = re.compile(num_pat)

email_pat = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b"
email_reg = re.compile(email_pat)

for row in identifiers.itertuples():
    if float(row.perc_nans) > 0.90:
        # print('UNUSABLE')
        rulebook_preds.append('Unusable')
        continue
    elif is_url(row, url_reg):
        # print('URL')
        rulebook_preds.append('URL')
        continue
    elif is_datetime(row):
        # print('DATETIME')
        rulebook_preds.append('Datetime')
        continue
    elif row.has_delimiters == 'True':
        if is_list(row, list_reg):
            # print('LIST')
            rulebook_preds.append('List', list_reg)
            continue
        else:
            rulebook_preds.append('')
    elif is_email(row, email_reg):
        # print('CUSTOM OBJECT')
        rulebook_preds.append('Custom Object')
        continue
    elif row.mean_word_count < 2.0:
        if is_num(row, num_reg):
            # print('NUMBERS')
            rulebook_preds.append('Numbers')
            continue
        else:
            rulebook_preds.append('')
    else:
        # Unable to identify, do NOT fill in y_act
        # print('DEFAULT')
        rulebook_preds.append('')

df['y_pred'] = rulebook_preds 
df.to_csv('data/needs_extraction_data/rulebook_labelled.csv', index=False)