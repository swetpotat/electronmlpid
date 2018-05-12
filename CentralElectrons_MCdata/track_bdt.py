import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier as RF


# Read in data and weight files
datafile = pd.read_csv('data/MC_data_2000000ev.csv')
weightfile = pd.read_csv('data/weights.csv')

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


# Extract relevant data sample, target variables and weights
data = datafile[features]
temp_targets = datafile.Truth
temp_weights = weightfile.weights

# Define Random Forest variables
n_estimators = 200
max_depth = 4
min_samples_split = 4

# Make Random Forest
rf = RF(n_estimators, max_depth, min_samples_split)

print("Random Forest made. Now fitting...")

data = data.values
targets = []
weights = []

for i in range(2723931):
	targets.append(temp_targets[i])
	weights.append(temp_weights[i])

# Fit Random Forest
rf.fit(data, targets, weights)

print("Training finished. Test me!")
