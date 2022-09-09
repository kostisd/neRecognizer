import config
import prep_data as prep
import recognizer as rcg
import scoring as scr
import pandas as pd
import os
import io
import sys
from sklearn.model_selection import train_test_split
import csv
import dummy


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

      print("Running Recognizer... ", end = '', flush=True)

      results_table = scr.make_table()

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
          # Cover for division by zero
          local_precision = round(local_tp / (local_tp + local_fp), 2) if (local_tp + local_fp) > 0 else "NA"
          local_recall = round(local_tp / (local_tp + local_fn), 2) if (local_tp + local_fn) > 0 else "NA"
          local_results = ["precision: ", local_precision, "recall: ", local_recall]
          local_counts = str("tp: " + str(local_tp) + ", fp: " + str(local_fp) + ", tn: " + str(local_tn) + ", fn: " + str(local_fn))
          local_results.append(local_counts)

          # with io.open('augmented_sentences.csv', 'a') as f:
          #     write = csv.writer(f)
          #     write.writerow("")
          #     write.writerow(local_results)
          #     write.writerow(ngram)
          #     write.writerow(entity)
          # f.close()
      #
      # print('Done')g
      #
      # precision = round(tp / (tp + fp), 2) if (tp + fp) > 0 else "NA"
      # recall = round(tp / (tp + fn), 2) if (tp + fn) > 0 else "NA"
      #
      # print("\n" + print_line)
      # print("  Results ")
      # print(print_line)
      # print("\nPrecision: ", precision)
      # print("Recall:    ", recall , "\n")

