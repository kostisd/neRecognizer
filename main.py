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

# keep current dir
pwd = os.getcwd()

data = pd.read_csv(config.train_tsv, sep='\t', header=0)
read_dev_data = pd.read_csv(config.dev_tsv, sep='\t', header=0)
print("Done reading data")
devset = prep.prep_dev_data(read_dev_data)

print_line="------------"

if __name__ == '__main__':

   print("\n" + print_line + print_line)
   print("  Data Preprocessing")
   print(print_line + print_line)

   # normalise data
   data[config.string_col] = data[config.string_col].apply(prep.clean_string)

   # filter uncommon entities
   data = prep.filter_entities(data, config.ent_min_n)

   # split data
   print("Creating train/dev sets...")

   train_data, dev_data = train_test_split(data, test_size=config.dev_size)
   print(f"\n    Train set size: {len(train_data.index)}")
   print(f"      Dev set size:  {len(dev_data.index)}")

   if config.train:
      # extract entities to dictionaries from train set
      print("\n" + print_line)
      print("  Training")
      print(print_line)

      print("Preparing Dictionaries...\n")
      prep.make_dictionaries(train_data)

   if config.test:

      # Read test data
      dev_data = dev_data.head(100) # REMOVE THIS TO RUN FULL
      testset = list(zip(dev_data['string'], dev_data['type']))
      testset = dummy.testset
      testset = devset

      # Run recognizer
      print("\n" + print_line)
      print("  Testing:   ")
      print(print_line)
      results_table = scr.make_results_table()
      print("Running Recognizer... ", end = '', flush=True)
      print("\n") # REMOVE later SOOOOOOOOOOOOOS
      #filelist = rcg.searchText("dictionaries/")

      matches = []
      for tst in list(testset):
         sentence = tst[0]
         sentence = tst.lower()
         #ngram_list = rcg.make_ngrams(sentence)
         pwd = os.getcwd()
         rcg_output = rcg.recognizer(sentence)
         #quit()
         matches.append(rcg_output[1])
      print('Done')
      quit()

      print("Calculating accuracy... ", end="", flush=True)

      results = scr.calc_accuracy(matches, testset, results_table)
      accuracy = results[0]
      recall = results[1]
      results_table = results[2]
      print('Done')

      print("Saving results to file... ", end="", flush=True)
     # os.chdir(pwd) # done in searchText now
      results_table.to_csv("./results_table.tsv", sep='\t')
      print("Done")
      print("Results saved in: results_table.tsv")

      print("\n" + print_line)
      print("  Results ")
      print(print_line)
      print(results_table.head())
      print("\nAccuracy: ", round(accuracy,2) , "%")
      print("Recall:    ", round(recall,2) , "\n")






