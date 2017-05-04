from decisiontree import *
from preprocess import *
import math

class AdaDecTree:

	def __init__(self, attr_type_file_name, attr_possible_values_file_name, train_data, max_classifier_no, imbalance):

		self.max_classifier_no = max_classifier_no
		self.classifier_no = 0
		self.attr_type_dict = get_attr_types(attr_type_file_name)
		self.attr_possible_values = get_possible_values(attr_possible_values_file_name)
		self.train_data = train_data
		self.weights = [1.0/len(self.train_data)] * len(self.train_data)
		self.classifier = {}
		self.alpha_list = [0] * self.max_classifier_no
		self.imbalance = imbalance

		self.train()


	def classify(self, data):
		predictions = np.array([0.0] * len(data))
		for i in range(self.max_classifier_no):
			current_prediction = np.array(self.classifier[i].classify(data))
			if self.alpha_list[i] > 0:
				predictions = predictions + (self.alpha_list[i] * current_prediction)
			else:
				predictions = predictions - (self.alpha_list[i] * (1 - current_prediction))

		return predictions/sum(abs(np.array(self.alpha_list)))


	def train(self):
		self.classifier_no = 0
		for i in range(self.max_classifier_no):

			sample_indexes = self.sample_index()
			current_train_data = self.train_data.loc[sample_indexes]

			current_classifier = DecisionTree(3, 3, 0)

			current_classifier.train_data = current_train_data
			current_classifier.attr_type_dict = self.attr_type_dict
			current_classifier.disc_possible_values = self.attr_possible_values

			current_classifier.train()

			correct_true, correct_false, error = self.classify_train(current_classifier, self.train_data)

			self.alpha_list[self.classifier_no] = math.log((1 - error) / error)
			self.classifier[self.classifier_no] = current_classifier

			if error < 0.5:
				incorrect_true = [i for i in range(len(self.train_data)) if (i not in correct_true) & (self.train_data['IsBadBuy'][i]==1)]
				incorrect_false = [i for i in range(len(self.train_data)) if (i not in correct_false) & (self.train_data['IsBadBuy'][i]==0)]
			else:
				error = 1-error
				incorrect_true = correct_true
				incorrect_false =correct_false

			for index in incorrect_true:
				self.weights[index] *= ((1 - error) / error) * self.imbalance
			for index in incorrect_false:
				self.weights[index] *= ((1 - error) / error)

			sum_weights = sum(self.weights)
			self.weights = [float(w) / sum_weights for w in self.weights]

			print "len(correct_true) = %d, len(correct_false) = %d, error = %f" %(len(correct_true),len(correct_false),error)

			self.classifier_no += 1

	def sample_index(self):
		sample = np.random.multinomial(len(self.train_data), self.weights)
		sample_indexes = [0]*len(sample)
		count = 0
		for i in range(len(sample)):
			if sample[i] !=0:
				for j in range(sample[i]):
					sample_indexes[count] = i
					count += 1
		return sample_indexes


	def classify_train(self, dec_tree, data):
		predictions = dec_tree.classify(data)
		correct_true = []
		correct_false = []
		num_true = sum(data['IsBadBuy'])
		num_false = len(data) - num_true

		for i in range(len(predictions)):
			if predictions[i] == data['IsBadBuy'][i]:
				if data['IsBadBuy'][i] == 0:
					correct_false.append(i)
				else:
					correct_true.append(i)

		error = 1 - float(len(correct_false) + self.imbalance*len(correct_true)) /(num_false + num_true*self.imbalance)

		if error == 0:
			error = 1 / len(self.train_data)

		return (correct_true, correct_false, error)