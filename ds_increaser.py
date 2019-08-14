import pandas as pd
import numpy as np
import re

# NOTE
# -----------------------------------------------------------------------------------------------------
# The following was written AUG12,2019 to help with increasing data set size and add potential features.
# User should know what columns they want labelled, which label to use, and which reason
# How it works:
#   1.) User enters name of file to look for
#   2.) User enters column names that should be labelled
#   3.) User enters label for the columns
#   4.) User enters reason (if necessary)
#   4.) Script reads the raw csv, takes the features, and updates labelled_data.csv
# This new data is added to a copy of the labelled_data.csv @ labelled_data_added_feat_and_size.csv
# -----------------------------------------------------------------------------------------------------

meta_path = "data/additional_data/meta/meta_data.csv"
dataset_path = "data/additional_data/ds"

del_pattern = r'((\d|\w|\')+(,|>|;|:|\-|`\.|\||\*){1}\s?(\d|\w|\')+){2,}'
del_reg = re.compile(del_pattern)

def get_act():
    print("Select a label")
    available_cats = ['Numbers', 'List', 'Datetime', 'Sentence', 'URL', 'Custom Object']
    count = 1
    choice = 0
    while not(choice >= 1 and choice <= 6):
        choice = 0
        for category in categories:
            print(f"{count}.) {category}")
            count += 1
        choice = int(input("Label #: "))
    return available_cats[choice-1]


def get_reason(label):
    reasons = {
        "c": "Follows standard numerical formatting seen in applications e.g. ‘12.22.16’, ‘1998/01/01’, ‘30-8-2002’",
        "d": "Uses a combination of strings and numbers to convey a date e.g. ‘December 1’, ‘October 30, 2019’, ‘The first of May’",
        "e": "Follows standard numerical formatting seen in applications e.g. ‘12:30', ‘1:30:20’, ‘15:00’",
        "f": "Uses a combination of strings and numbers to convey a time of day e.g. ‘Half past 12’, ‘12 PM’, ‘9 o’ clock in the morning’",
        "i": "Multiple numerical values whose context is unrelated to date or time and may require more contextual processing than other numbers e.g. '(-0.022, 2.2]', '(-5.0000, 33.0000)'",
        "j": "Phrases containing words that convey specific geographic information e.g. ‘address : 9415 Campus Point Dr’, ‘mailing address: 345 Airport Rd PO Box 1242 Malta’, ‘MT 59538’",
        "k": "Electronic identification data e.g. , ‘email : johndoe@website.com’, 'URL suffixes : /homebrew/recipe/view/246372/freo-pale-ale'",
        "l": "Descriptive data that should have been classified by an earlier step.",
        "m": "Total of NaN values is too high and/or sample items do not convey contextual background of what the data is"
    }
    if label == 'Numbers':
        return 'a'
    elif label == 'List':
        return 'b'
    elif label == 'Datetime':
        print("Select a reason")
        possible = ['c', 'd', 'e', 'f']
        while True:
            for choice in possible:
                print(f"{choice}.) {reasons[choice]}")
            opt = input("Reason: ")
            if opt in choice:
                return reasons[choice]
    elif label == 'Sentence':
        return 'g'
    elif label == 'URL':
        return 'h'
    else:
        print("Select a reason")
        possible = ['i', 'j', 'k', 'l', 'm']
        while True:
            for choice in possible:
                print(f"{choice}.) {reasons[choice]}")
            opt = input("Reason: ")
            if opt in choice:
                return reasons[choice]


def get_csv(r_id, meta_df):
    path_name = meta_df.loc[meta_df.Record_id == r_id].name.iloc[0]
    return pd.read_csv(f"{dataset_path}/{path_name}")


def get_vals(df):
    pass


def format_data(data, label, reason, samples, r_id, col_name):
    vals = [f"a{r_id}", col_name, '', label, reason] + data + samples
    return vals


labelled_df = pd.read_csv("data/needs_extraction_data/labelled_data_added_feat_and_size.csv")
meta_df = pd.read_csv(meta_path)

r_id = input("Enter record id: ")
label = get_act()
reason = get_reason(label)
df = get_csv(r_id, meta_df)
cols = input("Enter columns (no whitespace, comma-seperated format): ").split(',')
for col in cols:
    samples = get_rand_samples(df)
    sig_vals = get_vals(df)

    data = format_data(sig_vals, label, reason, samples, r_id, col)
    labelled_df.loc[len(labelled_df)] = data
labelled_df.to_csv("data/needs_extraction_data/labelled_data_added_feat_and_size.csv", index=False)