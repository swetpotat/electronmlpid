#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########################################################
#
# Fill, display and save a set of histograms of event
# variables stored in a tree derived from a Belle II
# analysis.
#
# Contributors: K. Varvell (August 2017)
#               modifying script of D. Schjelderup (June 2017)
#
###########################################################

from ROOT import TFile, gDirectory
# You probably also want to import TH1D,
# unless you're not making any histograms.
from ROOT import TH1D
from ROOT import TH2D
from ROOT import TCanvas
from ROOT import TPad
from ROOT import TMath
from ROOT import gStyle

from modularAnalysis import printROEInfo

import helpers

# Open the input root file. 

myfile = TFile( "data/MC_SigBkgElectrons_2000000ev.root" )

# Retrieve the n-tuple of interest. In this case, the n-tuple's name is
# "bsig". You may have to use the TBrowser to find the name of the
# n-tuple that someone gives you.
mychain = gDirectory.Get( 'data' )
entries = mychain.GetEntriesFast()

### --------------------------------------------------------------------------
### The Set-up code goes here.
### --------------------------------------------------------------------------

# Creating dictionary of histograms

histograms = {}
histograms["Z_m"]=helpers.defineHistogram("Z_m",'Mass of Z Boson',101, 90999, 91001)
histograms['LHValue']=helpers.defineHistogram('p_LHValue',"Likelihood Value",101, -4, 2)
histograms['et_calo']=helpers.defineHistogram('p_et_calo',"Transverse Energy of Electron",101, 0, 100)
histograms['mva_Track_kBDT_conf1_mc']=helpers.defineHistogram('p_mva_Track_kBDT_conf1_mc',"BDT Score for Track Variables",101, -0.7, 0.5)
histograms['mva_Iso_kBDT_conf1_mc']=helpers.defineHistogram('p_mva_Iso_kBDT_conf1_mc',"BDT Score for Isolation Variables",101, -0.7, 0.5)
histograms['mva_Calo_kBDT_conf1_mc']=helpers.defineHistogram('p_mva_Calo_kBDT_conf1_mc',"BDT Score for Calorimeter Variables",101, -0.7, 0.5)
histograms['mva_kBDT_conf1_mc_final']=helpers.defineHistogram('p_mva_kBDT_conf1_mc_final',"Fisher Combination of BDT's",101, -9, 4)
histograms['label0']=helpers.defineHistogram('label0',"File Indicator",101, 0, 1)
histograms['label1']=helpers.defineHistogram('label1',"File Indicator",101, 0, 1)
histograms['TruthType']=helpers.defineHistogram('p_TruthType',"Electron Candidate Matches",101, 0, 18)
histograms['Truth']=helpers.defineHistogram('Truth',"Truth",101, 0, 1)

gStyle.SetOptStat(11111111)   # Gives a lot of detail in the stats box for the histograms

# Counter for the number of events in the file
numevt = 0

### --------------------------------------------------------------------------

for jentry in range( entries ):
   # Get the next tree in the chain and verify.
   ientry = mychain.LoadTree( jentry )
   if ientry < 0:
      break

   # Copy next entry into memory and verify.
   nb = mychain.GetEntry( jentry )
   if nb <= 0:
      continue

   # Use the values directly from the tree. 

   ### -----------------------------------------------------------------------
   ### The Loop code goes here.
   ### -----------------------------------------------------------------------

   numevt = numevt + 1

   values = {}

   values['Z_m'] = mychain.Z_m
   values['LHValue'] = mychain.p_LHValue
   values['et_calo'] = mychain.p_et_calo
   values['mva_Track_kBDT_conf1_mc'] = mychain.mva_Track_kBDT_conf1_mc
   values['mva_Calo_kBDT_conf1_mc'] = mychain.mva_Calo_kBDT_conf1_mc
   values['mva_Iso_kBDT_conf1_mc'] = mychain.mva_Iso_kBDT_conf1_mc
   values['mva_kBDT_conf1_mc_final'] = mychain.mva_kBDT_conf1_mc_final
   values['label0'] = mychain.label0
   values['label1'] = mychain.label1
   values['TruthType'] = mychain.p_TruthType
   values['Truth'] = mychain.Truth

   for key in histograms:
      histograms[key].Fill(values[key])

   
### --------------------------------------------------------------------------
### The Wrap-up code goes here
### --------------------------------------------------------------------------


# See helpers.py for the functions used here
# They save a few lines in setting up and filling the canvases and pads
canvas1 = helpers.defineCanvas('c1', 'Canvas_1', 100, 100, 900, 600, 2, 2)
helpers.plotinCanvas(canvas1, 1, histograms['Z_m'],     '')
helpers.plotinCanvas(canvas1, 2, histograms['LHValue'],   '')
helpers.plotinCanvas(canvas1, 3, histograms['et_calo'],    '')

canvas2 = helpers.defineCanvas('c2', 'Canvas_2', 150, 150, 900, 600, 2, 2)
helpers.plotinCanvas(canvas2, 1, histograms['mva_Track_kBDT_conf1_mc'],      '')
helpers.plotinCanvas(canvas2, 2, histograms['mva_Iso_kBDT_conf1_mc'], '')
helpers.plotinCanvas(canvas2, 3, histograms['mva_Calo_kBDT_conf1_mc'],     '')
helpers.plotinCanvas(canvas2, 4, histograms['mva_kBDT_conf1_mc_final'],     '')

canvas3 = helpers.defineCanvas('c3', 'Canvas_3', 200, 200, 900, 600, 2, 2)
helpers.plotinCanvas(canvas3, 1, histograms['label0'], '')
helpers.plotinCanvas(canvas3, 2, histograms['label1'], '')
helpers.plotinCanvas(canvas3, 3, histograms['TruthType'], '')
helpers.plotinCanvas(canvas3, 3, histograms['Truth'], '')

plotFileName = "other_variables"

# Save the histograms to a file

print("Saving histograms to a root file.")
outputfile = TFile(plotFileName+".root", "RECREATE")

for key in histograms:
   histograms[key].Write()

outputfile.Close()

# Print histograms to PDF
canvas1.Print(plotFileName+".pdf(")
canvas2.Print(plotFileName+".pdf")
canvas3.Print(plotFileName+".pdf)")

# Report on the number of events processed
print("The number of events processed was", numevt)

# Press any key to exit
reply = input("Press any key to exit: ")
### --------------------------------------------------------------------------

