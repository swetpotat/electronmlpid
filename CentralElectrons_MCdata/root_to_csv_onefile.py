#!/usr/bin/env python

from ROOT import *
import sys
from time import time
import math
import numpy
import pandas as pd
import numpy as np


# If you want to add variables you need to do two things: 
#	add the variable's name as a string in the vector name
#	add the variable in the vector helper in the function makeVector by intree.VARIABLE_NAME_IN_ROOT_FILE
# Note, the order of name and helper needs to be the same, and there are four helper that needs to be changed. 
# If you add a new variable in the end of helper, it needs to be in the end of name.

name = ["p_Rhad1" ,
		"p_Rhad" ,
		"p_f3" ,
		"p_weta2" ,
		"p_Rphi" ,
		"p_Reta" ,
		"p_Eratio" ,
		"p_f1" ,
		"p_eta" ,
		"p_ptPU30" ,
		"averageInteractionsPerCrossing" ,

		"p_etcone20" ,
		"p_etcone30" ,
		"p_etcone40" ,
		"p_etcone20ptCorrection" ,
		"p_etcone30ptCorrection" ,
		"p_etcone40ptCorrection" ,
		"p_ptcone20" ,
		"p_ptcone30" ,
		"p_ptcone40" ,
		
		"p_numberOfInnermostPixelHits" ,
		"p_numberOfPixelHits" ,
		"p_numberOfSCTHits" ,
		"p_d0" , 
		"p_d0Sig" ,
		"p_dPOverP" ,
		"p_deltaEta1" ,
		"p_deltaPhiRescaled2" ,
		"p_EptRatio" ,
		"p_TRTPID" ,
		"p_numberOfTRTHits" ,
		"p_TRTTrackOccupancy" ,
		"p_numberOfTRTXenonHits",
		
		"Z_m",
		"p_LHValue",
		"p_et_calo",

		# MVA stuff
		"mva_Calo_kBDT_conf1_mc",
		"mva_Iso_kBDT_conf1_mc",
		"mva_Track_kBDT_conf1_mc",
		"mva_kBDT_conf1_mc_final",

		"label0" ,
		"label1",
		"p_TruthType",
		"Truth"]


def find_bin( value , vector ) :
	#needs an extra bin for values larger than what im interested in
	bin_number = 0
	for i in range(len(vector)) :
		if (value<vector[i+1]) :
			bin_number = i
			return bin_number

cutlist_et          = [ 0. , 20000. , 30000. , 40000. , 50000. , 7000000. ]
cutlist_eta         = [ 0. , 0.8, 1.37 , 1.52 , 2.01 , 2.47 ]

def in_or_out(weight , r):
	frac, whole = math.modf(weight)
	extra = 0
	if (r<frac):
		extra = 1
	return (extra+whole) 


def makeVector( vec , labeltype_sig, labeltype_bkg , infilesig , infilebkg , weight_conf , type_data,filetype) :
	
	#SIG
	intree = infilesig.Get("tree")
	nentries = intree.GetEntries()
	nentries_1percent = nentries/100

	#random = np.random.rand(nentries)


	for ientry in range( nentries ) : #nentries
		if intree.GetEntry( ientry ) < 0 : break
		lh          = intree.p_LHValue
		et_temp     = intree.p_et_calo
		eta_temp    = intree.p_eta
		eta_temp    = abs(eta_temp)
		Z_mass      = intree.Z_m
		mu_temp     = intree.averageInteractionsPerCrossing

		Truth 		= int(intree.p_TruthType)

		if (eta_temp > 2.47): continue
		if ( (abs(intree.Z_m - 91188.) > 50000.) ): continue
		#if (mu_temp < 11.5 ): continue
		#if (mu_temp > 39.5): continue

		#eta_bin     = find_bin( eta_temp , cutlist_eta)
		#et_bin      = find_bin( et_temp , cutlist_et)

		#if (ientry<100):
			#print eta_bin,et_bin
			#print eta_temp , et_temp

		if (filetype==0):
			if (Truth==2): Truth = 1
			if (Truth!=2): Truth = 0
			helper = [      intree.p_Rhad1 ,
							intree.p_Rhad ,
							intree.p_f3 ,
							intree.p_weta2 ,
							intree.p_Rphi ,
							intree.p_Reta ,
							intree.p_Eratio ,
							intree.p_f1 ,
							intree.p_eta ,
							intree.p_ptPU30 ,
							intree.averageInteractionsPerCrossing ,

							intree.p_etcone20 ,
							intree.p_etcone30 ,
							intree.p_etcone40 ,
							intree.p_etcone20ptCorrection ,
							intree.p_etcone30ptCorrection ,
							intree.p_etcone40ptCorrection ,
							intree.p_ptcone20 ,
							intree.p_ptcone30 ,
							intree.p_ptcone40 ,
							
							intree.p_numberOfInnermostPixelHits ,
							intree.p_numberOfPixelHits ,
							intree.p_numberOfSCTHits ,
							intree.p_d0 , 
							intree.p_d0Sig ,
							intree.p_dPOverP ,
							intree.p_deltaEta1 ,
							intree.p_deltaPhiRescaled2 ,
							intree.p_EptRatio,
							intree.p_TRTPID ,
							intree.p_numberOfTRTHits ,
							intree.p_TRTTrackOccupancy ,
							intree.p_numberOfTRTXenonHits,

							# other
							intree.Z_m,
							intree.p_LHValue,
							intree.p_et_calo,

							# MVA stuff
							intree.mva_Calo_kBDT_conf1_mc,
							intree.mva_Iso_kBDT_conf1_mc,
							intree.mva_Track_kBDT_conf1_mc,
							intree.mva_kBDT_conf1_mc_final,


							1,
							0,
							intree.p_TruthType,
							Truth ]
		if (filetype==1):
			if (Truth==2): Truth = 1
			if (Truth!=2): Truth = 0
			helper = [      intree.p_Rhad1 ,
							intree.p_Rhad ,
							intree.p_f3 ,
							intree.p_weta2 ,
							intree.p_Rphi ,
							intree.p_Reta ,
							intree.p_Eratio ,
							intree.p_f1 ,
							intree.p_eta ,
							intree.p_ptPU30 ,
							intree.averageInteractionsPerCrossing ,

							intree.p_etcone20 ,
							intree.p_etcone30 ,
							intree.p_etcone40 ,
							intree.p_etcone20ptCorrection ,
							intree.p_etcone30ptCorrection ,
							intree.p_etcone40ptCorrection ,
							intree.p_ptcone20 ,
							intree.p_ptcone30 ,
							intree.p_ptcone40 ,
							
							intree.p_numberOfInnermostPixelHits ,
							intree.p_numberOfPixelHits ,
							intree.p_numberOfSCTHits ,
							intree.p_d0 , 
							intree.p_d0Sig ,
							intree.p_dPOverP ,
							intree.p_deltaEta1 ,
							intree.p_deltaPhiRescaled2 ,
							intree.p_EptRatio,
							intree.p_TRTPID ,
							intree.p_numberOfTRTHits ,
							intree.p_TRTTrackOccupancy ,
							intree.p_numberOfTRTXenonHits,

							# other
							intree.Z_m,
							intree.p_LHValue,
							intree.p_et_calo,

							# MVA stuff
							intree.mva_Calo_kBDT_conf1_mc,
							intree.mva_Iso_kBDT_conf1_mc,
							intree.mva_Track_kBDT_conf1_mc,
							intree.mva_kBDT_conf1_mc_final,

							intree.mva_Calo_kBDT_conf1_data,
							intree.mva_Iso_kBDT_conf1_data,
							intree.mva_Track_kBDT_conf1_data,
							intree.mva_kBDT_conf1_data_final,

							intree.p_datadata_weight,
							1,
							0,
							intree.p_TruthType ,
							Truth]
		
	if (ientry<10):
		print len(helper)
		print helper
	vec.append(helper)
	if ( ientry%nentries_1percent == 0) :
		print '\rCompleted %5.0f. Parsed entries: %7.0f.' % (100*(ientry+1)/nentries , ientry )
	infilesig.Close()

	#BKG
	intree = infilebkg.Get("tree")
	nentries = intree.GetEntries()
	nentries_1percent = nentries/100

	#random = np.random.rand(nentries)


	for ientry in range( nentries ) : 
		if intree.GetEntry( ientry ) < 0 : break

		lh          = intree.p_LHValue
		et_temp     = intree.p_et_calo
		eta_temp    = intree.p_eta
		eta_temp_w  = intree.p_eta
		eta_temp    = abs(eta_temp)
		Z_mass      = intree.Z_m
		mu_temp     = intree.averageInteractionsPerCrossing

		Truth 		= int(intree.p_TruthType)

		if (eta_temp > 2.47): continue
		if ( (abs(intree.Z_m - 91188.) > 50000.) ): continue
		#if (mu_temp < 11.5 ): continue
		#if (mu_temp > 39.5): continue

		#eta_bin     = find_bin( eta_temp , cutlist_eta)
		#et_bin      = find_bin( et_temp , cutlist_et)

		#if (ientry<100):
		# 	print eta_bin,et_bin

		if (filetype==0):
			if (Truth==2): Truth = 1
			if (Truth!=2): Truth = 0
			helper = [      intree.p_Rhad1 ,
							intree.p_Rhad ,
							intree.p_f3 ,
							intree.p_weta2 ,
							intree.p_Rphi ,
							intree.p_Reta ,
							intree.p_Eratio ,
							intree.p_f1 ,
							intree.p_eta ,
							intree.p_ptPU30 ,
							intree.averageInteractionsPerCrossing ,

							intree.p_etcone20 ,
							intree.p_etcone30 ,
							intree.p_etcone40 ,
							intree.p_etcone20ptCorrection ,
							intree.p_etcone30ptCorrection ,
							intree.p_etcone40ptCorrection ,
							intree.p_ptcone20 ,
							intree.p_ptcone30 ,
							intree.p_ptcone40 ,
							
							intree.p_numberOfInnermostPixelHits ,
							intree.p_numberOfPixelHits ,
							intree.p_numberOfSCTHits ,
							intree.p_d0 , 
							intree.p_d0Sig ,
							intree.p_dPOverP ,
							intree.p_deltaEta1 ,
							intree.p_deltaPhiRescaled2 ,
							intree.p_EptRatio,
							intree.p_TRTPID ,
							intree.p_numberOfTRTHits ,
							intree.p_TRTTrackOccupancy ,
							intree.p_numberOfTRTXenonHits,

							# other
							intree.Z_m,
							intree.p_LHValue,
							intree.p_et_calo,

							# MVA stuff
							intree.mva_Calo_kBDT_conf1_mc,
							intree.mva_Iso_kBDT_conf1_mc,
							intree.mva_Track_kBDT_conf1_mc,
							intree.mva_kBDT_conf1_mc_final,

							0,
							1,
							intree.p_TruthType,
							Truth ]
		if (filetype==1):
			if (Truth==2): Truth = 1
			if (Truth!=2): Truth = 0
			helper = [      intree.p_Rhad1 ,
							intree.p_Rhad ,
							intree.p_f3 ,
							intree.p_weta2 ,
							intree.p_Rphi ,
							intree.p_Reta ,
							intree.p_Eratio ,
							intree.p_f1 ,
							intree.p_eta ,
							intree.p_ptPU30 ,
							intree.averageInteractionsPerCrossing ,

							intree.p_etcone20 ,
							intree.p_etcone30 ,
							intree.p_etcone40 ,
							intree.p_etcone20ptCorrection ,
							intree.p_etcone30ptCorrection ,
							intree.p_etcone40ptCorrection ,
							intree.p_ptcone20 ,
							intree.p_ptcone30 ,
							intree.p_ptcone40 ,
							
							intree.p_numberOfInnermostPixelHits ,
							intree.p_numberOfPixelHits ,
							intree.p_numberOfSCTHits ,
							intree.p_d0 , 
							intree.p_d0Sig ,
							intree.p_dPOverP ,
							intree.p_deltaEta1 ,
							intree.p_deltaPhiRescaled2 ,
							intree.p_EptRatio,
							intree.p_TRTPID ,
							intree.p_numberOfTRTHits ,
							intree.p_TRTTrackOccupancy ,
							intree.p_numberOfTRTXenonHits,

							# other
							intree.Z_m,
							intree.p_LHValue,
							intree.p_et_calo,

							# MVA stuff
							intree.mva_Calo_kBDT_conf1_mc,
							intree.mva_Iso_kBDT_conf1_mc,
							intree.mva_Track_kBDT_conf1_mc,
							intree.mva_kBDT_conf1_mc_final,

							intree.mva_Calo_kBDT_conf1_data,
							intree.mva_Iso_kBDT_conf1_data,
							intree.mva_Track_kBDT_conf1_data,
							intree.mva_kBDT_conf1_data_final,

							intree.p_datadata_weight,
							0,
							1,
							intree.p_TruthType,
							Truth ]
		if (ientry<10):
			print len(helper)
			print helper

		vec.append(helper)
		if ( ientry%nentries_1percent == 0) :
			print '\rCompleted %5.0f. Parsed entries: %7.0f.' % (100*(ientry+1)/nentries , ientry )
	infilebkg.Close()


	return vec



Sig_Files = [   #"/hep/nperez/storage/Data/Split_1M_A_EGAM1.root_w_mcmc_mcmcfinal_mcdata_mcdatafinal" ,
				#"/hep/nperez/storage/Data/Split_18M_A_EGAM1.root_w_LH_mm_mmf_md_mdf" ,
				#"/hep/nperez/storage/Data/Split_5M_B_EGAM1.root_w_LH_mm_mmf_md_mdf_dd_ddf" ,
				#"/hep/nperez/storage/Data/Split_5M_A_EGAM1.root_w_LH_mm_mmf_md_mdf_dd_ddf" ]
				"/hep/nperez/storage/MC/Split_2M_A_Signal_Zee.root_w_LH_mm_mmf" ,
				"/hep/nperez/storage/MC/Split_0.5M_A_Signal_Zee.root_w_LH_mm_mmf"]
				#"/hep/nperez/storage/MC/Split_2M_A_Signal_Zee.root_w_mcmc_mcmcfinal_mcdata_mcdatafinal" ,
				#"/hep/nperez/storage/MC/Split_0.5M_A_Signal_Zee.root_w_mcmc_mcmcfinal_mcdata_mcdatafinal"]

Bkg_Files = [   "/hep/nperez/storage/MC/Split_2M_A_Background_mix.root_w_LH_mm_mmf" ,
				"/hep/nperez/storage/MC/Split_0.5M_A_Background_mix.root_w_LH_mm_mmf"]
				#"/hep/nperez/storage/Data/Split_18M_A_EGAM7.root_w_LH_mm_mmf_md_mdf" ,
				#"/hep/nperez/storage/Data/Split_5M_B_EGAM7.root_w_LH_mm_mmf_md_mdf_dd_ddf" ,
				#"/hep/nperez/storage/Data/Split_5M_A_EGAM7.root_w_LH_mm_mmf_md_mdf_dd_ddf" ]

print len(Sig_Files)

csv_file_name = [ "MC2_" , "MC05_" , "Data5A_" ]
#csv_file_name = [ "Data18_" , "Data5A_" , "Data5B_" ]
weight_conf	= [0,0,0,0,0,0,1,1]
type_data	= [0,0,0,0,1,1,2,2]
weight_conf     = [0,0,0]
type_data       = [0,0,0]


# 0 for MC and 1 for data
# In data, the data trained BDT values are saved as well. 
filetype        = [0,0,1]

ifile = int(sys.argv[1]) - 1 

vec = []

#if (type_data[ifile]==0): continue;
infile_sig = TFile(Sig_Files[ifile], "READ")
infile_bkg = TFile(Bkg_Files[ifile], "READ")
vec = makeVector( vec , 1 , 0 , infile_sig , infile_bkg , weight_conf[ifile] , type_data[ifile] ,filetype[ifile])

string = csv_file_name[ifile] + ".csv"
print string
numpy.savetxt(str("/hep/nperez/storage/CSV/"+string), vec, delimiter="," )

print len(name)

#Reads the numpy txt with pandas
df_train  = pd.read_csv("/hep/nperez/storage/CSV/" + csv_file_name[ifile] +".csv" , names = name ) #, names = name

#Saves the data frame with header (Variable names)
df_train.to_csv( str("/hep/nperez/storage/CSV/" + csv_file_name[ifile] +".csv") , index=False)

