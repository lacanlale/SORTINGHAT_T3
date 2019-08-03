import pandas as pd
import time 

# NOTE
# --------------------------------------------------------------------------------------
# The following was written to help preview sample data points per category
# alongside their respective attribute name and recoreded csv. This was written ~2 weeks
# after labelling and was made for taking note of examples and possibly odd data.
# --------------------------------------------------------------------------------------

def get_origin_csv(record_id):
    return meta_df.loc[meta_df.Record_id == record_id].name.iloc[0]

meta_df = pd.read_csv('data/meta_data.csv')
labelled_df = pd.read_csv('data/needs_extraction_data/labelled_data.csv')

vocab = ['Datetime', 'List', 'Numbers', 'Sentence', 'URL', 'Custom Object']
count = 1
index = -1
while not(index >= 1 and index <= len(vocab)):
    print('[Enter number of item to preview]')
    for cat in vocab:
        print(f'{count}.) {cat}')
        count += 1
    index = int(input('Option #: '))
    count = 0
pref = vocab[index-1]

labelled_cut = labelled_df.loc[labelled_df.y_act == pref][['Record_id', 'Attribute_name', 'sample_1', 'sample_2', 'sample_3', 'sample_4', 'sample_5']]
for tup in labelled_cut.itertuples():
    csv_name = get_origin_csv(tup.Record_id)
    print(f'{tup.Record_id}: {tup.Attribute_name} @ {csv_name}')
    print('- ', tup.sample_1)
    print('- ', tup.sample_2)
    print('- ', tup.sample_3)
    print('- ', tup.sample_4)
    print('- ', tup.sample_5)
    print()
    time.sleep(1)