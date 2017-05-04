import math

class decisionNode:
	def __init__(self):
		#the property to make decision in this level
		self.decision_property_serial = 0
		#set the level of tree
		self.level = 0
		#set the nodes
		self.nodes = []
		#classify standard. len(If self.nodes ) != 0, then when test data come in, which node should it goes to?
		#form example, self.standard = [[0, 10], [10, 20], [20, 25], [25,29]] means if value < 10 then go to first node, 10~20 to the second,
		# 20~25 to third and 25~more to the forth
		self.standard = []
		#if len(self.nodes) == 0 then this is a leaf, a leaf should has a final value for the classifier. this value only valid if self.nodes has no elements
		self.result  = 0.0


	####################### helper functions ##############################################
	'''
	Helper
	function used to compute entrophy
	'''
	def compute_entrophy(self, data_set):
		entrophy = 0.0
		total_num = len(data_set)
		value_dict = {}
		for data in data_set:
			value = data[-1]
			if value in value_dict:
				value_dict[value] += 1
			else:
				value_dict[value] =  1

		#THIS CAN BE MODIFIED! APPLY THE WAY YOU LIKE! GINI OR WHAT THE FUCK EVER
		for k,v in value_dict.iteritems():
			appear_probability = float(v)/float(total_num)
			#this is tricky... log(a)/log(b) = log a (b), so I use log(x)/log(2) to get log 2 (x)
			entrophy -= appear_probability* (math.log(appear_probability)/math.log(2))
		#THIS CAN BE MODIFIED! APPLY THE WAY YOU LIKE! GINI OR WHAT THE FUCK EVER

		return entrophy

	'''
	Helper
	compute the most common value of the last element in each data
	'''
	def compute_most_common_value(self, data_set):
		value_dict = {}
		for data in data_set:
			value = data[-1]
			if value in value_dict:
				value_dict[value] += 1
			else:
				value_dict[value] =  1
		result = 0
		max_appearance  = 0
		for k,v in value_dict.iteritems():
			if v > max_appearance:
				max_appearance = v
				result = k
		return result

	'''
	Helper
	function used to split a data set on given property
	return is a list of two
	first is the spliting standard
	second is splitted sets
	'''
	def split_tree(self, data_set, property_serial):
		result = []
		spliter  = []
		splitted_data = []
		#first figure out what kind of data we are dealing with: only 1and 0 or a continuous value
		value_dict = {}
		min_value  = 0.0
		max_value = 0.0
		only_zero_and_one = True
		for data in data_set:
			value = data[property_serial]
			if only_zero_and_one and  value != 0 and value != 1:
				only_zero_and_one = False
			if value < min_value:
				min_value = value
			if value > max_value:
				max_value = value
			if value in value_dict:
				value_dict[value] += 1
			else:
				value_dict[value] =  1

		#THIS CAN BE MODIFIED! APPLY THE WAY YOU LIKE!
		if only_zero_and_one:
			spliter=[[0.0, 0.5], [0.5, 1]]
			ones = []
			zeros = []
			for data in data_set:
				if data[property_serial] == 0:
					zeros.append(data)
				else:
					ones.append(data)
			splitted_data = [zeros, ones]
		else:
			#right now my way is to split into two trees
			median = (min_value + max_value )/2.0
			spliter=[[min_value, median], [median, max_value]]
			first_half = []
			second_half = []
			for data in data_set:
				if data[property_serial] <= median:
					first_half.append(data)
				else:
					second_half.append(data)
			splitted_data = [first_half, second_half]
		#THIS CAN BE MODIFIED! APPLY THE WAY YOU LIKE!

		result.append(spliter)
		result.append(splitted_data)
		return result

	'''
	Helper
	function used to return a value on a given dataset
	'''
	def test(self, data):		
		#if leaf, then return value
		if len(self.nodes) == 0:
			return self.result
		else:
			val = data[self.decision_property_serial]
			#print "evluating on property #", self.decision_property_serial
			for i in range(0, len(self.standard)):
				if i == 0:
					splitter = self.standard[i]
					if val < splitter[1]:
						#go to the next node
						return self.nodes[i].test(data)
				elif i == len(self.standard) - 1:
					splitter = self.standard[i]
					if val >= splitter[0]:
						#go to the next node
						return self.nodes[i].test(data)
				else:
					splitter = self.standard[i]
					if val >= splitter[0] and val < splitter[1]:
						#go to the next node
						return self.nodes[i].test(data)
		#something goes wrong
		return -9999.9999
	'''
	given a tranning set and a boolean list of if every property has been used, compute the decision property in this level
	the last three parameter is the accuracy threshold, desired max level(0 means no limit) and desired min number of data
	'''
	def get_decision_property(self, training_set, unused_property_list, level, accuracy_threshold = 1.0, max_level = 0, min_data_num = 1):
		#set level
		self.level = level
		print "///////////////////////////////////////////a node of level: ", level
		####################### base case ##############################################
		#if the lenght of the data left in tranning set is smaller than threshold then stop sub-dividing
		if len(training_set) <= min_data_num:
			self.result = self.compute_most_common_value(training_set)
			print "end divide due to min data num", self.result
			return

		#if the tree is the way too high, stop
		if max_level != 0 and level >= max_level:
			self.result = self.compute_most_common_value(training_set)
			print "end divide due to level constraint", self.result
			return

		#if accuracy is high enough then stop 
		most_common_value =  self.compute_most_common_value(training_set)
		print "most common value of this node is:", most_common_value
		data_num_with_most_common_value = 0
		for data in training_set:
			if data[-1] ==  most_common_value:
				data_num_with_most_common_value += 1
		print "accuracy is :", float(data_num_with_most_common_value) / float(len(training_set))
		if float(data_num_with_most_common_value) / float(len(training_set)) >= accuracy_threshold:
			self.result =  most_common_value
			print "end divide due to accuracy threshold achieved, final result is ", self.result
			return


		####################### training process ##############################################
		#keep track the gain of each property
		current_max_gain = 0.0
		current_max_gain_property_serial = -1
		#get the current enttophy of data
		current_entrophy= self.compute_entrophy(training_set)
		print "current entrophy is: ", current_entrophy
		#get the number of tranning set
		training_set_num = len(training_set)
		#go through each perperty
		for i in range(0, len(unused_property_list)):
			if unused_property_list[i] ==  False:
				continue
			else:
				print "//////analysing property #" , i
				new_entrophy  = 0.0
				#first split the tree
				splitted_result = self.split_tree(training_set, i)
				splitted_sets = splitted_result[1]
				#then compute the entrophy of each node with WEIGHT
				for splitted_set in splitted_sets:
					new_entrophy += float(self.compute_entrophy(splitted_set)) * len(splitted_set) / float(training_set_num)

					#print "new entrophy", new_entrophy
				#make judgement
				gain = current_entrophy - new_entrophy
				print "gain on this property is: ", gain
				if gain > current_max_gain:
					current_max_gain = gain
					current_max_gain_property_serial = i
		#if current_max_gain_property_serial == 0 means no property is getting gain or no more available property. Any way return
		if current_max_gain_property_serial == -1:
			self.result = self.compute_most_common_value(training_set)
			print "end divide due to no gainning"
			return
		else:
			print "///////////final decision splitter property number is : ", current_max_gain_property_serial
			unused_property_list[current_max_gain_property_serial] = False
			self.decision_property_serial =  current_max_gain_property_serial
			splitted_result = self.split_tree(training_set, current_max_gain_property_serial)
			self.standard = splitted_result[0]
			print "///////////standard is: ", self.standard
			splitted_sets = splitted_result[1]
			for splitted_set in splitted_sets:
				node = decisionNode()
				node.get_decision_property(splitted_set, unused_property_list, self.level + 1, accuracy_threshold, max_level, min_data_num )
				self.nodes.append(node)


class decisionTree:
	def __init__(self):
		self.root = decisionNode()

	def train(self, training_set, accuracy_threshold = 1.0, max_level = 0, min_data_num = 1):
		print "trainning begain:///////////////////////////////////////////////"
		property_num = len(training_set[0]) -1
		print "propeties total is: ", property_num
		#set a list of properties that are unused to split the tree
		unused_property_list = [True] * property_num
		self.root.get_decision_property(training_set, unused_property_list, 0, accuracy_threshold, max_level, min_data_num)

	def self_test(self, training_set):
		print "self-test begain:///////////////////////////////////////////////"
		print "self-test begain:///////////////////////////////////////////////"
		print "self-test begain:///////////////////////////////////////////////"
		print "self-test begain:///////////////////////////////////////////////"
		test_date = []
		for data in training_set:
			new_data = data[:-1]
			test_date.append(new_data)
		total = 0.0
		correct  = 0.0
		result_set = {}
		for i in range(0, len(test_date)):
			result  = self.root.test(test_date[i])
			if result in result_set:
				result_set[result] += 1
			else:
				result_set[result] = 1
			if result == training_set[i][-1]:
				correct += 1.0
			total +=1.0
		print "final precision :" , correct/total
		for k,v in result_set.iteritems():
			print "class: " , k
			print "num: ", v


	def test(self, testing_set):
		print "test begain:///////////////////////////////////////////////"
		print "test begain:///////////////////////////////////////////////"
		print "test begain:///////////////////////////////////////////////"
		print "test begain:///////////////////////////////////////////////"
		result_set = {}
		for data in testing_set:
			answer = self.root.test(data)
			if answer in result_set:
				result_set[answer] += 1
			else:
				result_set[answer] = 1
		for k,v in result_set.iteritems():
			print "class: " , k
			print "num: ", v