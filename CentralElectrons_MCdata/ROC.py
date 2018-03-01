#!/usr/bin/python

from ROOT import TFile, TCanvas, TH1F
from ROOT import gDirectory, std
import sys, getopt
import math
from ROOT import *
from array import *

gStyle.SetOptStat(1)

def main():

	gROOT.SetBatch(True)

	# Open root files
	rfile = TFile('/home/pche3675/summer2018/electronmlpid/CentralElectrons_MCdata/data/MC_SigElectrons_2000000ev.root')

	# Retrieve the ntuple
	rtree = rfile.Get('data')
	rentries = rtree.GetEntries()

	h_LHValue = TH1F("p_LHValue", "LHValue", 101, -1.6, 2)
	
	# Fill the histogram
	for i in xrange(rentries):
		if (i % (rentries/10)) == 0:
		    print ":: processing entry [%s]... " % i

		# Load tree
		if rtree.LoadTree(i) < 0: 
		    print "** could not load tree for entry #%s" % i
		    break

		nb = rtree.GetEntry(i)
		if nb <= 0:
		    # no data
		    continue 

	    # Define branches of tree that will be used for cuts
		p_LHValue = rtree.p_LHValue
		h_LHValue.Fill(p_LHValue) 

	# Draw the histogram
	c1 = TCanvas()
	h_LHValue.Draw()
	h_LHValue.GetXaxis().SetTitle('Likelihood Value')
	h_LHValue.GetYaxis().SetTitle('Number of Entries')
	c1.SaveAs('LHValue_sig.pdf')

	c2 = TCanvas()
	h_ROC = TH1F("ROC for Likelihood Fit", "ROC for Likelihood Fit", 101, 1, 1)
	columns = h_LHValue.GetNbinsX()

	total = 0
	
	for i in range(columns + 1):
		total += h_LHValue.GetBinContent(i)
		ratio = (rentries-total)/rentries
		h_ROC.Fill(ratio)

	h_ROC.Draw("L")
	h_ROC.GetXaxis().SetTitle('Signal Efficiency')
	h_ROC.GetYaxis().SetTitle('Background Rejection')
	c2.SaveAs('ROC_LHValue.pdf')

# Call main()
if __name__ == "__main__":
	main()
