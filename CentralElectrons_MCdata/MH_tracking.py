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
histograms["numberOfInnermostPixelHits"]=helpers.defineHistogram("p_numberOfInnermostPixelHits",'Number of Innermost Pixel Hits',10, 0, 3)
histograms["numberOfPixelHits"]=helpers.defineHistogram("p_numberOfPixelHits","Number of Pixel Hits",10, 0, 9)
histograms['numberOfSCTHits']=helpers.defineHistogram('p_numberOfSCTHits',"Number of SCT Hits",10, 0, 15)
histograms['d0']=helpers.defineHistogram('p_d0',"Transverse Impact Parameter",101, -1, 1)
histograms['d0Sig']=helpers.defineHistogram('p_d0Sig',"Transverse Impact Parameter (Signal)",101, -20, 20)
histograms['dPOverP']=helpers.defineHistogram('p_dPOverP',"dPOverP",101, -0.5, 1.2)
histograms['deltaEta1']=helpers.defineHistogram('p_deltaEta1',"Pseudorapidity",101, -0.2, 0.2)
histograms['deltaPhiRescaled2']=helpers.defineHistogram('p_deltaPhiRescaled2',"Azimuthal Angle Rescaled",101, -0.15, 0.15)
histograms['EptRatio']=helpers.defineHistogram('p_EptRatio',"Electron Momentum Ratio",101, 0, 25)
histograms['TRTPID']=helpers.defineHistogram('p_TRTPID',"Tracker PID",101, -0.8, 0.8)
histograms['numberOfTRTHits']=helpers.defineHistogram('p_numberOfTRTHits',"Number of TRT Detector Hits",10, 0, 50)
histograms['TRTTrackOccupancy']=helpers.defineHistogram('p_TRTTrackOccupancy',"Occupancy in Direction of Electron Candidate",101, 0, 0.8)
histograms['numberOfTRTXenonHits']=helpers.defineHistogram('p_numberOfTRTXenonHits',"Number of TRT Detector Hits in Straws with Xenon",101, 0, 45)


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

   values['numberOfInnermostPixelHits'] = mychain.p_numberOfInnermostPixelHits
   values['numberOfPixelHits'] = mychain.p_numberOfPixelHits
   values['numberOfSCTHits'] = mychain.p_numberOfSCTHits
   values['d0'] = mychain.p_d0
   values['d0Sig'] = mychain.p_d0Sig
   values['dPOverP'] = mychain.p_dPOverP
   values['deltaEta1'] = mychain.p_deltaEta1
   values['deltaPhiRescaled2'] = mychain.p_deltaPhiRescaled2
   values['EptRatio'] = mychain.p_EptRatio
   values['TRTPID'] = mychain.p_TRTPID
   values['numberOfTRTHits'] = mychain.p_numberOfTRTHits
   values['TRTTrackOccupancy'] = mychain.p_TRTTrackOccupancy
   values['numberOfTRTXenonHits'] = mychain.p_numberOfTRTXenonHits

   for key in histograms:
      histograms[key].Fill(values[key])

   
### --------------------------------------------------------------------------
### The Wrap-up code goes here
### --------------------------------------------------------------------------


# See helpers.py for the functions used here
# They save a few lines in setting up and filling the canvases and pads
canvas1 = helpers.defineCanvas('c1', 'Canvas_1', 100, 100, 900, 600, 2, 2)
helpers.plotinCanvas(canvas1, 1, histograms['numberOfInnermostPixelHits'],     '')
helpers.plotinCanvas(canvas1, 2, histograms['numberOfPixelHits'],   '')
helpers.plotinCanvas(canvas1, 3, histograms['numberOfSCTHits'],    '')

canvas2 = helpers.defineCanvas('c2', 'Canvas_2', 150, 150, 900, 600, 2, 2)
helpers.plotinCanvas(canvas2, 1, histograms['d0'],      '')
helpers.plotinCanvas(canvas2, 2, histograms['d0Sig'], '')
helpers.plotinCanvas(canvas2, 3, histograms['dPOverP'],     '')

canvas3 = helpers.defineCanvas('c3', 'Canvas_3', 200, 200, 900, 600, 2, 2)
helpers.plotinCanvas(canvas3, 1, histograms['deltaEta1'], '')
helpers.plotinCanvas(canvas3, 2, histograms['deltaPhiRescaled2'], '')
helpers.plotinCanvas(canvas3, 3, histograms['EptRatio'], '')

canvas4 = helpers.defineCanvas('c4', 'Canvas_4', 250, 250, 900, 600, 2, 2)
helpers.plotinCanvas(canvas4, 1, histograms['TRTPID'], '')
helpers.plotinCanvas(canvas4, 2, histograms['numberOfTRTHits'],          '')
helpers.plotinCanvas(canvas4, 3, histograms['TRTTrackOccupancy'],   'box')
helpers.plotinCanvas(canvas4, 4, histograms['numberOfTRTXenonHits'], '')

plotFileName = "tracking_variables"

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

