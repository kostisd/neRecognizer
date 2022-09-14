import pandas as pd
import re

def scoring(rcg_output, train_data, dict_list):
    tp_dict, fp_dict, fn_dict = dict_list[0], dict_list[1], dict_list[2]
  #  tp_dict, fp_dict, fn_dict = [{'ORG': 0, 'GPE': 0, 'PERSON': 0, 'DATE': 0,
  #                                   'CARDINAL': 0, 'NORP': 0, 'MONEY': 0, 'PERCENT': 0,
  #                                   'ORDINAL': 0, 'LOC': 0, 'TIME': 0, 'WORK_OF_ART': 0,
  #                                   'QUANTITY': 0, 'FAC': 0, 'PRODUCT': 0, 'EVENT': 0,
  #                                   'LAW': 0, 'LANGUAGE': 0} for _ in range(3)]

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
    true_entity = ""

# We check every ngram against the id-based subset
    if not train_data.empty:
        for ngram, entity in zip(ngram_list, entity_list):
            true_entity = "NAN"
            str_list = train_data['string'].to_list()
            if ngram in str_list:
                true_entity = (train_data[train_data['string'] == ngram]['type'].to_string(index = False)).strip()
                #print("FOUND", entity, true_entity, ngram)
                if entity == "NOMATCH": # there is a true_entity for this str but we tagged it as NOMATCH
                  #  print("FN NOMATCH", entity, true_entity, ngram)
                    local_fn += 1
                    fn_dict[true_entity] += 1
                elif entity == true_entity:
                   # print("TP", entity, true_entity, ngram)
                    local_tp += 1
                    tp_dict[entity] += 1
                elif entity != true_entity:
                    #print("FP / FN", entity, true_entity, ngram)
                    local_fp += 1
                    local_fn += 1
                    fp_dict[entity] += 1
                    fn_dict[true_entity] += 1
            else: # if the ngram cannot be found in the true entities
                #print("NOT FOUND", entity, true_entity, ngram)
                if entity == "NOMATCH":
                    local_tn += 1 # we don't use this for scoring
                else:
                    #print("FP - NOT FOUND", entity, true_entity, ngram)
                    local_fp += 1 # we tagged a non-existing name/entity

    out_dicts = [fp_dict, tp_dict, fn_dict]

    return [local_fp, local_tp, local_fn, out_dicts]

def accuracy(fp, tp, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else False # a compromise to avoid "divide by zero" cases
    recall = tp / (tp + fn) if (tp + fn) > 0 else False

    results = {"precision": precision, "recall": recall}
    return results
