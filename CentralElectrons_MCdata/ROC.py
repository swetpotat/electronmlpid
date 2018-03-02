#!/usr/bin/env python

from ROOT import TFile, TCanvas, TGraph, TH1F
from ROOT import gDirectory, std
import sys, getopt
import math
from ROOT import *
from array import *

gStyle.SetOptStat(1)

def main():

	gROOT.SetBatch(True)

	# Open root files
	sig_file = TFile('/home/pche3675/summer2018/electronmlpid/CentralElectrons_MCdata/data/MC_SigElectrons_2000000ev.root')
	bkg_file = TFile('/home/pche3675/summer2018/electronmlpid/CentralElectrons_MCdata/data/MC_BkgElectrons_2000000ev.root')

	# Retrieve the ntuple
	sig_tree = sig_file.Get('data')
	sig_nentries = sig_tree.GetEntries()
	bkg_tree = bkg_file.Get('data')	
	bkg_nentries = bkg_tree.GetEntries() 

	h_sigLH = TH1F("Sig_LHValue", "Signal LHValue", 101, -1.6, 2)
	h_bkgLH = TH1F("Bkg_LHValue", "Background LHValue", 101, -4, 1.5)
	
	# Fill the signal histogram
	for i in range(sig_nentries):
	
		if (i % (sig_nentries/10)) == 0:
			print ":: processing signal entry [%s]... " % i
		
		# Load tree
		if sig_tree.LoadTree(i) < 0:
			print "** could not load tree for signal entry #%s" % i
			break

		nb = sig_tree.GetEntry(i)
		if nb <= 0:
			continue
	
		p_LHValue = sig_tree.p_LHValue
		h_sigLH.Fill(p_LHValue)
		
	c1 = TCanvas()
	h_sigLH.Draw()
	h_sigLH.GetXaxis().SetTitle('Likelihood Value')
	h_sigLH.GetYaxis().SetTitle('Number of Entries')
	c1.SaveAs('sig_LH.pdf')

	# Fill the background histogram
	for i in range(bkg_nentries):
		
		if (i % (bkg_nentries/10)) == 0:
			print ":: processing background entry [%s]... " % i
		
		# Load tree
		if bkg_tree.LoadTree(i) < 0:
			print "** could not load tree for background entry #%s" % i
			break

		nb = bkg_tree.GetEntry(i)
		if nb <= 0:
			continue
	
		p_LHValue = bkg_tree.p_LHValue
		h_bkgLH.Fill(p_LHValue)

	c2 = TCanvas()
	h_bkgLH.Draw()
	h_bkgLH.GetXaxis().SetTitle('Likelihood Value')
	h_bkgLH.GetYaxis().SetTitle('Number of Entries')
	c2.SaveAs('bkg_LH.pdf')

	# Calculate TPR and FPR
	TPR = array('f')
	FPR = array('f')

	scounter = 0
	bcounter = 0
	columns = h_sigLH.GetNbinsX()    #  Both signal and background will have same number
									 #  of columns


	for i in range(columns + 1):
		scounter += h_sigLH.GetBinContent(i)
		TPR.append((sig_nentries-scounter)/sig_nentries)
		bcounter += h_bkgLH.GetBinContent(i)
		FPR.append(1-(bkg_nentries-bcounter)/bkg_nentries)
	
	c3 = TCanvas()	
	gr_ROC = TGraph(len(TPR), TPR, FPR)
	gr_ROC.Draw("ACP")
	c3.SaveAs('roc.pdf')
	

# Call main()
if __name__ == "__main__":
	main()
