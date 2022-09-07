import pandas as pd
import re

def scoring(rcg_output, train_data, results_table):
    id = re.sub(r'^.*?@', '', rcg_output[0])
    ngram_list = rcg_output[1]
    entity_list = rcg_output[2]

    # dropna because many subtree_ids are missing
    train_data = train_data.dropna(subset = ['subtree_id'])
    train_data = train_data[train_data['subtree_id'].str.contains(id)]

   if train_data:
        for ngram, entity in zip(ngram_list, entity_list):
            
    else:
        return
    print("ID: " , id)
    print(train_data)



def calc_accuracy(matches, testset, results_table):
    corr = 0
    nomatch = 0
    for match, test in zip(matches, testset):
        nomatch += 1 if (match[1] == "NOMATCH") else 0
        corr += 1 if (match[1] == test[1]) else 0
        new_row = pd.DataFrame([{'string': match[0], 'span': len(match[0]), 'type': test[1], 'hyp': match[1],
                                 'result': (match[1] == test[1])}])
        results_table = pd.concat([results_table, new_row], axis=0, ignore_index=True)
    accuracy = corr / len(testset) * 100
    recall = corr / (corr + nomatch)
    return [accuracy, recall, results_table]

def make_table():
    table = pd.DataFrame(columns=['id', 'string', 'span', 'type', 'hyp', 'result'])
   # results_table = pd.DataFrame(columns=['string', 'span', 'type', 'hyp', 'result'])
    return table
