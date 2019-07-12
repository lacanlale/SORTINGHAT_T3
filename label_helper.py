import pandas as pd
import numpy as np

def get_actual():
    categories = ['Numbers', 'List', 'Date', 'Timestamp', 'Sentence', 'URL', 'Custom Object', 'Unusuable']
    count = 1
    choice = 0
    while not(choice >= 1 and choice <= 8):
        choice = 0
        for category in categories:
            print(f"{count}.) {category}")
            count += 1
        choice = int(input("Reason #: "))
    return categories[choice-1]


def get_reason():
    reasons = {
        'a': 'Number value proceeded and/or preceded by a unit string, as well as possibly in-between e.g. ‘100 inches, ‘$15’, ‘-0.12 amps’, ‘~23 feet’, ‘US$ PER 100 LBS’, $5,000,000.00',
        'b': 'Text corpus that contains a delimiter that differs from standard date formats e.g ‘a,b,c’, ‘word 1; word 2; word 3’, ‘{men|clothing, women|clothing, children|toys etc}’',
        'c': 'Follows standard numerical formatting seen in applications e.g. ‘12.22.16’, ‘1998/01/01’, ‘30-8-2002’',
        'd': 'Uses a combination of strings and numbers to convey a date e.g. ‘December 1’, ‘October 30, 2019’, ‘The first of May’',
        'e': 'Follows standard numerical formatting seen in applications e.g. ‘12:30, ‘1:30:20’, ‘15:00’',
        'f': 'Uses a combination of strings and numbers to convey a time of day e.g. ‘Half past 12’, ‘12 PM’, ‘9 o’ clock in the morning’',
        'g': 'Text corpus that does not qualify as a date, timestamp, or URL and conveys significant contextual meaning based on the dataset (title, description, individual information, text excerpt, etc.). This text should also not represent a variable type that may be intended for computer processing e.g. ‘Do schools kill creativity?’, ‘SEE TEXT’, ‘statistics, computer science’',
        'h': 'Contains a protocol prefix and/or top-level domain suffix with possible additional categorical/product information e.g. ‘google.com’, ‘https://www.ucsd.edu/’, ‘https://www.researchgate.net/blog’',
        'i': 'Text corpus that may represent a variable type with the intention for computer process e.g. ‘{\'id\': 7, \'name\': \'Funny\', \'count\': 19645}’',
        'j': 'Multiple numerical values whose context is unrelated to date or time and may require more contextual processing than other numbers e.g. \'(-0.022, 2.2]\', \'(-5.0000, 33.0000)\'',
        'k': 'Phrases containing words that convey specific geographic information e.g. ‘address : 9415 Campus Point Dr’, ‘mailing address: 345 Airport Rd PO Box 1242 Malta’, ‘MT 59538’',
        'l': 'Electronic identification data e.g. , ‘email : johndoe@website.com’',
        'm': 'Descriptive data that should have been classified by an earlier step.',
        'n': 'Total of NaN values is too high and/or sample items do not convey contextual background of what the data is'
    }
    choice = 0
    while not choice:
        for key, value in reasons.items():
            print(f"{key}.) {value}")
        choice = input("Reason: ")
    return choice


df = pd.read_csv("data/needs_extraction_data/labelled_data.csv")
row = np.where(df.y_act.isnull())[0][0]
for num in range(row, len(df)):
    print("==============================")
    row_info = df.loc[num]
    for key, val in row_info.iteritems():
        print(f"{key}: {val}")
    print("==============================")

    y_act = get_actual()
    print()
    reason = get_reason()
    row_info.y_act = y_act
    row_info.Reason = reason

    df.loc[num] = row_info

    print("Would you like to continue? ")
    inp = input('(Y/n): ').lower()
    if inp == 'n':
        break

df.to_csv("data/needs_extraction_data/labelled_data.csv", index=False)
