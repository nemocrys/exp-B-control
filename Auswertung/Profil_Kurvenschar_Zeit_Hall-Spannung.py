import numpy as np                              # Bibliothek für das Arbeiten mit Vektoren usw.
import matplotlib.pyplot as plt                 # Bibliothek für die Ausgabe von Graphen
import os

global KurvenE, color_Nr, look

##################################################################################################################################################
def Kurven_Plot(Path):
##################################################################################################################################################
    global KurvenE, color_Nr, look

    # Listen:
    hall_Spannung = []
    time = []

    Line_color = ['b', 'r', 'y', 'g', 'm', 'c', 'k']                             # Liste der Farben
    Line_Art = ['-', '--', '-.', ':', 'o', 's', 'D', '^', 'x', '*', '+']         # Liste Linien Art (Notiz: Die ersten 4 Arten machen noch Sinn - das wären 28 Kurven, 7 je Art) [durchgezogene Linie, gestrichelte Linie, Strich-Punkt-Linie, gepunktete Linie, Punkt=Kreis, Punkt=Square, Punkt=Diamant, Punkt=Dreieck, Punkt=x, Punkt=*, Punkt=+]

    # Datei auslesen:
    with open(Path,'r', encoding="utf-8") as fi:
        for num, line in enumerate(fi, 1):
            if 'abs. Zeit' in line:
                break
        lines = fi.readlines()
        for line in lines:
            values = line.split()
            time.append(float(values[1]))
            hall_Spannung.append(float(values[2])*1000)

    # Erzeuge die Kurven:
    if color_Nr + 1 > len(Line_color):                                                                                              # Es wird geschaut ob genügend Farben vorhanden sind
        color_Nr = 0                                                                                                                # wenn nicht wird die Liste von vorn begonnen,
        look += 1                                                                                                                   # aber das Aussehen verändert
    l0, = ax1.plot(time, hall_Spannung, f'{Line_color[color_Nr]}{Line_Art[look]}', label =f'Position Hall-Sensor - {position}')              # f'{Line_color[color_Nr]}{Line_Art[look]}' das setzt die Farbe mit der Art zusammen z.B. 'r-' oder 'b-.' | Diese Art geht nicht mit den Farben wie 'orange', 'purple', ... da dies vom Programm nicht gelesen werden kann
    Kurven.append(l0)
    color_Nr += 1

##################################################################################################################################################
                                                                                                          # Angabe der Pfade, keine Individuelle Eingabe
#data = { 'Ab  - Mitte - P1'            : 'Daten/4-3-22/2022_03_04_#01_Profil.txt',
#         'Auf - Mitte - P2'            : 'Daten/4-3-22/2022_03_04_#02_Profil.txt',
#         'Ab  - Links-von-Mitte - P3'  : 'Daten/4-3-22/2022_03_04_#03_Profil.txt',
#         'Ab  - Vorne-von-Mitte - P4'  : 'Daten/4-3-22/2022_03_04_#04_Profil.txt',
#         'Ab  - Rechts-von-Mitte - P5' : 'Daten/4-3-22/2022_03_04_#05_Profil.txt',
#         'Ab  - Hinten-von-Mitte - P6' : 'Daten/4-3-22/2022_03_04_#06_Profil.txt'
#        }

data = { 'Mitte - 11.5 cm über Boden - Abwärts bis 3.5 cm'  : '../Daten/Daten_vom_2022_03_04/2022_03_04_#01_Profil.txt',
         'Mitte - 3.5 cm über Boden - Aufwärts bis 11.5 cm'  : '../Daten/Daten_vom_2022_03_04/2022_03_04_#02_Profil.txt',
        }

Kurven = []

color_Nr = 0
look = 0

fig1, ax1 = plt.subplots(figsize=(9,9))

for position in data:
    path = data[position]
    if not os.path.exists(path):
        print('Gibt es nicht!')
    else:
        print('Pfad vorhanden!')
        Kurven_Plot(path)

plt.title('Profil Übersicht', fontsize=35)
plt.ylabel("Hall-Spannung in mV",fontsize=20)
plt.xlabel("Zeit in s",fontsize=20)
plt.legend(loc='best',fontsize=11)
plt.tight_layout()
plt.grid()

plt.show()