import csv
import os
#import raw_data        das '#' entfernen, sobald das verknüpfen mit raw_data funktioniert

os.remove("HSNR.csv")

################## Rohdatenerfassung ################################
rawOPSD=open('opsd.csv')
rawHSNR=open('HSNR_ohne_regenerative.csv')

liste_opsd=csv.reader(rawOPSD)
liste_HSNR=csv.reader(rawHSNR)

opsd=list(liste_opsd)   #hier wird eine Liste des gesamten CSV-files opsd erstellt
HSNR=list(liste_HSNR)   #hier wird eine Liste des gesamten CSV-files HSNR erstellt

rawOPSD.close()
rawHSNR.close()
######################################################################


################### CSV-Manipulation #################################
# Hier werden die Rohdaten von OPSD mit dem HSNR.csv zusammengeführt #
######################################################################
zeitreihe =[]
for row in opsd:
    zeitreihe.append(row [3:9])
#print(zeitreihe)



with open("HSNR.csv", "a",newline='') as f:
    writer=csv.writer(f)
    for row in range (0,8761):
        writer.writerow(HSNR[row]+zeitreihe[row])

f.close()

    
