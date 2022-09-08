import pandas as pd
import re

def scoring(rcg_output, train_data):
    id = re.sub(r'^.*?@', '', rcg_output[0])
    ngram_list = rcg_output[1]
    entity_list = rcg_output[2]

    # local scores
    local_tp = 0 # true positive
    local_fp = 0 # false positive
    local_tn = 0 # true negative
    local_fn = 0 # false negative

    # dropna because many subtree_ids are missing
    train_data = train_data.dropna(subset = ['subtree_id'])
    train_data = train_data[train_data['subtree_id'].str.contains(id)]
    true_entity = "NOMATCH"
    # We check every ngram against the id-based subset
    if not train_data.empty:
        for ngram, entity in zip(ngram_list, entity_list):
            str_list = train_data['string'].to_list()
            if ngram in str_list:
                true_entity = (train_data[train_data['string'] == ngram]['type'].to_string(index = False)).strip()
                if entity == "NOMATCH":
                    local_fn += 1
                elif entity == true_entity:
                    local_tp += 1
                else:
                    local_fp += 1
            else:
                if entity == "NOMATCH":
                    local_tn += 1
                else:
                    local_fp += 1

    #print(tabulate([word_list, entity_list]))

    return [local_fp, local_tp, local_fn, local_tn]

def make_table():
    table = pd.DataFrame(columns=['id', 'string', 'span', 'type', 'hyp', 'result'])
   # results_table = pd.DataFrame(columns=['string', 'span', 'type', 'hyp', 'result'])
    return table
