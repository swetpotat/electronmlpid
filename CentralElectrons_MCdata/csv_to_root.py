from ROOT import *

# Creating new root file
hfile = TFile('MC_SigElectrons_500000ev.root','RECREATE')

print("Filling up ntuples...")

tree = TTree('data','data')
tree.ReadFile('data/MC_SigElectrons_500000ev.csv','',',')

print("Saving ntuple to file and closing file.") 

tree.Write()
hfile.Close()
