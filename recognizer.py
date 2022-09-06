import re
import os

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

def searchText(path):
    os.chdir(path)
    filelist = os.listdir()
    return filelist

# Starting searching from the longest ngram
def recognizer(sentence, filelist):
    original_sentence = sentence
    string_dict = {}
    entity_dict = {}
    #print("Original sentence", sentence)
    while len(sentence.strip()) > 0:
        ngram_list = make_ngrams(sentence.strip())
        sentence, match = match_finder(sentence, ngram_list, filelist)
        string_matched = match[0]
        entity_matched = match[1]
        start_index_matched = original_sentence.find(string_matched)
        span_matched = match[3]
        #string_dict[string_matched] = start_index_matched
        #entity_dict[entity_matched] = start_index_matched
        string_dict[start_index_matched] = string_matched
        entity_dict[start_index_matched] = entity_matched

        #print("Table: ", string_matched, entity_matched, start_index_matched, span_matched)
        #print("Trimmed Sentence ", sentence)
    a = sorted(string_dict.keys())
    b = sorted(string_dict.items())
    c = sorted(entity_dict.keys())
    d = sorted(entity_dict.items())
    str=""
    ents= (' ' * len(original_sentence))
    prev_index = 0

    for word, entity in zip(b, d):
        #print("Entity: ", entity, " Word: ", word)
        print("Prev: " , prev_index)
        print("Curr", entity[0])
        print("Steps: ", entity[0] - prev_index -1)
        #print("Current loc: ", entity[0] - prev_index)
        str += (" " + word[1])
        ents = ents[:entity[0]]  + entity[1] + ents[entity[0] + 1:]
        #ents += (("#"*(entity[0] - prev_index - 1)) + entity[1])
        prev_index = entity[0]


        #str += (" " + word[0][1])
        #ent += (" " + str(entity[1][1]))
    print(str)
    print(ents)

    #print(str)
    #print(a)
    # print(b)
    # print(c)
    # print(d)
    # entity_dict = sorted(entity_dict)
    # #print("Dictionary: ", string_dict)
    #print(entity_dict)


    return [string_dict, entity_dict]

def match_finder(sentence, ngram_list, entities_list):
    origial_sentence = sentence
    #print("MATCH_FINDER:", origial_sentence, sentence)
    match_found = False
    for ngram in ngram_list[::-1]:
        if match_found == False:

            # search start
            for entity in entities_list:
                textfile = open(entity, 'r')
                filetext = textfile.read()
                textfile.close()
                ngram_string = " ".join(ngram).strip()
                pattern = re.compile(ngram_string)
            # end of search

                if pattern.search(filetext):
                    match_found = True
                    # Remove match from sentence and repeat
                    ngram_length = (len(ngram_string))
                    ngram_start = sentence.find(ngram_string)
                    match = (ngram_string, entity, ngram_start, ngram_length)
                    sentence = trim_sentece(sentence, ngram_length, ngram_start)
                    return [sentence, match]

    # if NO MATCH
    entity = "NOMATCH"
    ngram_length = (len(ngram_string))
    ngram_start = origial_sentence.find(ngram_string)
    match = (ngram_string, entity, ngram_start, ngram_length)
    sentence = trim_sentece(sentence, ngram_length, ngram_start)

    return [sentence, match]

def trim_sentece(sentence, ngram_length, ngram_start):
    if ngram_start == 0:  # match is at start of utt
        sentence = sentence[ngram_start + ngram_length:len(sentence)]  # removed -1 ,it was del last char
    elif (ngram_start + ngram_length) == len(sentence):  # match is at the end of utt
        sentence = sentence[0:ngram_start]
    else:  # match in the middle
        sentence = sentence[0:ngram_start] + sentence[(ngram_start + 1 + ngram_length):len(sentence) + 1]
    return sentence

