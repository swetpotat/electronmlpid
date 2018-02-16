import csv

filename_sig = "MC_SigElectrons_2000000ev.csv"
filename_bkg = "MC_BkgElectrons_2000000ev.csv"

out_sig = csv.writer(open(filename_sig, 'w+'), delimiter = ',')
out_bkg = csv.writer(open(filename_bkg, 'w+'), delimiter = ',')

counter = 0

with open('data/MC_SigBkgElectrons_2000000ev.csv') as f:
	csvfile = csv.reader(f, delimiter = ',')
	for row in csvfile:
		if counter != 0:
			if float(row[-2]) == 2.0:
				out_sig.writerow(row)
			else:
				out_bkg.writerow(row)
		else:
			out_sig.writerow(row)
			out_bkg.writerow(row)
		counter += 1

