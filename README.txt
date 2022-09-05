-----------------------
Name Entity Recogniser
-----------------------

Usage: . run.sh

Settings in config.py:

	dev_size: Ratio to split the data to train/dev, e.g. 0.2	
	input_data: Path to input tsv file, e.g. data/ontonotes_en_name_entity.tsv
	string_col: Name of text column, e.g. 'string' 
	entities_col: Name of entities column, e.g. 'type'
	ent_min_n: Counts threshold for removing scarce entities, e.g. 3
	train: Run training stage (True/False)
	test: Run testing stage (True/False)
