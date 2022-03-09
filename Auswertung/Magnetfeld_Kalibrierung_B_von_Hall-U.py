import numpy as np                              # Bibliothek für das Arbeiten mit Vektoren usw.
import matplotlib.pyplot as plt                 # Bibliothek für die Ausgabe von Graphen
import os

lese_File = '2022_03_04_#01_volt.txt'

hall_U = []
magfeld = []
head = []

with open('Daten/' + lese_File, 'r', encoding='utf-8') as fo:
    for num, line in enumerate(fo, 1):
        if 'U_Hall_0' in line:
            U_Null = float(line.split(':')[1].split()[0])
        if 'Frequenz' in line:
            break
        head.append(line)
    lines = fo.readlines()
    for line in lines:                  # lese alle Zeilen ein (alle Zeilen mit Werten, da die ersten übersprungen wurden)
        values = line.split()
        hall_U.append(round(float(values[1])*1000,4))            # in mV

for item in hall_U:
    mag_Gauss = (item - U_Null)/(3.125)
    mag_Tesla = mag_Gauss/10000 * 1000                  # in mT
    magfeld.append(mag_Tesla)

figure, ax1 = plt.subplots(figsize=(9,9))   
line11, = ax1.plot(hall_U, magfeld, 'b', label='Daten')
plt.title('B(U_Hall)', fontsize=35)
plt.ylabel("Magnetische Flussdichte B in mT",fontsize=20)
plt.xlabel("Hall-Spannung in mV",fontsize=20)
plt.legend(loc='best') 
plt.tight_layout()                                                 
plt.grid()

plt.show()

# Bildnamen erzeugen (wie Filenamen) aus dem Filenamen
NameFile = ''
NameBild = ''
NameFile = lese_File[0:14] + '_Kalibrierung_Rohdata.txt'
NameBild = lese_File[0:14] + '_Kalibrierung_Rohdata.png'

folder = 'Daten/Kalibrierung'
if not os.path.exists(folder):
    os.makedirs(folder)

print ('Output data: ', NameBild)
figure.savefig(folder + '/' + NameBild)

with open(folder + '/' + NameFile, 'w', encoding='utf-8') as foN:
    for item in head:
        foN.write(item)
    foN.write('Hall-Spannung [mV]'.ljust(20) + 'Magnetische Flussdichte [mT]'.ljust(30) + '\n')
    n = 0
    for item in hall_U:
        foN.write(f'{item:<20}{magfeld[n]:<30f}\n')
        n += 1