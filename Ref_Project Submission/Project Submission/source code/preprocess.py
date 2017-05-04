from pandas import *


def get_attr_types(input_file):
	attr_types = {}
	with open(input_file, "r") as f_in:
		for line in f_in:
			arr = line.strip().split(":")
			if len(arr) < 2:
				continue
			attr_name = arr[0]
			attr_type = arr[1]

			attr_types[attr_name] = attr_type

	return attr_types


def get_possible_values(input_file):
	possible_values = {}

	with open(input_file, "r") as f_in:
		for line in f_in:
			arr = line.strip().replace("'", "").split(":")
			if len(arr) < 2:
				continue

			attr_name = arr[0]
			possible_value_list = arr[1].strip().split(",")
			data_type = arr[2]

			if data_type == 'int':
				possible_value_list = [int(i) for i in possible_value_list]

			possible_values[attr_name] = possible_value_list

	return possible_values


def get_data(data_file):
	data_frame = read_csv(data_file)
	return data_frame
