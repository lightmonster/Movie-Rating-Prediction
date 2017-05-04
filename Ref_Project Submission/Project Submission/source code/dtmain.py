from decisiontree import *
from preprocess import *

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 3:
		print "usage : python dtmain.py max_depth output_file"
		exit(-1)

	attr_type_file_name ='./data/attr_type'
	attr_possible_values_file_name = './data/disc_attr_possible_values'
	train_file = './data/train_clean.csv'
	test_file = './data/test_clean.csv'
	max_depth = sys.argv[1]
	output_file = sys.argv[2]

	attr_type_dict = get_attr_types(attr_type_file_name)
	attr_possible_values = get_possible_values(attr_possible_values_file_name)
	# this is the common information for all training process just copy for adaboosting
	# input for attr_type_file_name is the attr_type file in data folder
	# input for attr_possible_value_file_name is the disc_attr_possible_values in data folder

	train_data = get_data(train_file)
	test_data = get_data(test_file)

	dec_tree = DecisionTree(max_depth, 3, 0)
	# initialize a Decision Tree with parameter specification (depth, method, criterion)
	# methond = 1 ,2 ,3 for different attribute selection method (information gain, gini gain, gain ratio)

	dec_tree.train_data = train_data
	dec_tree.attr_type_dict = attr_type_dict
	dec_tree.disc_possible_values = attr_possible_values
	# give parameters for Decision Tree class

	dec_tree.train()
	# tree training

	result = dec_tree.classify(test_data)

	with open(output_file, 'w') as f:
		for item in result:
			f.write("%f\n" %item)

