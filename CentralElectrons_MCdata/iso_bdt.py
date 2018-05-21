import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sn
from scipy.interpolate import spline

from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, roc_auc_score


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
	rf = RF(n_estimators = 200, max_depth = 4, min_samples_split = 4)

	print("Random Forest made. Now training following model...")
	print(rf)

	# Fit Random Forest
	rf.fit(training_data, training_targets, weights)
	
	return rf


def test(rf, testing_data):
	
	print("Training finished. Testing model...!")

	probabilities = rf.predict_proba(testing_data)[:,1]
	predictions = rf.predict(testing_data)

	return predictions, probabilities 


def plot_confusion_matrix(testing_targets, predictions):

	cm = confusion_matrix(testing_targets, predictions)
	df_cm = pd.DataFrame(cm, index = ['Signal', 'Background'], columns = ['Signal', 'Background'])
	plt.figure(figsize = (8,5))
	sn.heatmap(df_cm, annot = True, cmap = 'Blues', fmt = 'g')
	plt.title('Confusion Matrix for Isolation Features')
	plt.ylabel('Predicted Class')
	plt.xlabel('Actual Class')
	plt.savefig('cm_iso.pdf', bbox_inches = 'tight')

	print("Signal purity: " + str(cm[1,1]/(cm[1,1]+cm[1,0])))
	print("Background purity: " + str(cm[0,0]/(cm[0,0]+cm[0,1])))


def plot_roc_curve(testing_targets, probabilities):
	
	fpr, tpr, thresholds = roc_curve(testing_targets, probabilities, pos_label = 1)
	area = roc_auc_score(testing_targets, probabilities)
	plt.figure(figsize = (8,5))
	plt.plot(fpr, tpr, 'b', label = 'AUC = %0.5f'% area)
	plt.title('ROC for Isolation Features')
	plt.legend(loc = 'lower right')
	plt.xlim([0, 1])
	plt.ylim([0, 1])
	plt.xlabel('Signal Efficiency')
	plt.ylabel('Background Acceptance')
	plt.savefig('roc_iso.pdf', bbox_inches = 'tight')
		
	print('ROC AUC = %0.5f'% area)
	
	return fpr, tpr


def main():

	training_data, training_targets, weights = collect_train_data()
	testing_data, testing_targets = collect_test_data()
	
	rf = train(training_data, training_targets, weights)
	predictions, probabilities = test(rf, testing_data)

	# Plot confusion matrix and ROC
	plot_confusion_matrix(testing_targets, predictions)
	fpr, tpr = plot_roc_curve(testing_targets, probabilities)
	
	print("Training accuracy: " + str(accuracy_score(training_targets, rf.predict(training_data))))
	print("Testing accuracy: " + str(accuracy_score(testing_targets, predictions)))


if __name__ == "__main__":
	main()

