import sys
import math
import numpy as np

class NaiveBayes:
    def __init__(self):
        self.training_data = []
        self.pos_cnt = 0
        self.neg_cnt = 0
        self.Num = 0
        self.pos_frequency = []
        self.neg_frequency = []

    # Runs the classifier and uses classifyTuples() to predict. Also writes the output in either 0 or 1
    def runClassifier(self, t_file):
        # print("Running Classifier on "+str(testing_file)+" to evaluate performance")
        attr_titles = None
        with open('nb_output.txt', 'w') as f:
            for line in open(t_file):
                line = line.rstrip('\n')
                attributes = line.split(',')
                if attr_titles is None:
                    attr_titles = attributes  # change this if required
                else:
                    # class_label = attributes[0]
                    cont_attrs = attributes[16:24]
                    cont_attrs.insert(0, attributes[12])
                    cont_attrs.append(attributes[29])
                    cont_attrs.append(attributes[31])
                    dsc_attrs = attributes[2:12]
                    dsc_attrs.append(attributes[13])
                    dsc_attrs.append(attributes[14])
                    dsc_attrs.append(attributes[15])
                    dsc_attrs.append(attributes[30])

                    label_predicted = self.classifyTuples(dsc_attrs, cont_attrs)
                    f.write(label_predicted+"\n")

    # Classifies each of the tuples.
    def classifyTuples(self, dsc_attrs_vector, cont_attrs_vector):
        # def classifyTuples(self, dsc_attrs_vector):
        neg_prob = self.p_neg
        pos_prob = self.p_pos
        # print("cont_attrs_vector: ", len(cont_attrs_vector))
        for i in range(len(dsc_attrs_vector)):
            try:
                neg_prob += self.p_neg_attr[i][dsc_attrs_vector[i]]
            except KeyError:
                neg_prob += 0
            try:
                pos_prob += self.p_pos_attr[i][dsc_attrs_vector[i]]
            except KeyError:
                pos_prob += 0

        for attr in cont_attrs_vector:
            bp = gp = a = b=  1
            power = -1 / 2 * math.pow((float(attr) - self.mean[0]), 2) / (self.std[0] ** 2)
            bp *= math.exp(power) / math.sqrt(2 * math.pi) * self.std[0]
            power = -1 / 2 * math.pow((float(attr) - self.mean[1]), 2) / (self.std[1] ** 2)
            gp *= math.exp(power) / math.sqrt(2 * math.pi) * self.std[1]
            pos_prob += math.log(gp)
            neg_prob += math.log(bp)

        if neg_prob < pos_prob:
            return '+1'
        else:
            return '0'

    # trains the classifier
    def trainClassifier(self, file_name):
        attr_titles = None
        self.cl = []

        self.pos_cont_attrs = [[] for x in xrange(11)]
        self.neg_cont_attrs = [[] for x in xrange(11)]

        self.pos_frequency = [{} for x in xrange(14)]
        self.neg_frequency = [{} for x in xrange(14)]
        self.dsc_attr_values = [[] for x in xrange(14)]
        with open(file_name, 'r') as file:
            feature = []
            for line in file:
                line = line.rstrip('\n')
                feature = line.split(',')
                if attr_titles is None:
                    attr_titles = feature
                else:
                    class_label = feature[0]
                    self.cl.append(class_label)
                    cont_attrs = feature[16:24]
                    cont_attrs.insert(0, feature[12])
                    cont_attrs.append(feature[29])
                    cont_attrs.append(feature[31])
                    dsc_attrs = feature[2:12]
                    dsc_attrs.append(feature[13])
                    dsc_attrs.append(feature[14])
                    dsc_attrs.append(feature[15])
                    dsc_attrs.append(feature[30])

                    if class_label == '0':
                        self.neg_cnt += 1
                        for k in range(len(cont_attrs)):
                            self.neg_cont_attrs[k].append(float(cont_attrs[k]))
                        for k in range(len(dsc_attrs)):
                            self.dsc_attr_values[k].append(dsc_attrs[k])
                            self.neg_frequency[k][dsc_attrs[k]] = self.neg_frequency[k].get(dsc_attrs[k], 0) + 1
                    else:
                        self.pos_cnt += 1
                        for k in range(len(cont_attrs)):
                            self.pos_cont_attrs[k].append(float(cont_attrs[k]))
                        for k in range(len(dsc_attrs)):
                            self.dsc_attr_values[k].append(dsc_attrs[k])
                            self.pos_frequency[k][dsc_attrs[k]] = self.pos_frequency[k].get(dsc_attrs[k], 0) + 1
                    self.Num += 1

        # print("self.Num: ", self.Num)
        self.p_pos = math.log(self.pos_cnt / float(self.Num))
        self.p_neg = math.log(self.neg_cnt / float(self.Num))
        self.p_pos_attr = []
        self.p_neg_attr = []
        # print("self.p_pos: ", self.p_pos)
        # print("self.p_neg: ", self.p_neg)

        for i in range(len(self.dsc_attr_values)):
            self.dsc_attr_values[i] = set(self.dsc_attr_values[i])

        for i in range(len(self.pos_frequency)):
            d = {}
            denom = float(self.pos_cnt) + len(self.dsc_attr_values[i])
            for key in self.dsc_attr_values[i]:
                num = 1 + self.pos_frequency[i].get(key, 0)  # laplacian correction
                # d[key] = (num / float(denom))
                d[key] = math.log(num / float(denom))
            self.p_pos_attr.append(d)
        for i in range(len(self.neg_frequency)):
            d = {}
            denom = float(self.neg_cnt) + len(self.dsc_attr_values[i])
            for key in self.dsc_attr_values[i]:
                num = 1 + self.neg_frequency[i].get(key, 0)  # laplacian correction
                d[key] = math.log(num / float(denom))
                # d[key] = (num / float(denom))
            self.p_neg_attr.append(d)

        # continuous values
        self.mean = {}
        self.std = {}
        self.mean[1] = np.mean(self.pos_cont_attrs)
        self.mean[0] = np.mean(self.neg_cont_attrs)
        self.std[0] = np.std(self.neg_cont_attrs)
        self.std[1] = np.std(self.pos_cont_attrs)
        # print (self.mean)
        # print (self.std)

if __name__ == '__main__':
    if len(sys.argv) != 2:
            print("Format:python NaiveBayes.py")
            sys.exit()
    
    name = sys.argv[1]
    training_file= "data\\train_clean.csv"
    testing_file = "data\\test_clean.csv"

    nb = NaiveBayes()
    nb.trainClassifier(training_file)               #Train the classifier
    nb.runClassifier(testing_file)                  # Run  the classifier
