import pandas as pd

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

def make_results_table():
    results_table = pd.DataFrame(columns=['string', 'span', 'type', 'hyp', 'result'])
    return results_table
