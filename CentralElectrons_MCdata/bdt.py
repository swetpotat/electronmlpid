import tensorflow as tf
import tensorflow.contrib.tensor_forest.python as tensor_forest

from ROOT import *
import numpy as np


# Open ROOT data files - signal, background, weights

sfile = TFile('/home/pche3675/summer2018/electronmlpid/CentralElectrons_MCdata/data/MC_SigElectrons_2000000ev.root')
bfile = TFile('/home/pche3675/summer2018/electronmlpid/CentralElectrons_MCdata/data/MC_BkgElectrons_2000000ev.root')
wfile = TFile('/home/pche3675/summer2018/electronmlpid/CentralElectrons_MCdata/data/weights.root')

# Retrieve ntuples

stree = sfile.Get('data')
snentries = stree.GetEntries()
btree = bfile.Get('data')
bnentries = btree.GetEntries()
wtree = wfile.Get('weights')

# Fill numpy arrays with data

sdata = np.zeros((snentries, 14), dtype = float)
sweights = np.zeros(snentries, dtype = float)

for i in range(snentries):
	
	stree.LoadTree(i)
	sentry = stree.GetEntry(i)
	sdata[i, 0] = i
	sdata[i, 1] = stree.p_numberOfInnermostPixelHits
	sdata[i, 2] = stree.p_numberOfPixelHits
	sdata[i, 3] = stree.p_numberOfSCTHits
	sdata[i, 4] = stree.p_d0
	sdata[i, 5] = stree.p_d0Sig
	sdata[i, 6] = stree.p_dPOverP
	sdata[i, 7] = stree.p_deltaEta1
	sdata[i, 8] = stree.p_deltaPhiRescaled2
	sdata[i, 9] = stree.p_EptRatio
	sdata[i, 10] = stree.p_TRTPID
	sdata[i, 11] = stree.p_numberOfTRTHits
	sdata[i, 12] = stree.p_TRTTrackOccupancy
	sdata[i, 13] = stree.p_numberOfTRTXenonHits

	wtree.LoatTree(i)
	wentry = wtree.GetEntry(i)
	sweights[i] = wtree.sig_weights

bdata = np.zeros((bnentries, 14), dtype = float)
bweights = np.zeros(bnentries, dtype = float)

for i in range(bnentries):

	btree.LoadTree(i)
	bentry = btree.GetEntry(i)
	bdata[i, 0] = i
	bdata[i, 1] = btree.p_numberOfInnermostPixelHits
	bdata[i, 2] = btree.p_numberOfPixelHits
	bdata[i, 3] = btree.p_numberOfSCTHits
	bdata[i, 4] = btree.p_d0
	bdata[i, 5] = btree.p_d0Sig
	bdata[i, 6] = btree.p_dPOverP
	bdata[i, 7] = btree.p_deltaEta1
	bdata[i, 8] = btree.p_deltaPhiRescaled2
	bdata[i, 9] = btree.p_EptRatio
	bdata[i, 10] = btree.p_TRTPID
	bdata[i, 11] = btree.p_numberOfTRTHits
	bdata[i, 12] = btree.p_TRTTrackOccupancy
	bdata[i, 13] = btree.p_numberOfTRTXenonHits

# Parameters
num_trees = 200
num_steps = 100
max_depth = 4
num_classes = 2
num_features = 13
batch_size = 46000

# Create tensor placeholders for input and target data
X = tf.placeholder(tf.float32, shape = [None, num_features])
Y = tf.placeholder(tf.int32, shape = [None])
	
# Random Forest Parameters
params = tensor_forest.ForestHParams(num_classes = num_classes,
									 num_features = num_features,
									 max_depth = max_depth,
									 num_trees = num_trees).fill()

# Build Random Forest






