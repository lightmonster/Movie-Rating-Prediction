from adadecisiontree import *


if __name__ == "__main__":
	import sys

	if len(sys.argv) < 4:
		print "usage : python adadtmain.py imbalance_coefficient max_classifier_no output_file"
		exit(-1)

	attr_type_file_name ='./data/attr_type'
	attr_possible_values_file_name = './data/disc_attr_possible_values'
	train_file = './data/train_clean.csv'
	test_file = './data/test_clean.csv'
	imbalance = float(sys.argv[1])
	max_classifier_no = int(sys.argv[2])
	output_file = sys.argv[3]

	train_data = get_data(train_file)
	test_data = get_data(test_file)

	ada_dt = AdaDecTree(attr_type_file_name, attr_possible_values_file_name, train_data, max_classifier_no, imbalance)

	result = ada_dt.classify(test_data)

	with open(output_file, 'w') as f:
		for item in result:
			f.write("%f\n" %item)
