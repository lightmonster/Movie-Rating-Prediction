from attributeselectionmethod import *


class DecisionTreeNode:
	def __init__(self):
		self.children = []
		self.indicated_class = None
		self.split_attr = None

	@property
	def is_leaf(self):
		return len(self.children) == 0


class DecisionTree:
	def __init__(self, max_depth, method, criterion):
		self.root = None
		self.train_data = None
		self.attr_type_dict = None
		self.disc_possible_values = None

		self._max_depth = max_depth
		self._method = method
		self._criterion = criterion


	def get_major_class(self, data_frame):
		pos_count = sum(data_frame['IsBadBuy'] == 1)
		neg_count = sum(data_frame['IsBadBuy'] == 0)

		if pos_count > neg_count:
			return 1
		else:
			return 0


	def gen_tree(self, data_frame, attr_dict, depth):

		node = DecisionTreeNode()
		
		depth += 1
		if (depth > self._max_depth): # edit by shuanglong
			node.indicated_class = self.get_major_class(data_frame)
			return node

		do_split, selected_attr = attribute_selection_method(data_frame, attr_dict, self._method, self._criterion)
		#print selected_attr.split

		if do_split == False:
			node.indicated_class = self.get_major_class(data_frame)
			return node

		#print "====selected_attr = %s" %(selected_attr.name)

		node.split_attr = selected_attr

		data_slice_list = attr_slice(data_frame, selected_attr)

		if not selected_attr.if_cont: #edit by shuanglong
			attr_dict.pop(selected_attr.name)

		major_class_of_current_data_frame = self.get_major_class(data_frame)
		for child_data_frame in data_slice_list:
			if len(child_data_frame) == 0:
				child_node = DecisionTreeNode()
				child_node.indicated_class = major_class_of_current_data_frame
				node.children.append(child_node)
			elif len(child_data_frame) <= 4:
				child_node = DecisionTreeNode()
				child_node.indicated_class = self.get_major_class(child_data_frame) #edit by shuanglong
				node.children.append(child_node)
			else:
				child_node = self.gen_tree(child_data_frame, attr_dict, depth)
				node.children.append(child_node)

		if not selected_attr.if_cont: #edit by shuanglong
			attr_dict[selected_attr.name] = selected_attr

		return node


	def train(self):

		attr_dict = {}
		for attr in self.attr_type_dict:
			if self.attr_type_dict[attr] == "disc":
				attr_dict[attr] = Attr(attr, False, self.disc_possible_values[attr])
			else:
				attr_dict[attr] = Attr(attr, True, [])

		self.root = self.gen_tree(self.train_data, attr_dict, 0)


	def get_decision(self, data_series):
		cur_node = self.root
		while cur_node.is_leaf == False:
			split_attr_name = cur_node.split_attr.name
			value = data_series[split_attr_name]

			child_index = -1
			if cur_node.split_attr.if_cont == False:
				#try:
				child_index = cur_node.split_attr.split.index(value)
				#except:
					#print split_attr_name
			else:
				for i in range(len(cur_node.split_attr.split)):
					if cur_node.split_attr.split[i] > value:
						child_index = i
						break
				if child_index == -1:
					child_index = len(cur_node.split_attr.split)

			cur_node = cur_node.children[child_index]


		return cur_node.indicated_class


	def classify(self, test_frame):

		results = [-1] * len(test_frame)
		
		for i in range(len(test_frame)):
			data_record = test_frame.iloc[i]
			results[i] = self.get_decision(data_record)

		return results