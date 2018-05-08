#!/usr/bin/env python

from ROOT import *
import sys, getopt
import math
import array
import numpy

gStyle.SetOptStat(1)

def main():

	# Open root files
	sfile = TFile('/home/pche3675/summer2018/electronmlpid/CentralElectrons_MCdata/data/MC_SigElectrons_2000000ev.root')
	bfile = TFile('/home/pche3675/summer2018/electronmlpid/CentralElectrons_MCdata/data/MC_BkgElectrons_2000000ev.root')

	# Retrieve the ntuple
	stree = sfile.Get('data')
	snentries = stree.GetEntries()
	btree = bfile.Get('data')
	bnentries = btree.GetEntries()

	print("Trees loaded.")

	# Make histograms
	hs_eta = TH1F("Signal Eta", "Eta angle", 101, -2.5, 2.5)
	hb_eta = TH1F("Background Eta", "Eta angle", 101, -2.5, 2.5)
	hs_et = TH1F("Signal E_t", "Transverse Energy", 101, 0, 100000)
	hb_et = TH1F("Background E_t", "Transverse Energy", 101, 0, 100000)
	hs_mu = TH1F("Signal <mu>", "Average Interactions Per Crossing", 41, -0.5, 40.5)
	hb_mu = TH1F("Background <mu>", "Average Interactions Per Crossing", 41, -0.5, 40.5)

	sn_eta = []
	sn_mu = []
	sn_et = []	

	# Fill the signal histogram
	for i in range(snentries):
		stree.LoadTree(i)
		nb = stree.GetEntry(i)
		p_eta = stree.p_eta
		p_mu = stree.averageInteractionsPerCrossing
		p_et_calo = stree.p_et_calo
		hs_eta.Fill(p_eta)
		hs_et.Fill(p_et_calo)
		hs_mu.Fill(p_mu)
		sn_eta.append(hs_eta.GetXaxis().FindBin(p_eta))
		sn_et.append(hs_et.GetXaxis().FindBin(p_et_calo))
		sn_mu.append(hs_mu.GetXaxis().FindBin(p_mu))

	bn_eta = []
	bn_mu = []
	bn_et = []
	
	# Fill the background histogram
	for i in range(bnentries):
		btree.LoadTree(i)
		nb = btree.GetEntry(i)
		p_eta = btree.p_eta
		p_mu = btree.averageInteractionsPerCrossing
		p_et_calo = btree.p_et_calo
		hb_et.Fill(p_et_calo)
		hb_mu.Fill(p_mu)
		hb_eta.Fill(p_eta)
		bn_eta.append(hb_eta.GetXaxis().FindBin(p_eta))
		bn_mu.append(hb_mu.GetXaxis().FindBin(p_mu))
		bn_et.append(hb_et.GetXaxis().FindBin(p_et_calo))		

	# Calculate weights
	eta_weights = hs_eta.Clone()
	eta_weights.Divide(hb_eta)
	et_weights = hs_et.Clone()
	et_weights.Divide(hb_et)
	mu_weights = hs_mu.Clone()
	mu_weights.Divide(hb_mu)

	# Assign weights to each event
	
	bkg_weights = numpy.array([0])
	sig_weights = numpy.array([0])	

	tfile = TFile('weights.root', 'recreate')
	ttree = TTree('weights', 'weights')

	ttree.Branch('sig_weights', sig_weights ,'sig_weights/D' )
	ttree.Branch('bkg_weights', bkg_weights, 'bkg_weights/D')	

	for i in range(len(sn_eta)):
		sig_weights = numpy.append(sig_weights,mu_weights.GetBinContent(int(sn_mu[i]))*et_weights.GetBinContent(int(sn_et[i]))*eta_weights.GetBinContent(int(sn_eta[i])))
		if (i % 100000 == 0 and i != 0):
			print(str(i) + " signal event weights assigned.....")
		ttree.Fill()

	for i in range(len(bn_eta)):
		bkg_weights = numpy.append(bkg_weights,mu_weights.GetBinContent(int(bn_mu[i]))*et_weights.GetBinContent(int(bn_et[i]))*eta_weights.GetBinContent(int(bn_eta[i])))
		if (i % 100000 == 0 and i != 0):
			print(str(i) + " background event weights assigned.....")
		ttree.Fill()


	print("Signal: " + str(len(sn_eta)))
	print("Background: " + str(len(bn_eta)))
	print("Total number of events: " + str(bnentries + snentries))

	tfile.Write()
	tfile.Close()

if __name__ == "__main__":
	main()
