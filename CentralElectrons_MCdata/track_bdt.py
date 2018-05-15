import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.metrics import accuracy_score, confusion_matrix, auc, roc_curve


# Define features used for training
features = ['p_numberOfInnermostPixelHits',
	    'p_numberOfPixelHits',
	    'p_numberOfSCTHits',
	    'p_d0',
	    'p_d0Sig',
	    'p_dPOverP',
	    'p_deltaEta1',
	    'p_deltaPhiRescaled2',
	    'p_EptRatio',
	    'p_TRTPID']


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
	
	print("Training finished. Test me!")
	print("If you insist! Testing model...")

	predictions = rf.predict(testing_data)

	return predictions 


def plot_confusion_matrix(testing_targets, predictions):

	cm = confusion_matrix(testing_targets, predictions)
	df_cm = pd.DataFrame(cm, index = ['Signal', 'Background'], columns = ['Signal', 'Background'])
	plt.figure(figsize = (8,5))
	sn.heatmap(df_cm, annot = True, cmap = 'Blues', fmt = 'g')
	plt.title('Confusion Matrix for Track Features')
	plt.ylabel('Predicted Class')
	plt.xlabel('Actual Class')
	plt.savefig('cm_track.png', bbox_inches = 'tight')


def plot_roc_curve(testing_targets, predictions):
	
	fpr, tpr, _ = roc_curve(testing_targets, predictions)
	roc_auc = auc(tpr, fpr)
	plt.figure(figsize = (8,5))
	plt.title('ROC for Track Features')
	interp_range = range(0,1,0.05)
	interp_values = plt.spline(tpr, fpr, interp_range)
	plt.plot(tpr, fpr, 'b', interp_range, interp_values, label = 'AUC = %0.2f'% roc_auc)
	plt.legend(loc = 'lower right')
	plt.xlim([0, 1])
	plt.ylim([0, 1])
	plt.xlabel('Signal Efficiency')
	plt.ylabel('Background Acceptance')
	plt.savefig('roc_track.png', bbox_inches = 'tight')
			


def main():

	training_data, training_targets, weights = collect_train_data()
	rf = train(training_data, training_targets, weights)

	testing_data, testing_targets = collect_test_data()
	predictions = test(rf, testing_data)

	print("Training accuracy: " + str(accuracy_score(training_targets, rf.predict(training_data))))
	print("Testing accuracy: " + str(accuracy_score(testing_targets, predictions)))

	# Plot confusion matrix and ROC
	plot_confusion_matrix(testing_targets, predictions)
	plot_roc_curve(testing_targets, predictions)

if __name__ == "__main__":
	main()

