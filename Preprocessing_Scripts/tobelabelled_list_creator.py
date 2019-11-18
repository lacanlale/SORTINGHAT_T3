import pandas as pd
import numpy as np
import re
import os

# NOTE
# --------------------------------------------------------------------------------------
# Short python script file for compiling list of data that needs extraction
# After execution, two files will be made:
#       1. CSV that holds data collected from the data_for_labelling#.xlsx files [columns included]
#       2. CSV that holds Record_id's and Attribute_name's that needed extraction
# And one folder:
#       1. Holds copies of the data that requires extraction
# --------------------------------------------------------------------------------------

cond = "Usable with extraction"
beg = f"data/data_for_labelling"
end = ".xlsx"
extraction_path = "data/needs_extraction_data/"
meta_path = "data/data_set/meta_data/meta_data.csv"
dataset_path = "data/data_set/dataset/"
meta_df = pd.read_csv(f"{meta_path}")

del_pattern = r'((\d|\w|\')+(,|>|;|:|\-|`\.|\||\*){1}\s?(\d|\w|\')+){2,}'
del_reg = re.compile(del_pattern)


def get_csv(r_id):
    return meta_df.loc[meta_df.Record_id == r_id].name.iloc[0]


def get_vals(r_id, attr_name):
        csv_name = get_csv(r_id)
        path = f"{dataset_path}{csv_name}"
        print("Reading path: ", path)
        try:
                df = pd.read_csv(f"{dataset_path}{csv_name}", encoding='utf-8').dropna().drop_duplicates(subset=[attr_name])
        except UnicodeDecodeError:
                df = pd.read_csv(f"{dataset_path}{csv_name}", encoding='ISO-8859-1').dropna().drop_duplicates(subset=[attr_name])
        nan_total = len(df) - df[attr_name].count() # Total NaN's
        perc_nan = nan_total/len(df) # % of NaN's
        has_delim = False
        totals = []
        count = 0
        length = len(df)
        for value in df[attr_name]:
                count += 1
                totals.append(len(str(value).split(' '))) 
                if not has_delim and del_reg.match(str(value)):
                        has_delim = True
                print(f"\t - Processed {count}/{length} items || {'{0:.3g}'.format((count/length)*100)}% finished")

        vals = [np.mean(totals), np.std(totals), has_delim, nan_total, perc_nan]
        return vals



folder_path = "data/needs_extraction_data/"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Warn user that there is an already-existing file
if os.path.exists(f"{folder_path}record_ids.csv"):
        print("!! WARNING !!")
        print("A compiled list of record_id's and attributes already exists! Would you like to overwrite?")
        inp = input("(Y/n): ").lower()
        if inp == 'n':
                exit()
                
# Create CSV of 'Usable with extraction' data from data_for_labelling#.xlsx files
for x in range(0,10):
    path = f"{beg}{x}{end}"
    print(f"Finding [{cond}] items in file {path}")
    df = pd.read_excel(path)
    df_sub = df.loc[df.y_act == cond]
    if 'needs_extr' in locals():
            needs_extr = pd.concat([needs_extr, df_sub], axis=0)
    else:
        needs_extr = df_sub

needs_extr.drop(['% nans','Check','Unnamed: 2','Unnamed: 9','check','max_val','mean','min_val','Num of nans','num of dist_val','reason','Reason','std_dev','y_Arun','y_act','y_pred'], axis=1, inplace=True)

print()
r_ids = needs_extr[['Record_id', 'Attribute_name']]
sig_vals = {
        'mean_token_count' : [],
        'stdev_token_count' : [],
        'has_delims' : [],
        'num_nans' : [],
        '%_nans' : []
}
count = 0
length = len(needs_extr)
for row in r_ids.itertuples():
       r_id = row[1] 
       attr_name = row[2]
       count += 1
       print(f"Item {count}/{length} [Record_id: {r_id} || Attribute: {attr_name}]")
       vals = get_vals(r_id, attr_name)
       sig_vals['mean_token_count'].append(vals[0])
       sig_vals['stdev_token_count'].append(vals[1])
       sig_vals['has_delims'].append(vals[2])
       sig_vals['num_nans'].append(vals[3])
       sig_vals['%_nans'].append(vals[4])
        
needs_extr['%_nans'] = sig_vals['%_nans']
needs_extr['num_nans'] = sig_vals['num_nans']
needs_extr['has_delims'] = sig_vals['has_delims']
needs_extr['stdev_token_count'] = sig_vals['stdev_token_count']
needs_extr['mean_token_count'] = sig_vals['mean_token_count']
needs_extr.to_csv(f"{folder_path}/needs_extraction.csv", index=False)