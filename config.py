# Train data
train_tsv = "data/ontonotes_en_name_entity.tsv"
string_col = 'string' # name of text column
entities_col = 'type'

# Dev data
original_dev_tsv = "data/ontonotes_en_token.tsv"

# Gerneral
ent_min_n = 3 # remove entities if n < 3

train=False
test=True