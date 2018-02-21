The following is an explanation of the naming scheme used to label the data files that are
output from TMVA. These root files do not contain all relevant plots. Instead, these can be
obtained by using the TMVAGui macros available in root. 

The following command (once root has been opened) will allow you to call up the gui that was
produced when originally running the script: TMVA::TMVAGui("myfile.root"); 

#################################################################################################
# NEURAL NETWORKS
#################################################################################################


- General naming scheme: MLP_LEARNINGMETHOD_TRAININGMETHOD_track/calo/iso.root

MLP_STOCH_BP_*.root ====> learning method = stochastic, training method = backpropogation


#################################################################################################
# BOOSTED DECISION TREES
#################################################################################################


- General naming scheme: BDT_LEARNINGMETHOD_TRAININGMETHOD_track/calo/iso.root

BDT_AD_GI_*.root ====> learning method = adaptive boost, training method = GiniIndex 
BDT_BAG_GI_*.root ====> learning method = bagging, training method = GiniIndex
BDT_GR_GI_*.root ====> learning method = gradient boost, training method = GiniIndex
BDT_AD_CR_*.root ====> learning method = adaptive boost, training method = CrossEntropy
BDT_BAG_CR_*.root ====> learning method = bagging, training method = CrossEntropy
BDT_GR_CR_.*root ====> learning method = gradient boost, training method = CrossEntropy
