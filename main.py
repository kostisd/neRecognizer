import config
import prep_data as prep
import recognizer as rcg
import scoring as scr
import pandas as pd
import os
import io
import sys
import csv

print_line = "------------"

if __name__ == '__main__':

    print("\n" + print_line + print_line)
    print("  Data Preprocessing")
    print(print_line + print_line)

    # Train Data Loading
    print("Reading train data... ", end = '', flush=True)
    original_train_data = pd.read_csv(config.train_tsv, sep='\t', header=0)
    print("Done")

    # Data Preparation
    train_data = original_train_data

    # Normalise utterances
    print("Preparing train set... ", end = '', flush=True)
    train_data[config.string_col] = train_data[config.string_col].apply(prep.clean_string)
    print("Done")
    # filter uncommon entities in train set
    train_data = prep.filter_entities(train_data, config.ent_min_n)

    # Prepare dev set
    devset = prep.prep_dev_data()

    if config.train:
      # extract entities to dictionaries from train set
      print("\n" + print_line)
      print("  Training")
      print(print_line)

      print("Preparing Dictionaries...\n")
      prep.make_dictionaries(train_data)

    if config.test:
      print("\n" + print_line)
      print("  Testing:   ")
      print(print_line)

      print("Running Recognizer... ", end = '\n', flush=True)

      # Initializing f/t positive and f/t negative values to store scores
      fp = tp = fn = tn = 0

      for index, line in devset.iterrows():
          id = str(line['id']).strip()
          sentence = str(line['sentence']).strip()
          rcg_output = rcg.recognizer([id, sentence])
          ngram = rcg_output[1]
          entity = rcg_output[2]

          local_fp, local_tp, local_fn, local_tn = scr.scoring(rcg_output, train_data)

          fp += local_fp
          tp += local_tp
          fn += local_fn
          tn += local_tn

          results = scr.accuracy(local_fp, local_tp, local_fn, local_tn)
          local_counts = ", tp: " + str(local_tp) + ", fp: " + str(local_fp) + ", tn: " \
                         + str(local_tn) + ", fn: " + str(local_fn)
          local_results = ["precision: ", results["precision"], "recall: ", results["recall"]]
          print(local_results, local_counts, "\n")

          with io.open('augmented_sentences.csv', 'a') as f:
              write = csv.writer(f)
              write.writerow("")
              write.writerow(local_results)
              write.writerow(ngram)
              write.writerow(entity)
          f.close()

      final_results = scr.accuracy(fp, tp, fn, tn)

      print("\n" + print_line)
      print("  Results ")
      print(print_line)
      print("\nPrecision: ", results["precision"])
      print("Recall:    ", results["recall"] , "\n")