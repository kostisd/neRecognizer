import config
import numpy as np
import pandas as pd
from os import path
from os.path import exists
import re

def clean_string(text):
    # think about keeping dots etc
    text = re.sub(',', ' ', str(text))
    text = re.sub(' +', ' ', (str(text))).lower().strip()
    return text

def filter_entities(data, ent_min_n):
    # Filter out all entities below our set threshold (3)
    filtered_data = data[data['type'].map(data['type'].value_counts()) >= ent_min_n]
    # Get info about removed entities, if any
    removed_data = data[data['type'].map(data['type'].value_counts()) < ent_min_n]
    removed_entities_list = list(removed_data['type'].value_counts().index)
    print(f"Removed Entities: {len(removed_entities_list)}")
    if len(removed_entities_list) > 0:
        print(removed_entities_list)
    return filtered_data

def make_dictionaries(data):
    # now save the remaining entities to a list to iterate over them and get the strings
    entities_list = list(data['type'].value_counts().index)

    # Create the dictionaries as we go. We only need to iterate once over the entities
    for ent in entities_list:
        subset = data[data['type'] == ent]
        text_list = subset['string'].values
        text_list = np.unique(text_list) # let's not forget to sort uniq the dictionaries
        with open(path.join("dictionaries/", ent), "w") as dict:
            # let's not forget to sort + uniq the strings list
            for text in sorted(set(list(text_list))):
                dict.write("%s\n" % text)
            print(" Added Dictionary %s" % ent)
    return 0

def prep_dev_data():
    devset_tsv = "data/dev_data.tsv"
    if exists(devset_tsv):
        print("Dev Set file already exists - Using that")
        devset_df = pd.read_csv(devset_tsv, sep='\t', header=0)

    else:
        print("Preprocessing the dev set.. ", end='', flush=True)
        original_dev_data = pd.read_csv(config.original_dev_tsv, sep='\t', header=0)
        original_dev_data = original_dev_data.head(200)

        devset = []
        sentence = ""

        for index, line in original_dev_data.iterrows():
            word = str(line['word']).strip()
            id = str(line['id']).strip()
            pos = str(line['part_of_speech']).strip()
            if pos == ".":
                sentence = clean_string(sentence)
                devset.append([id, sentence])
                sentence = ""
            else:
                not_empty = True if re.search('[a-zA-Z0-9]', word) else False
                if pos != "-NONE-" and not_empty:
                    sentence += (" " + word)

        devset_df = pd.DataFrame(devset, columns = ['id', 'sentence'])
        devset_df.to_csv(devset_tsv, sep='\t')
        print("Done")
    return devset_df