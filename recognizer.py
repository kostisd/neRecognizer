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

def trim_sentece(sentence_queue, sentence, ngram_start, ngram_length):
    if ngram_start == 0: # match is at start of utt
        sentence = sentence[ngram_start + ngram_length:]  # removed -1 ,it was del last char
        sentence_queue.append(sentence)
    elif (ngram_start + ngram_length) >= len(sentence):  # match is at the end of utt (KEEP AN EYE AT >
        sentence = sentence[0:ngram_start]
        sentence_queue.append(sentence)
    elif ngram_start > 0 and (ngram_start + ngram_length) < len(sentence):  # match in the middle
        sentence1 = sentence[0:ngram_start]
        sentence2 = sentence[(ngram_start + ngram_length):]
        sentence_queue.extend([sentence1, sentence2])
    else:
        print("ERROR rcg.trim_sentence: Something is wrong with indexing this ngram")
        quit()
    return sentence_queue

def searchText(ngram_string, path):
    pwd = os.getcwd()
    os.chdir(path)
    entities_list = os.listdir()

    match_entity = "NONE"
    match_found = False
    ngram_string = ngram_string.strip()
    ngram_string = "^" + ngram_string + "$"
    for entity in entities_list:
        with open(entity, 'r') as f:
            for line in f.readlines():
                found = re.findall(ngram_string, line)
                if found:
                    match_found = True
                    match_entity = entity

                    f.close()
                    os.chdir(pwd)  # Return to default pwd
                    return [match_found, match_entity]
            f.close()
    os.chdir(pwd) # Return to default pwd
    return [match_found, match_entity]

def match_finder(ngram_list):
    match_found = False # should stop searching if True
    for ngram in ngram_list[::-1]: # starting from the longest ngram
        if match_found is False:
            ngram_string = " ".join(ngram).strip()
            match_found, entity = searchText(ngram_string.strip(), "dictionaries/")
            if match_found: # check if match found
                match = (ngram_string, entity) # here we just pack the match info and pass it over
                return match
    # if NO MATCH
    entity = "NOMATCH"
    match = (ngram_string, entity)
    return match

def recognizer(input_list):
    # input_list contains the id at [0] and the sentence as string at [1]
    original_sentence = input_list[1]
    sentence_queue = [] # we will be adding trimmed sentences to tag
    sentence = original_sentence # we'll work with sentence later
    sentence_queue.append(sentence)
    id = input_list[0]
    string_dict = {} # add all matched ngrams here
    entity_dict = {} # add all found entities here
    while sentence_queue:
    #    print("Queue 0: ", sentence_queue)
        sentence = sentence_queue.pop(0)
        while len(sentence.strip()) > 0: # this will stop the matching and trimming cycle
            ngram_list = make_ngrams(sentence) # we re-do the ngrams after every match
            match = match_finder(ngram_list) # sentence here is a new, trimmed sub-sentence
            string_matched, entity_matched = match[0], match[1] # match_finder just sends the matched ngram and it's tag
            start_index_matched = original_sentence.find(string_matched) # FOR SORTING - NOT TRIMMING find match in original
            string_dict[start_index_matched] = string_matched # store matched string
            entity_dict[start_index_matched] = entity_matched # store tag of string
            pattern = re.compile(rf'(^|\s){string_matched}($|\s)')
            trim_index_matched = re.search(pattern, sentence).start() # FOR SORTING - NOT TRIMMING find match in original
            sentence_queue = trim_sentece(sentence_queue, sentence, trim_index_matched, (len(string_matched)+1)) # returns queue
            sentence = sentence_queue.pop(0)

        words = sorted(string_dict.items())
        entities = sorted(entity_dict.items())
        word_list = []
        entity_list = []
        for word, entity in zip(words, entities):
            word_list.append(word[1])
            entity_list.append(entity[1])

    return (id, word_list, entity_list)