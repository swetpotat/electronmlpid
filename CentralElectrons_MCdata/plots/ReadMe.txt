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
MLP_STOCH_BFGS_*.root ====> learning method = stochastic, training method = BFGS



#################################################################################################
# BOOSTED DECISION TREES
#################################################################################################


- General naming scheme: BDT_LEARNINGMETHOD_TRAININGMETHOD_track/calo/iso.root

BDT_AD_GI_*.root ====> learning method = adaptive boost, training method = GiniIndex 
