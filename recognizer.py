import pandas as pd
from tabulate import tabulate
import re
import os
import prep_data

def make_ngrams(sentence):
    ngram = 1 # starting from 1
    ngram_list = []
    split_sentence = sentence.split()
    while ngram <= len(split_sentence):
        # -ngram to avoid duplicates or out of range error
        for i in range(len(split_sentence) -ngram + 1):
            grams = split_sentence[i:i+ngram]
            ngram_list.append(grams)
            i += 1
        ngram += 1
    return ngram_list

def searchText(ngram_string, path):
    # change dirs to access dictionaries
    pwd = os.getcwd()
    os.chdir(path)
    entities_list = os.listdir()

    match_counts = 0
    match_entity = "NOMATCH"
    for entity in entities_list:
        textfile = open(entity, 'r')
        filetext = textfile.read()
        textfile.close()
        # apply cleaning to both pattern and string
        # filetext = prep_data.strong_clean_string(filetext)
        # ngram_string = prep_data.strong_clean_string(ngram_string)
        # pattern = 'r"^' + ngram_string + '$'
        # new_counts = filetext.count(pattern)

      #  print(pattern)
      #  quit()

        # Searching algorithm
        new_counts = filetext.count(ngram_string)
        if new_counts > match_counts:
            match_counts = new_counts
            match_entity = entity

    # Tell match_finder there was NOMATCH for this ngram
    match_found = True if match_counts > 0 else False

    os.chdir(pwd) # Return to default pwd

    return [match_found, match_entity]

def trim_sentece(sentence, ngram_length, ngram_start):
    if ngram_start == 0:  # match is at start of utt
        #sentence = sentence[ngram_start + ngram_length:len(sentence)]  # removed -1 ,it was del last char
        # keep an eye on this change
        sentence = sentence[ngram_start + ngram_length:]  # removed -1 ,it was del last char
    elif (ngram_start + ngram_length) >= len(sentence):  # match is at the end of utt (KEEP AN EYE AT >
        sentence = sentence[0:ngram_start]
    elif ngram_start > 0 and (ngram_start + ngram_length) < len(sentence):  # match in the middle
        # MAJOR CHANGE HERE
        sentence = sentence[0:ngram_start] + sentence[(ngram_start + 1 + ngram_length):len(sentence) + 1]
        #sentence2 = entence[ngram_start + ngram_length:]
    else:
        print("ERROR rcg.trim_sentence: Something is wrong with indexing this ngram")
        quit()

    return sentence

def match_finder(sentence, ngram_list):
    original_sentence = sentence
    match_found = False
    for ngram in ngram_list[::-1]:
        if match_found == False:
            ngram_string = " ".join(ngram).strip()

            match_found, entity = searchText(ngram_string, "dictionaries/")

            if match_found: # check if match found
                # Remove match from sentence and repeat
                ngram_length = (len(ngram_string))
                ngram_start = original_sentence.find(ngram_string)

                match = (ngram_string, entity, ngram_start, ngram_length)
                sentence = trim_sentece(sentence, ngram_length, ngram_start)
                return [sentence, match]

    # if NO MATCH
    entity = "NOMATCH"
    ngram_length = (len(ngram_string))
    ngram_start = original_sentence.find(ngram_string)
    match = (ngram_string, entity, ngram_start, ngram_length)
    sentence = trim_sentece(sentence, ngram_length, ngram_start)

    return [sentence, match]

# Starting searching from the longest ngram
def recognizer(input_list):
    original_sentence = input_list[1]
    sentence = original_sentence
    id = input_list[0]
    string_dict = {}
    entity_dict = {}
    while len(sentence.strip()) > 0:
        ngram_list = make_ngrams(sentence.strip())
        sentence, match = match_finder(sentence, ngram_list)
        string_matched = match[0]
        entity_matched = match[1]
        # span_matched = match[3]

        start_index_matched = original_sentence.find(string_matched)
        string_dict[start_index_matched] = string_matched
        print(string_dict)
        entity_dict[start_index_matched] = entity_matched

    words = sorted(string_dict.items())
    print("Sorted: ", words)
    entities = sorted(entity_dict.items())
    #words_indexes = sorted(string_dict.keys())
    #entities_indexes = sorted(entity_dict.keys())

    word_list = []
    entity_list = []
    for word, entity in zip(words, entities):
        word_list.append(word[1])
        entity_list.append(entity[1])

    #print(tabulate([word_list, entity_list]))

    return (id, word_list, entity_list)
    #return [string_dict, entity_dict]

