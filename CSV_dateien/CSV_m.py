import csv
import os




################## Rohdatenerfassung ################################
rawHSNR=open('HSNR.csv')
rawENTSOE=open('ENTSOE.csv')

liste_HSNR=csv.reader(rawHSNR)
liste_ENTSOE=csv.reader(rawENTSOE)

HSNR=list(liste_HSNR)    #hier wird eine Liste des gesamten CSV-files HSNR erstellt
ENTSOE=list(liste_ENTSOE)#hier wird eine Liste des gesamten CSV-files ENTSOE erstellt

rawHSNR.close()
rawENTSOE.close()
######################################################################


############################# CSV-Manipulation ##############################
# Hier werden die Rohdaten von OPSD/ENTSOE mit dem HSNR.csv zusammengeführt #
#############################################################################

hsnr=[]                     # Erzeugt eine leere Liste 'hsnr'. Dieser können Elemente aus
                            #   anderen CSV-Files hinzugefügt werden.
for row in HSNR:
    hsnr.append(row[0:])    #Das 'row[0:]' bewirkt, dass alle Spaltenelemente aus dem Original
##print(hsnr)               #   HSNR.csv in die Liste 'hsnr' "hinzuaddiert" werden.
                            #   Man kann auch nur bestimmte Spaltenelemente hinzufügen, indem der
                            #   Bereich [0:] variiert wird.
    
zeitreihe =[]               # Hier wird eine leere Liste 'zeitreihe' erstellt. 
for row in ENTSOE:
    zeitreihe.append(row[4:5])  #Mit dem zeitreihe.append(row[4:5])-Befehl wird aus der
##print(zeitreihe)              #   ENTSOE.csv-Datei die Spalte 'browncoal /lignite' der
                                #   leeren Liste 'zeitreihe' hinzuaddiert. Weiter unten im Code
                                #   werden die nun befüllten Listen 'hsnr' und 'zeitreihe'
                                #   mittels Summation zusammenaddiert.

with open("HSNR1.csv", "a",newline='') as m:
    writer=csv.writer(m)
    for row in range (0,8761):
        writer.writerow(hsnr[row]+zeitreihe[row]) 
os.remove("HSNR.csv")
os.rename("HSNR1.csv","HSNR.csv")
    
