import numpy as np                              # Bibliothek für das Arbeiten mit Vektoren usw.
import matplotlib.pyplot as plt                 # Bibliothek für die Ausgabe von Graphen
import os

global KurvenE, color_Nr, look

##################################################################################################################################################
def Kurven_Plot(Path):
##################################################################################################################################################
    global KurvenE, color_Nr, look

    # Listen:
    magfeld = []          # Magnetische Flussdichte
    wegrot = []           # Entweder sind da die Weg Daten drinnen oder die Winkeldaten

    Line_color = ['b', 'r', 'y', 'g', 'm', 'c', 'k']                             # Liste der Farben
    Line_Art = ['-', '--', '-.', ':', 'o', 's', 'D', '^', 'x', '*', '+']         # Liste Linien Art (Notiz: Die ersten 4 Arten machen noch Sinn - das wären 28 Kurven, 7 je Art) [durchgezogene Linie, gestrichelte Linie, Strich-Punkt-Linie, gepunktete Linie, Punkt=Kreis, Punkt=Square, Punkt=Diamant, Punkt=Dreieck, Punkt=x, Punkt=*, Punkt=+]

    # Datei auslesen:
    with open(Path,'r', encoding="utf-8") as fi:
        for num, line in enumerate(fi, 1):
            if 'Zeit [s]' in line:
                break
        lines = fi.readlines()
        for line in lines:
            values = line.split()
            wegrot.append(float(values[1]))
            magfeld.append(float(values[2]))

    # Erzeuge die Kurven:
    if color_Nr + 1 > len(Line_color):                                                                                              # Es wird geschaut ob genügend Farben vorhanden sind
        color_Nr = 0                                                                                                                # wenn nicht wird die Liste von vorn begonnen,
        look += 1                                                                                                                   # aber das Aussehen verändert
    l0, = ax1.plot(wegrot, magfeld, f'{Line_color[color_Nr]}{Line_Art[look]}', label =f'Position Hall-Sensor - {position}')              # f'{Line_color[color_Nr]}{Line_Art[look]}' das setzt die Farbe mit der Art zusammen z.B. 'r-' oder 'b-.' | Diese Art geht nicht mit den Farben wie 'orange', 'purple', ... da dies vom Programm nicht gelesen werden kann
    Kurven.append(l0)
    color_Nr += 1

##################################################################################################################################################
                                                                                                          # Angabe der Pfade, keine Individuelle Eingabe
#data = { 'Ab  - Mitte'            : 'Daten/Profil-Umrechnung/2022_03_04_#01_Profil_Hubbewegung_1.txt',
#         'Auf - Mitte'            : 'Daten/Profil-Umrechnung/2022_03_04_#02_Profil_Hubbewegung_1.txt',
#         'Ab  - Links-von-Mitte'  : 'Daten/Profil-Umrechnung/2022_03_04_#03_Profil_Hubbewegung_1.txt',
#         'Ab  - Vorne-von-Mitte'  : 'Daten/Profil-Umrechnung/2022_03_04_#04_Profil_Hubbewegung_1.txt',
#         'Ab  - Rechts-von-Mitte' : 'Daten/Profil-Umrechnung/2022_03_04_#05_Profil_Hubbewegung_1.txt',
#         'Ab  - Hinten-von-Mitte' : 'Daten/Profil-Umrechnung/2022_03_04_#06_Profil_Hubbewegung_1.txt'
#        }

data = { '11.5 cm über Boden - CCW'  : 'Daten/Profil-Umrechnung/2022_03_09_#01_Profil_Rotationsbewegung.txt',
         '11.5 cm über Boden - CW '  : 'Daten/Profil-Umrechnung/2022_03_09_#02_Profil_Rotationsbewegung.txt',
         ' 7.5 cm über Boden - CCW'  : 'Daten/Profil-Umrechnung/2022_03_09_#03_Profil_Rotationsbewegung.txt',
         ' 3.5 cm über Boden - CCW'  : 'Daten/Profil-Umrechnung/2022_03_09_#04_Profil_Rotationsbewegung.txt'
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
plt.ylabel("Magnetische Flussdichte in mT",fontsize=20)
plt.xlabel("Winkel in °",fontsize=20)
plt.legend(loc='best')
plt.tight_layout()
plt.grid()

plt.show()