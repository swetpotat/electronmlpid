import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from scipy.interpolate import spline

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


def train(training_data, training_targets, weights, testing_data):
	
	# Make Random Forest
	rf = RF(n_estimators = 200, max_depth = 4, min_samples_split = 4)

	print("Random Forest made. Now training following model...")
	print(rf)

	# Fit Random Forest
	pred = rf.fit(training_data, training_targets, weights).predict_proba(testing_data)[:,1]
	
	return rf, pred


def test(rf, testing_data):
	
	print("Training finished. Testing model...")

	prob_predictions = rf.predict_proba(testing_data)
	#predictions = rf.predict(testing_data)

	return prob_predictions


def plot_confusion_matrix(testing_targets, predictions):

	cm = confusion_matrix(testing_targets, predictions)
	df_cm = pd.DataFrame(cm, index = ['Signal', 'Background'], columns = ['Signal', 'Background'])
	plt.figure(figsize = (8,5))
	sn.heatmap(df_cm, annot = True, cmap = 'Blues', fmt = 'g')
	plt.title('Confusion Matrix for Track Features')
	plt.ylabel('Predicted Class')
	plt.xlabel('Actual Class')
	plt.savefig('cm_track.pdf', bbox_inches = 'tight')


def plot_roc_curve(testing_targets, probabilities):
	
	#fpr, tpr, _ = roc_curve(testing_targets, probabilities)
	#roc_auc = auc(tpr, fpr)
	#interp_range = np.linspace(0,1,100)
	#interp_values = spline(tpr, fpr, interp_range)
	fpr, tpr, thresholds = roc_curve(testing_targets, probabilities, pos_label = 1)
	plt.figure(figsize = (8,5))
	plt.plot(fpr, tpr)
	#plt.plot(interp_range, interp_values, 'b', label = 'AUC = %0.2f'% roc_auc)
	#plt.title('ROC for Track Features')
	#plt.legend(loc = 'lower right')
	print("Here")
	plt.xlim([0, 1])
	plt.ylim([0, 1])
	plt.xlabel('Signal Efficiency')
	plt.ylabel('Background Acceptance')
	plt.savefig('roc_track.pdf', bbox_inches = 'tight')
			


def main():

	training_data, training_targets, weights = collect_train_data()
	testing_data, testing_targets = collect_test_data()
	rf, pred = train(training_data, training_targets, weights, testing_data)

	#prob_predictions = test(rf, testing_data)

	#print("Training accuracy: " + str(accuracy_score(training_targets, rf.predict(training_data))))
	#print("Testing accuracy: " + str(accuracy_score(testing_targets, predictions)))

	# Plot confusion matrix and ROC
	#plot_confusion_matrix(testing_targets, predictions)
	plot_roc_curve(testing_targets, pred)

if __name__ == "__main__":
	main()

