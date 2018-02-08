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
histograms["etcone20"]=helpers.defineHistogram("p_etcone20",'etcone20',101, 0, 3.5)
histograms["etcone30"]=helpers.defineHistogram("p_etcone30","etcone30",101, 0, 4.5)
histograms['etcone40']=helpers.defineHistogram('p_etcone40',"etcone40",101, 0, 5)
histograms['etcone20ptCorrection']=helpers.defineHistogram('p_etcone20ptCorrection',"etcone20ptCorrection",101, 0, 0.12)
histograms['etcone30ptCorrection']=helpers.defineHistogram('p_etcone30ptCorrection',"etcone30ptCorrection",101, 0, 0.12)
histograms['etcone40ptCorrection']=helpers.defineHistogram('p_etcone40ptCorrection',"etcone40ptCorrection",101, 0, 0.15)
histograms['ptcone20']=helpers.defineHistogram('p_ptcone20',"ptcone20",101, 0, 6)
histograms['ptcone30']=helpers.defineHistogram('p_ptcone30',"ptcone30",101, 0, 8)
histograms['ptcone40']=helpers.defineHistogram('p_ptcone40',"ptcone40",101, 0, 10)
histograms['ptPU30']=helpers.defineHistogram('p_ptPU30',"Sum of pt Inside Cone of deltaR < 0.3 for Pileup",101, 0, 0.01)


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

   values['etcone20'] = mychain.p_etcone20
   values['etcone30'] = mychain.p_etcone30
   values['etcone40'] = mychain.p_etcone40
   values['etcone20ptCorrection'] = mychain.p_etcone20ptCorrection
   values['etcone30ptCorrection'] = mychain.p_etcone30ptCorrection
   values['etcone40ptCorrection'] = mychain.p_etcone40ptCorrection
   values['ptcone20'] = mychain.p_ptcone20
   values['ptcone30'] = mychain.p_ptcone30
   values['ptcone40'] = mychain.p_ptcone40
   values['ptPU30'] = mychain.p_ptPU30

   for key in histograms:
      histograms[key].Fill(values[key])

   
### --------------------------------------------------------------------------
### The Wrap-up code goes here
### --------------------------------------------------------------------------


# See helpers.py for the functions used here
# They save a few lines in setting up and filling the canvases and pads
canvas1 = helpers.defineCanvas('c1', 'Canvas_1', 100, 100, 900, 600, 2, 2)
helpers.plotinCanvas(canvas1, 1, histograms['etcone20'],     '')
helpers.plotinCanvas(canvas1, 2, histograms['etcone30'],     '')
helpers.plotinCanvas(canvas1, 3, histograms['etcone40'],     '')

canvas2 = helpers.defineCanvas('c2', 'Canvas_2', 150, 150, 900, 600, 2, 2)
helpers.plotinCanvas(canvas2, 1, histograms['etcone20ptCorrection'],      '')
helpers.plotinCanvas(canvas2, 2, histograms['etcone30ptCorrection'],      '')
helpers.plotinCanvas(canvas2, 3, histograms['etcone40ptCorrection'],      '')

canvas3 = helpers.defineCanvas('c3', 'Canvas_3', 200, 200, 900, 600, 2, 2)
helpers.plotinCanvas(canvas3, 1, histograms['ptPU30'], '')

canvas4 = helpers.defineCanvas('c4', 'Canvas_4', 150, 150, 900, 600, 2, 2)
helpers.plotinCanvas(canvas4, 1, histograms['ptcone20'],      '')
helpers.plotinCanvas(canvas4, 2, histograms['ptcone30'],      '')
helpers.plotinCanvas(canvas4, 3, histograms['ptcone40'],      '')


plotFileName = "isolation_variables"

# Save the histograms to a file

print("Saving histograms to a root file.")
outputfile = TFile(plotFileName+".root", "RECREATE")

for key in histograms:
   histograms[key].Write()

outputfile.Close()

# Print histograms to PDF
canvas1.Print(plotFileName+".pdf(")
canvas2.Print(plotFileName+".pdf")
canvas3.Print(plotFileName+".pdf")
canvas4.Print(plotFileName+".pdf)")

# Report on the number of events processed
print("The number of events processed was", numevt)

# Press any key to exit
reply = input("Press any key to exit: ")
### --------------------------------------------------------------------------

