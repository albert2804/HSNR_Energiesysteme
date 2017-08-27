import csv
import os

a='opsd.csv'
b='HSNR_ohne_regenerative.csv'
def opsd(a):
    rawOPSD=open(a)
    liste_opsd=csv.reader(rawOPSD)
    opsd=list(liste_opsd)   #hier wird eine Liste des gesamten CSV-files opsd erstellt
    
    return(opsd)

def HSNR(b):
    rawHSNR=open(b)
    liste_HSNR=csv.reader(rawHSNR)
    HSNR=list(liste_HSNR)   #hier wird eine Liste des gesamten CSV-files HSNR erstellen

    return (HSNR)

