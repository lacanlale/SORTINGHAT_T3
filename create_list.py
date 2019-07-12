import pandas as pd
import os

# Short python script file for compiling list of data that needs extraction
# After execution, two files will be made:
#       1. CSV that holds data collected from the data_for_labelling#.xlsx files [columns included]
#       2. CSV that holds Record_id's and Attribute_name's that needed extraction
# And one folder:
#       1. Holds copies of the data that requires extraction
cond = "Usable with extraction"
beg = f"data/data_for_labelling"
end = ".xlsx"

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

# Create CSV of Record_id's and Attribute_name's from needs_extraction csv
record_ids = needs_extr.Record_id.drop_duplicates()
record_dict = {}
for r_id in record_ids:
        record_dict[r_id] = []
        r_data = needs_extr.loc[needs_extr.Record_id == r_id]
        attr_names = r_data.Attribute_name
        for attr in attr_names:
                record_dict[r_id].append(attr)
        record_dict[r_id] = ', '.join(record_dict[r_id])

r_id_df = pd.Series(record_dict, name='Attribute_names')
r_id_df.index.name = 'Record_id'
r_id_df.reset_index()
r_id_df = pd.DataFrame({'Record_id':r_id_df.index, 'Attribute_names':r_id_df.values})
r_id_df['Labelled'] = False

needs_extr.to_csv(f"{folder_path}/needs_extraction.csv", index=False)
r_id_df.to_csv(f"{folder_path}/record_ids.csv", index=False)