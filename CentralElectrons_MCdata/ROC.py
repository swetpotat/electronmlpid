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

	h_sigLH = TH1F("Sig_LHValue", "Signal Likelihood Value", 101, -1.6, 2)
	h_bkgLH = TH1F("Bkg_LHValue", "Background Likelihood Value", 101, -4, 1.5)
	h_sigBDT = TH1F("Sig_BDTValue", "Signal BDT Value", 101, -4.5, 9)
	h_bkgBDT = TH1F("Bkg_BDTValue", "Background BDT Value", 101, -10, 7)
	
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
		mva_final_sig = sig_tree.mva_kBDT_conf1_mc_final
		h_sigLH.Fill(p_LHValue)
		h_sigBDT.Fill(mva_final_sig)
		
	c1 = TCanvas()
	h_sigLH.Draw()
	h_sigLH.GetXaxis().SetTitle('Likelihood Value')
	h_sigLH.GetYaxis().SetTitle('Number of Entries')
	c1.SaveAs('sig_LH.pdf')
	c2 = TCanvas()
	h_sigBDT.Draw()
	h_sigBDT.GetXaxis().SetTitle('BDT score')
	h_sigBDT.GetYaxis().SetTitle('Number of Entries')
	c2.SaveAs('sig_BDT.pdf')


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
		mva_final_bkg = bkg_tree.mva_kBDT_conf1_mc_final
		h_bkgLH.Fill(p_LHValue)
		h_bkgBDT.Fill(mva_final_bkg)

	c3 = TCanvas()
	h_bkgLH.Draw()
	h_bkgLH.GetXaxis().SetTitle('Likelihood Value')
	h_bkgLH.GetYaxis().SetTitle('Number of Entries')
	c3.SaveAs('bkg_LH.pdf')
	c4 = TCanvas()
	h_bkgBDT.Draw()
	h_bkgBDT.GetXaxis().SetTitle('BDT score')
	h_bkgBDT.GetYaxis().SetTitle('Number of Entries')
	c4.SaveAs('bkg_BDT.pdf')

	# Calculate TPR and FPR for Likelihood Fit
	TPR_LH = array('f')
	FPR_LH = array('f')

	scounter = 0
	bcounter = 0
	columns = h_sigLH.GetNbinsX()    #  Both signal and background will have same number
									 #  of columns


	for i in range(columns + 1):
		scounter += h_sigLH.GetBinContent(i)
		TPR_LH.append((sig_nentries-scounter)/sig_nentries)
		bcounter += h_bkgLH.GetBinContent(i)
		FPR_LH.append(1-(bkg_nentries-bcounter)/bkg_nentries)

	# Calculate TPR and FPR for BDT Algorithm
	TPR_BDT = array('f')
	FPR_BDT = array('f')

	scounter = 0
	bcounter = 0

	for i in range(columns + 1):
		scounter += h_sigBDT.GetBinContent(i)
		TPR_BDT.append((sig_nentries-scounter)/sig_nentries)
		bcounter += h_bkgBDT.GetBinContent(i)
		FPR_BDT.append(1-(bkg_nentries-bcounter)/bkg_nentries)

	ratios = array('f')

	for i in range(columns + 1):
		ratios.append(FPR_LH[i]/FPR_BDT[i])

	print "Likelihood"
	print FPR_LH
	print "Boosted Decision Tree"
	print FPR_BDT
	print "Ratios"
	print ratios
	print "TPR_LH"
	print TPR_LH

	c5 = TCanvas()	
	gr_ROC = TMultiGraph()
	gr_LH = TGraph(len(TPR_LH), TPR_LH, FPR_LH)
	gr_LH.SetLineColor(kBlue)
	gr_LH.SetLineWidth(3)
	gr_BDT = TGraph(len(TPR_BDT), TPR_BDT, FPR_BDT)
	gr_BDT.SetLineColor(kRed)
	gr_BDT.SetLineWidth(3)
	#LHdivBDT = TGraph(len(TPR_LH), TPR_LH, ratios)
	#LHdivBDT.SetLineColor(kBlack)
	#LHdivBDT.SetLineWidth(3)
	gr_ROC.Add(gr_LH)
	gr_ROC.Add(gr_BDT)
	#gr_ROC.Add(LHdivBDT)
	gr_ROC.Draw("ACP")
	gr_ROC.SetTitle("ROC Curve")
	gr_ROC.GetXaxis().SetTitle("Signal Efficiency")
	gr_ROC.GetYaxis().SetTitle("Background Rejection")	
	legend = TLegend(0.2, 0.2, 0.4, 0.4)
	legend.SetHeader("Legend", "C")
	legend.AddEntry(gr_LH, "Likelihood Fit", "l")
	legend.AddEntry(gr_BDT, "Boosted Decision Trees", "l")
	#legend.AddEntry(LHdivBDT, "Ratio LH/BDT", "1")
	legend.Draw()
	c5.SaveAs('roc.pdf')

	c6 = TCanvas()
	gr_ratio = TGraph(len(TPR_LH), sorted(TPR_LH), sorted(ratios))
	gr_ratio.Draw("ACP")
	gr_ratio.SetTitle("Ratio of LH ROC / BDT ROC")
	gr_ratio.GetXaxis().SetTitle("Signal Efficiency")
	gr_ratio.GetYaxis().SetTitle("Ratio")	
	c6.SaveAs('ratio.pdf')

	
# Call main()
if __name__ == "__main__":
	main()
