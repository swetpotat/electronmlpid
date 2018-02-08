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
histograms["Rhad1"]=helpers.defineHistogram("p_Rhad1",'p_Rhad1',101, 0, 1)
histograms["Rhad"]=helpers.defineHistogram("p_Rhad","Rhad",101, 0, 2.6)
histograms['f3']=helpers.defineHistogram('p_f3',"f3",101, 0, 0.5)
histograms['weta2']=helpers.defineHistogram('p_weta2',"weta2",101, -0.01, 0.04)
histograms['Rphi']=helpers.defineHistogram('p_Rphi',"Rphi",101, 0.2, 1.1)
histograms['Reta']=helpers.defineHistogram('p_Reta',"Reta",101, 0.2, 1.1)
histograms['Eratio']=helpers.defineHistogram('p_Eratio',"Eratio",101, 0, 1)
histograms['f1']=helpers.defineHistogram('p_f1',"f1",101, 0, 0.6)
histograms['eta']=helpers.defineHistogram('p_eta',"eta",101, -2.5, 2.5)
histograms['averageInteractionsPerCrossing']=helpers.defineHistogram('averageInteractionsPerCrossing',"Average Interaction Per Crossing",101, 0, 40)


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

   values['Rhad1'] = mychain.p_Rhad1
   values['Rhad'] = mychain.p_Rhad
   values['f3'] = mychain.p_f3
   values['weta2'] = mychain.p_weta2
   values['Rphi'] = mychain.p_Rphi
   values['Reta'] = mychain.p_Reta
   values['Eratio'] = mychain.p_Eratio
   values['f1'] = mychain.p_f1
   values['eta'] = mychain.p_eta
   values['averageInteractionsPerCrossing'] = mychain.averageInteractionsPerCrossing

   for key in histograms:
      histograms[key].Fill(values[key])

   
### --------------------------------------------------------------------------
### The Wrap-up code goes here
### --------------------------------------------------------------------------


# See helpers.py for the functions used here
# They save a few lines in setting up and filling the canvases and pads
canvas1 = helpers.defineCanvas('c1', 'Canvas_1', 100, 100, 900, 600, 2, 2)
helpers.plotinCanvas(canvas1, 1, histograms['Rhad1'],     '')
helpers.plotinCanvas(canvas1, 2, histograms['Rhad'],   '')
helpers.plotinCanvas(canvas1, 3, histograms['f1'],    '')
helpers.plotinCanvas(canvas1, 4, histograms['f3'],    '')

canvas2 = helpers.defineCanvas('c2', 'Canvas_2', 150, 150, 900, 600, 2, 2)
helpers.plotinCanvas(canvas2, 1, histograms['weta2'],      '')
helpers.plotinCanvas(canvas2, 2, histograms['eta'], '')
helpers.plotinCanvas(canvas2, 3, histograms['Rphi'],     '')
helpers.plotinCanvas(canvas2, 4, histograms['Reta'],     '')

canvas3 = helpers.defineCanvas('c3', 'Canvas_3', 200, 200, 900, 600, 2, 2)
helpers.plotinCanvas(canvas3, 1, histograms['Eratio'], '')
helpers.plotinCanvas(canvas3, 2, histograms['averageInteractionsPerCrossing'], '')


plotFileName = "calorimeter_variables"

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

