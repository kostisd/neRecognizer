import pandas as pd
import re

def scoring(rcg_output, train_data, dict_list, top_ngrams):
    tp_dict, fp_dict, fn_dict = dict_list[0], dict_list[1], dict_list[2]
    id = re.sub(r'^.*?@', '', rcg_output[0])
    ngram_list = rcg_output[1]
    entity_list = rcg_output[2]

    # local scores
    local_tp = 0 # true positive
    local_fp = 0 # false positive
    local_fn = 0 # false negative
    local_tn = 0 # true negative - not used for scoring

    # dropna because many subtree_ids are missing
    train_data = train_data.dropna(subset = ['subtree_id'])
    train_data = train_data[train_data['subtree_id'].str.contains(id)]
    # true_entity = "NOMATCH"
    # true_entity = ""

# We check every ngram against the id-based subset
    if not train_data.empty:
        for ngram, entity in zip(ngram_list, entity_list):
            true_entity = "NAN"
            str_list = train_data['string'].to_list()
            if ngram in str_list:
                true_entity = (train_data[train_data['string'] == ngram]['type'].to_string(index = False)).strip()
                if entity == "NOMATCH": # there is a true_entity for this str but we tagged it as NOMATCH
                    local_fn += 1
                    fn_dict[true_entity] += 1
                elif entity == true_entity:
                    if ngram in top_ngrams.keys():
                        top_ngrams[ngram] += 1
                    else:
                        top_ngrams[ngram] = 1
                    local_tp += 1
                    tp_dict[entity] += 1
                elif entity != true_entity:
                    local_fp += 1
                    local_fn += 1
                    fp_dict[entity] += 1
                    if true_entity in fn_dict.keys():
                        fn_dict[true_entity] += 1
                    else:
                        print("Error: Could not find the true entity in the dictionary keys")
            else: # if the ngram cannot be found in the true entities
                if entity == "NOMATCH":
                    local_tn += 1 # we don't use this for scoring
                else:
                    local_fp += 1 # we tagged a non-existing name/entity

    out_dicts = [fp_dict, tp_dict, fn_dict]

    return [local_fp, local_tp, local_fn, out_dicts, top_ngrams]

def accuracy(fp, tp, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else False # a compromise to avoid "divide by zero" cases
    recall = tp / (tp + fn) if (tp + fn) > 0 else False

    results = {"precision": precision, "recall": recall}
    return results
