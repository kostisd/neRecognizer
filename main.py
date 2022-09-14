import config
import prep_data as prep
import recognizer as rcg
import scoring as scr
import pandas as pd
from tabulate import tabulate
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

      # Create dictionaries to store scores per entity
      entities_list = list(train_data['type'].value_counts().index)
      fp_dict, tp_dict, fn_dict = ({} for i in range(3))

      for ent in entities_list:
          fp_dict[ent] = tp_dict[ent] = fn_dict[ent] = 0
      dict_list = [fp_dict, tp_dict, fn_dict]

      # Initializing false / true positive and negative values to store scores
      fp, tp, fn = [0] * 3

      devset = devset.head(10) # Comment to run full set!!
      for index, line in devset.iterrows():
          id = str(line['id']).strip()
          sentence = str(line['sentence']).strip()
          rcg_output = rcg.recognizer([id, sentence])
          word_list = rcg_output[1]
          entity_list = rcg_output[2]

          local_fp, local_tp, local_fn, out_dict_list = scr.scoring(rcg_output, train_data, dict_list)

          fp += local_fp
          tp += local_tp
          fn += local_fn

          #fp_dict, tp_dict, fn_dict = out_dict_list
          fp_dict = out_dict_list[0]
          tp_dict = out_dict_list[1]
          fn_dict = out_dict_list[2]

          # Get results for line
          local_results = scr.accuracy(local_fp, local_tp, local_fn)
          local_counts = "tp: " + str(local_tp) + ", fp: " + str(local_fp) + \
                         ", fn: " + str(local_fn)
          local_accuracy = "precision: " + str(round(local_results['precision'], 2)) + " recall: " + \
                          str(round(local_results["recall"], 2))
          print(tabulate([word_list, entity_list]))
          print(local_accuracy, local_counts, "\n")

          with io.open('augmented_sentences.csv', 'a') as f:
              write = csv.writer(f)
              write.writerow(word_list)
              write.writerow(entity_list)
              write.writerow([local_accuracy, local_counts])
              write.writerow("")
          f.close()

      fp_dict, tp_dict, fn_dict = out_dict_list

      final_results = scr.accuracy(fp, tp, fn)

      print("\n" + print_line + print_line)
      print("   Results by Entity")
      print(print_line + print_line)

      print_list = []
      for ent in entities_list:
          entity_results = scr.accuracy(fp_dict[ent], tp_dict[ent], fn_dict[ent])
          entity_precision = round(entity_results["precision"], 2)
          entity_recall = round(entity_results["recall"], 2)
          print_list.append([ent, entity_precision, entity_recall])
      print(tabulate(print_list, headers = ["Entity", "Precision  ", "Recall  "]), "\n")

      print("\n" + print_line)
      print("  Results ")
      print(print_line)
      print("Precision: ", round(final_results["precision"], 2))
      print("Recall:    ", round(final_results["recall"], 2),"\n")