import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.metrics import accuracy_score, confusion_matrix


# Define features used for training
features = ['p_etcone20',
	    'p_etcone30',
	    'p_etcone40',
	    'p_etcone20ptCorrection',
	    'p_etcone30ptCorrection',
	    'p_etcone40ptCorrection',
	    'p_ptcone20',
	    'p_ptcone30',
	    'p_ptcone40']


def collect_train_data():

	# Read in data and weight files
	datafile_training = pd.read_csv('data/MC_data_2000000ev.csv')
	weightfile = pd.read_csv('data/weights.csv')

	# Extract relevant data sample, target variables and weights
	training_data = datafile_training[features]
	training_targets = datafile_training.Truth
	weights = weightfile.weights

	# Convert dataframes to numpy arrays
	training_data = training_data.values
	training_targets = training_targets.values
	weights = weights.values

	return training_data, training_targets, weights


def collect_test_data():

	# Read in data
	datafile_testing = pd.read_csv('data/MC_data_500000ev.csv')

	# Extract relevant data sample and target variables
	testing_data = datafile_testing[features]
	testing_targets = datafile_testing.Truth
	
	# Convert dataframes to numpy arrays
	testing_data = testing_data.values
	testing_targets = testing_targets.values

	return testing_data, testing_targets


def train(training_data, training_targets, weights):
	
	# Make Random Forest
	rf = RF(n_estimators = 200, max_depth = 8, min_samples_split = 4)

	print("Random Forest made. Now training following model...")
	print(rf)

	# Fit Random Forest
	rf.fit(training_data, training_targets, weights)
	
	return rf


def test(rf, testing_data):
	
	print("Training finished. Test me!")
	print("If you insist! Testing model...")

	predictions = rf.predict(testing_data)

	return predictions 


def main():

	training_data, training_targets, weights = collect_train_data()
	rf = train(training_data, training_targets, weights)

	testing_data, testing_targets = collect_test_data()
	predictions = test(rf, testing_data)

	print("Training accuracy: " + str(accuracy_score(training_targets, rf.predict(training_data))))
	print("Testing accuracy: " + str(accuracy_score(testing_targets, predictions)))
	print("Confusion matrix: ")
	print(confusion_matrix(testing_targets, predictions))	


if __name__ == "__main__":
	main()

