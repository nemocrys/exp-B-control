# Vincent Funke

import numpy as np                              # Bibliothek für das Arbeiten mit Vektoren usw.
import matplotlib.pyplot as plt                 # Bibliothek für die Ausgabe von Graphen
import os

lese_File = '2022_03_04_#01_volt.txt'
ordner_2 = 'Daten_vom_' + lese_File[0:10] + '/'

fre = []
hall_U = []
vorR_U = []
amp_Gen = []
strom = []
magfeld = []

with open('../Daten/' + ordner_2 + lese_File, 'r', encoding='utf-8') as fo:
    for num, line in enumerate(fo, 1):
        if 'Frequenz' in line:
            break
    lines = fo.readlines()
    for line in lines:                  # lese alle Zeilen ein (alle Zeilen mit Werten, da die ersten übersprungen wurden)
        values = line.split()
        fre.append(float(values[0]))
        hall_U.append(float(values[1])*1000)
        vorR_U.append(float(values[2])*1000)
        amp_Gen.append(float(values[3]))

hall_UNull = float(input('Hall-Spannung ohne Magnetfeld in mV: '))
vorR = float(input('Vorwiderstand in Ohm: '))

for item in vorR_U:
    strom.append((item/vorR))     # I = U/R in mA

for item in hall_U:
    mag_Gauss = (item - hall_UNull)/(3.125)
    mag_Tesla = mag_Gauss/10000 * 1000                  # in mT
    magfeld.append(mag_Tesla)

# Grafik Erzeugung:
figure = plt.figure(figsize=(12,9))
figure.suptitle("Kalibrierungsdaten und Auswertung",fontsize=25)

# Generator - Oszi:
ax1 = plt.subplot(231)
line1, = ax1.plot(fre, amp_Gen, 'b', label='Vpp Generator')
plt.ylabel("Spannung in V",fontsize=12)
plt.legend(loc='best')
plt.grid()

# Vorwiderstands Spannung:
ax2 = plt.subplot(233)
line2, = ax2.plot(fre, vorR_U, 'b', label='Spannung an R_vor (AC RMS)')
plt.ylabel("Spannung in mV",fontsize=12)
plt.xlabel("Frequenz in Hz",fontsize=12)
plt.legend(loc='best')
plt.grid()

# Strom:
ax3 = plt.subplot(232)
line3, = ax3.plot(fre, strom, 'b', label='Strom - RMS')
plt.ylabel("Strom in mA",fontsize=12)
plt.legend(loc='best')
plt.grid()

# Magnetische Flussdichte:
ax4 = plt.subplot(234)
line4, = ax4.plot(fre, magfeld, 'b', label='Magnetische Flussdichte - RMS')
plt.ylabel("Magnetische Flussdichte in mT",fontsize=12)
plt.xlabel("Frequenz in Hz",fontsize=12)
plt.legend(loc='best')
plt.grid()

# Hall-Spannung:
ax5 = plt.subplot(235)
line5, = ax5.plot(fre, hall_U, 'b', label='Hall-Spannung (AC RMS)')
plt.ylabel("Spannung in mV",fontsize=12)
plt.xlabel("Frequenz in Hz",fontsize=12)
plt.legend(loc='best')
plt.grid()

figure.tight_layout()
plt.show()

# Bildnamen erzeugen (wie Filenamen) aus dem Filenamen
SaveOutIndex = str(1).zfill(2)
Name = ''
Name = lese_File.split('.')[0] + '_Bild_#' + SaveOutIndex + '.png'

folder = 'Daten/Daten_vom_' + lese_File.split('.')[0][0:14]
if not os.path.exists(folder):
    os.makedirs(folder)

j = 1
while os.path.exists(folder + '/' + Name) :
    j = j + 1
    SaveOutIndex = str(j).zfill(2)
    Name = lese_File.split('.')[0] + '_Bild_#' + SaveOutIndex + '.png'
print ('Output data: ', Name)
figure.savefig(folder + '/' + Name)
