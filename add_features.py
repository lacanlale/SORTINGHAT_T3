import re
import pandas as pd
import numpy as np
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 


def get_csv(r_id):
    return meta_df.loc[meta_df.Record_id == r_id].name.values[0]
    

stop_words = set(stopwords.words('english'))
full_ds_path = "full_data_set/"

meta_df = pd.read_csv("meta_data.csv")
df = pd.read_csv(f"data/needs_extraction_data/labelled_added.csv")
items = df[['Record_id', 'Attribute_name']]

mean_char_vals = []
mean_whitespace_vals = []
mean_stopword_vals = []
mean_delim_vals = []

stdev_char_vals = []
stdev_whitespace_vals = []
stdev_stopword_vals = []
stdev_delim_vals = []

has_date_vals = []
has_url_vals = []
has_email_vals = []

url_pat = r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
url_reg = re.compile(url_pat)

delim_pat = r"(,|>|;|:|\-|\.|\||\*)"
delim_reg = re.compile(delim_pat)

email_pat = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b"
email_reg = re.compile(url_pat)
for _, item in items.iterrows():
    # chars = []
    # whitespaces = []
    # stopwords = []
    # delims_count = []

    r_id = item['Record_id']
    attr_name = item['Attribute_name']
    csv_name = get_csv(r_id)
    try:
        curr_df = pd.read_csv(f"{full_ds_path}{csv_name}")
    except:
        curr_df = pd.read_csv(f"{full_ds_path}{csv_name}", encoding="ISO-8859-1")
    print(f"{r_id} || {csv_name} || {attr_name}")
    col = curr_df[attr_name]
    # has_url = False
    # has_date = False
    has_email = True
    for item in col:
        if not (type(item) is str):
            item = str(item)
        # emails
        if (not has_email) and (email_reg.match(str(item).strip()) and len(re.sub(email_pat, '', str(item).strip())) == 0):
            has_email = True
        # # chars
        # chars.append(len(item))
        # # whitespaces
        # whitespaces.append(item.count(' '))
        # # stopwords
        # tokenized = word_tokenize(item)
        # stopwords.append(len([w for w in tokenized if not w in stop_words]))
        # # delimeters
        # delims_count.append(len(delim_reg.findall(item)))
        # # url
        # if (not has_url) and (url_reg.match(str(item).strip()) and len(re.sub(url_pat, '', str(item).strip())) == 0):
        #     has_url = True
        # # dates
        # if not has_date:
        #     try:
        #         _ = pd.Timestamp(item)
        #         has_date = True
        #     except ValueError:
        #         try:
        #             _ = pd.Timestamp(int(item))
        #             has_date = True
        #         except ValueError:
        #             continue

    # mean_char = np.mean(chars)
    # mean_whitespace = np.mean(whitespaces)
    # mean_stopwords = np.mean(stopwords)
    # mean_delims = np.mean(delims_count)
    # stdev_char = np.std(chars)
    # stdev_whitespace = np.std(whitespaces)
    # stdev_stopwords = np.std(stopwords)
    # stdev_delims = np.std(delims_count)

    # print("> mean char:", mean_char)
    # print("> mean whitespace:", mean_whitespace)
    # print("> mean stopwords:", mean_stopwords)
    # print("> mean delimeters:", mean_delims)
    # print("> stdev char:", stdev_char)
    # print("> stdev whitespace:", stdev_whitespace)
    # print("> stdev stopwords:", stdev_stopwords)
    # print("> stdev delimeters:", stdev_delims)

    # mean_char_vals.append(mean_char)
    # mean_whitespace_vals.append(mean_whitespace)
    # mean_stopword_vals.append(mean_stopwords)
    # mean_delim_vals.append(mean_delims)
    # stdev_char_vals.append(stdev_char)
    # stdev_whitespace_vals.append(stdev_whitespace)
    # stdev_stopword_vals.append(stdev_stopwords)
    # stdev_delim_vals.append(stdev_delims)
    # has_url_vals.append(has_url)
    # has_date_vals.append(has_date)
    has_email_vals.append(has_email)

# df['mean_stopword_total'] = mean_stopword_vals
# df['mean_whitespace_count'] = mean_whitespace_vals
# df['mean_char_count'] = mean_char_vals
# df['mean_delim_count'] = mean_delim_vals
# df['stdev_stopword_total'] = stdev_stopword_vals
# df['stdev_whitespace_count'] = stdev_whitespace_vals
# df['stdev_char_count'] = stdev_char_vals
# df['stdev_delim_count'] = stdev_delim_vals
# df['has_url'] = has_url_vals
# df['has_date'] = has_date_vals
df['has_email'] = has_email_vals

df.to_csv("labelled_added.csv", index=False)