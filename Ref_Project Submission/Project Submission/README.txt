adadecisiontree: class for adaboosting decision tree.
adadtmain: main file for running adaboosting decision tree
attributeselectionmethod: functions for various attribute selection methods
decisiontree: class for decision tree
dtmain: mainfile for running adaboosting decision tree
preprocess: functions for reading data, attribute types and possible values
NaiveBayes: class for Naive Bayes classification algorithm.

First, please change the directory to source code folder, then execute the following:

Please use: 'python adadtmain.py imbalance_coef max_iteration output_file_name' to run the adaboosting decision tree. The recommended parameter is imbalance_coef = 1.4, max_teration = 5. An output file will be generated with all probability prediction in columns. It can be copy and paste into the score.csv file for submission.

Please use: 'python dtmain.py max_depth output_file_name' to run the decision tree algo. The recommended paramter is max_depth = 3. An output file with 0-1 prediction will be generated.

Please use: 'python NaiveBayes.py' to run the Naive Bayes algorithm. An output file (nb_output.txt) is generated whose values can be copy and pasted in score.csv file for submission.