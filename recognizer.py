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
    while len(sentence) > 0:
        ngram_list = make_ngrams(sentence) # Move make_ngram call here
        for ngram in ngram_list[::-1]: # My only job is to get an utterance and find a match. If no match then what?
                for file in filelist:
                    textfile = open(file, 'r')
                    filetext = textfile.read()
                    textfile.close()
                    ngram_string = " ".join(ngram).strip()
                    pattern = re.compile(ngram_string)

                    if pattern.search(filetext):
                        match=(ngram_string, file)
                        return [ngram_string, match]
        match = (sentence, "NOMATCH")
        return [ngram_string, match]




