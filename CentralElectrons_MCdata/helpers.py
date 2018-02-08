#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########################################################
#
# Utility code to help with defining and filling histograms
# and creating and displaying canvases containinf those
# histograms.
#
# Contributors: K. Varvell (August 2017)
#               modifying script of D. Schjelderup (June 2017)
#
###########################################################

from ROOT import TFile, gDirectory
from ROOT import TH1D
from ROOT import TH2D
from ROOT import TCanvas
from ROOT import TPad
from ROOT import TMath
from ROOT import gStyle

import math

def defineHistogram(key,x_title,nbins,start,end):

   histogram = TH1D(key, 'Histogram of '+x_title, nbins, start, end)
   histogram.GetXaxis().SetTitle(x_title)
   histogram.GetYaxis().SetTitle("Number of events")
   return histogram

# Designed to plot all histograms automatically. Not sure if this code of Daniel's works
def plotHistograms(hist_dictionary,cutHist_dictionary,outputPdfString,outputRootString):

   nHistograms = len(hist_dictionary)
   nCutHistograms = len(cutHist_dictionary)
   nCanvases = math.ceil(nHistograms/4) + math.ceil(nCutHistograms/4)
   canvases = []

   # Create canvases
   for i in range(nCanvases):
      canvases.append(TCanvas('c'+str(i+1), 'Canvas_'+str(i+1), 100, 100, 900, 600))
      canvases[i].Divide(2, 2)

   # Draw all histograms
   n = -1
   for key in hist_dictionary:
      n = n + 1
      canvases[math.floor(n/4)].cd(n+1-math.floor((n+1)/4)*4)
      hist_dictionary[key].Draw()
      canvases[math.floor(nHistograms/4)+math.floor(n/4)].cd(n+1-math.floor((n+1)/4))
      cutHist_dictionary[key].Draw()

   # Save histograms to root file
   print("Saving histograms to a root file.")
   outputfile = TFile(outputRootString, "RECREATE")

   for key in hist_dictionary:
      hist_dictionary[key].Write()

   for key in cutHist_dictionary:
      cutHist_dictionary[key].Write()

   outputfile.Close()

   # Print histograms to PDF
   canvases[0].Print(outputPdfString+'[')
   for canvas in canvases:
      canvas.Print(outputPdfString)
   canvases[nCanvases-1].Print(outputPdfString+']')

def defineCanvas(name, title, xpos, ypos, xwid, ywid, nx, ny):

   canvas = TCanvas(name, title, xpos, ypos, xwid, ywid)
   canvas.Divide(nx, ny)
   return canvas

def plotinCanvas(canvas, pad, histogram, options):

   canvas.cd(pad)
   histogram.Draw(options)

