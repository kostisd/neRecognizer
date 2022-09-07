import config
import prep_data as prep
import recognizer as rcg
import scoring as scr
import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
import json

import dummy



print_line = "------------"

if __name__ == '__main__':

   print("\n" + print_line + print_line)
   print("  Data Preprocessing")
   print(print_line + print_line)

   print("Reading data... ", end = '', flush=True)
   original_train_data = pd.read_csv(config.train_tsv, sep='\t', header=0)
   original_dev_data = pd.read_csv(config.dev_tsv, sep='\t', header=0)
   print("Done")

   # Data Preparation
   train_data = original_train_data

   # Normalise utterances
   print("Preparing train set... ", end = '', flush=True)
   train_data[config.string_col] = train_data[config.string_col].apply(prep.clean_string)
   print("Done")

   # Extract dev sentences and normalise
   print("Preparing dev set... ", end = '', flush=True)
   devset = prep.prep_dev_data(original_dev_data)
   print("Done")

   # filter uncommon entities in train set
   train_data = prep.filter_entities(train_data, config.ent_min_n)

   quit()
   if config.train:
      # extract entities to dictionaries from train set
      print("\n" + print_line)
      print("  Training")
      print(print_line)

      print("Preparing Dictionaries...\n")
      prep.make_dictionaries(train_data)

   if config.test:

      #testset = dummy.testset
      #testset = devset

      # Run recognizer
      print("\n" + print_line)
      print("  Testing:   ")
      print(print_line)
      results_table = scr.make_results_table()
      print("Running Recognizer... ", end = '', flush=True)
      print("\n") # REMOVE later SOOOOOOOOOOOOOS

      matches = []
      for line in list(devset):
         sentence = line[0]
         sentence = line.lower()
         rcg_output = rcg.recognizer(sentence)
         matches.append(rcg_output[1])
      print('Done')

      print("Prepare matches table... ", end="", flush=True)

      print('Done')

      quit()

      print("Calculating accuracy... ", end="", flush=True)

      results = scr.calc_accuracy(matches, testset, results_table)
      accuracy = results[0]
      recall = results[1]
      results_table = results[2]
      print('Done')

      print("Saving results to file... ", end="", flush=True)
      results_table.to_csv("./results_table.tsv", sep='\t')
      print("Done")
      print("Results saved in: results_table.tsv")

      print("\n" + print_line)
      print("  Results ")
      print(print_line)
      print(results_table.head())
      print("\nAccuracy: ", round(accuracy,2) , "%")
      print("Recall:    ", round(recall,2) , "\n")






