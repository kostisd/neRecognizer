# neRecognizer

### 1. Data Preparation

Reading the dev data line by line and adding completed sentences to a new csv.
Using the part_of_speech column to detect the end of sentences and empty lines

![Original dev dataset](./graphs/original_dev.png)

We can now read the sentences as one string and use the ids to search the train data for the true entity

![Original dev dataset](./graphs/prep_dev.png)

### 2. Printing Results

Printing out the augmented sentences, using NOMATCH for empty tags.
Below the lines we get the local scores for each sentence.

![Original dev dataset](./graphs/tabulate.png)

Printing the final results. The first table contains results by entity. After that we get the overall scores for the devset.

![Original dev dataset](./graphs/results_table.png)

A boxplot with the True Positives (Matched) counts per entity

![Original dev dataset](./graphs/boxplot.png)

These are the most frequent matches in the subset

![Original dev dataset](./graphs/top_ngram.png)


