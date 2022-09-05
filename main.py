import config
import prep_data as prep
import recognizer as rcg
import scoring as scr
import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
import json

# keep current dir
pwd = os.getcwd()

data = pd.read_csv(config.input_data, sep='\t', header=0)
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
      testset = list(zip(dev_data['string'], dev_data['type']))

      # Run recognizer
      print("\n" + print_line)
      print("  Testing:   ")
      print(print_line)
      results_table = scr.make_results_table()
      print("Running Recognizer... ", end = '', flush=True)
      filelist = rcg.searchText("dictionaries/")

      matches = []
      for tst in list(testset):
         sentence = tst[0]
         ngram_list = rcg.make_ngrams(sentence)
         rcg_output = rcg.recognizer(sentence, ngram_list, filelist)
         matches.append(rcg_output[1])
      print('Done')

      print("Calculating accuracy... ", end="", flush=True)

      results = scr.calc_accuracy(matches, testset, results_table)
      accuracy = results[0]
      recall = results[1]
      results_table = results[2]
      print('Done')

      print("Saving results to file... ", end="", flush=True)
      os.chdir(pwd) # return to cwd to save results here
      results_table.to_csv("./results_table.tsv", sep='\t')
      print("Done")
      print("Results saved in: results_table.tsv")

      print("\n" + print_line)
      print("  Results ")
      print(print_line)
      print(results_table.head())
      print("\nAccuracy: ", round(accuracy,2) , "%")
      print("Recall:    ", round(recall,2) , "\n")






