import csv

raw=open('reg.csv')
rawHSNR=open('HSNR.csv')

liste_reg=csv.reader(raw)
liste_HSNR=csv.reader(rawHSNR)

zeitreihe =[]
for row in liste_reg:
    zeitreihe.append(row [4])
#    for i in range (4,7):
#        zeitreihe.append(row [i])
#    zeitreihe.append(row [4])
#    zeitreihe.append(row [5])
#    zeitreihe.append(row [6])
print (zeitreihe)

raw.close()
rawHSNR.close()


with open("Probe.csv", "a") as f:
    writer=csv.writer(f)
    for i in range (0,20):
        writer.writerow(zeitreihe[i])
f.close()
    
