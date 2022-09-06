import numpy as np
from os import path
import re

def clean_string(text):
    # think about keeping dots etc
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', str(text)) # str() because some NA string was causing a type error.
    text = re.sub(' +', ' ', (text)).lower().strip()
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

def prep_dev_data(read_dev_data):
    sentence_list = []
    sentence = ""
    count = 0
    for index, line in read_dev_data.iterrows():
        word = str(line['word'])
        if word.strip() == ".":
            sentence_list.append(sentence)
            count += 1
            sentence = ""
        else:
            not_empty = True if re.search('[a-zA-Z0-9]', word) else False
            if "*" not in word and not_empty:
                sentence += (" " + word)
        if count > 10:
            break
    return sentence_list