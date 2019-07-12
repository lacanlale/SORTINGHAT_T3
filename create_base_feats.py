import pandas as pd
import numpy as np
import random
import re
import os

extraction_path = "data/needs_extraction_data/"
meta_path = "data/data_set/meta_data/meta_data.csv"
dataset_path = "data/data_set/dataset/"
r_id_csv = "record_ids.csv"
needs_extraction_csv = "needs_extraction.csv"

meta_df = pd.read_csv(f"{meta_path}")

def get_csv(r_id):
    return meta_df.loc[meta_df.Record_id == r_id].name.iloc[0]


def get_attrs(r_id):
    return r_id_df.loc[r_id_df.Record_id == r_id].Attribute_names.iloc[0].split(', ')


def get_mean_word_count(df):
    totals = []
    for value in df:
        totals.append(len(str(value).split(' ')))
    return np.mean(totals)


def get_std_dev_word_count(df):
    totals = []
    for value in df:
        totals.append(len(str(value).split(' ')))
    return np.std(totals)


def check_delim(df):
    regex = r'([\w\d](:|,|;|\/|-|~|\||_)[\w\d])+'
    pattern = re.compile(regex)
    for entry in df:
        if pattern.match(str(entry)):
            return True
    return False


def get_rand_samples(df):
    return random.sample(list(df), 5)


def get_sig_vals(df, attr, r_id):
    df_len = len(df) # Total vals
    nan_total = len(df) - df[attr].count() # Total NaN's
    perc_nan = nan_total/len(df) # % of NaN's
    mean_word_count = get_mean_word_count(df[attr]) # mean_word_count
    std_dev_word_count = get_std_dev_word_count(df[attr]) # std_dev_word_count
    has_delim = check_delim(df[attr]) # has_delimeters
    samples = get_rand_samples(df[attr])
    print('---------------------------')
    print('# of items | NaN Total | Percentage of NaN\'s | Mean word count | Stdev word count | Has delim')
    print('---------------------------')
    print(f'  {df_len}  |  {nan_total}  |  {perc_nan}  |  {mean_word_count}  |  {std_dev_word_count}  |  {has_delim}')

    count = 1
    for item in samples:
        print(f"Sample {count}.) {item}")
        count += 1
    print('---------------------------')
    print()
    vals = [r_id, attr, '', '', '', df_len, nan_total, perc_nan, mean_word_count, std_dev_word_count, has_delim] # Record_id, Attribute_name, y_pred
    vals += samples
    return vals


def update_records_csv(labelled):
    for r_id in labelled:
        r_id_df.loc[r_id_df.Record_id == r_id, ['Labelled']] = True
    
    r_id_df.to_csv("data/needs_extraction_data/record_ids.csv", index=False)

r_id_df = pd.read_csv(f"{extraction_path}{r_id_csv}")
r_ids = r_id_df.loc[r_id_df['Labelled'] == False].Record_id
labelled_records = []
row = np.where(r_id_df['Labelled'] == False)[0][0] 

if not os.path.exists(f"{extraction_path}labelled_data.csv"):
    labelled_df = pd.DataFrame(columns=['Record_id', 'Attribute_name', 'y_pred', 'y_act', 'Reason', 'total_vals', 'num_nans','%_nans', 'mean_word_count', 'std_dev_word_count', 'has_delimeters', 'sample_1', 'sample_2', 'sample_3', 'sample_4', 'sample_5'])
else:
    print("!! WARNING !!]")
    labelled_df = pd.read_csv(f"{extraction_path}labelled_data.csv")

for r_id in r_ids:
    print("\n===========================\n")

    attrs = get_attrs(r_id)
    csv_name = get_csv(r_id)
    print(f"!!Now labelling item {r_id} @ {csv_name}!!")

    try:
        df = pd.read_csv(f"{dataset_path}{csv_name}", encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(f"{dataset_path}{csv_name}", encoding='ISO-8859-1')

    for attr in attrs:
        print(f"-- Attribute: {attr} --")
        vals = get_sig_vals(df, attr, r_id)
        labelled_df.loc[row] = vals
        row += 1
        print("\n===========================\n")

    labelled_records.append(r_id)

update_records_csv(labelled_records)
labelled_df.to_csv('data/needs_extraction_data/labelled_data.csv', index=False)
print("\n!! ENDING SESSION !!")
