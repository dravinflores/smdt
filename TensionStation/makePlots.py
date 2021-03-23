import os
from ROOT import TH1D, TCanvas

DIR_PATH = os.getcwd()
filenames = os.listdir('output')#['data_18.12.2019_09_36_41.out']#os.listdir('output')

found = []
tensions = TH1D('','',50, 200, 400)
for filename in filenames:
	month = filename.split('.')[1]
	if int(month) >= 8 and int(month) != 12:
		with open(os.path.join(DIR_PATH, 'output', filename)) as file:
			next(file)
			for line in file:
				data = line.split(',')
				if len(data) < 7: continue
				tension = float(data[6])
				barcode = data[2]
				if 200 < tension < 400 and barcode not in found:
					found.append(barcode)
					tensions.Fill(tension)

tensions.GetXaxis().SetTitle('Tension [g#times grams]')
tensions.SetTitle('BMG Tube Tensions Since August 2019')
tensions.GetYaxis().SetTitle('Count')
c = TCanvas('c','c', 700, 800)
tensions.Draw()
c.SaveAs('shortTubeTensions.pdf')