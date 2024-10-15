# Vincent Funke

import numpy as np
import matplotlib.pyplot as plt
import math as m
import os

# Variablen zur Berechnung + Auslese Daten:
file_name = '../Daten/Daten_vom_2022_03_04/2022_03_04_#02_Profil.txt'

time = []
hall_U = []
head = []
magfeld = []
weg_value = []

with open(file_name, 'r', encoding='utf-8') as fo:
    for num, line in enumerate(fo, 1):
        if 'U_Hall' in line:
            U_Null = float(line.split(':')[1].split()[0])   # in mV
        if 'Startposition' in line:
            label = line.split(':  ')[1].strip()
        if 'Geradlinig' in line:
            hub = float(line.split()[2])                    # in mm/min
        if 'Rotation' in line:
            rotation = float(line.split()[2][:-4]) # in mm
        if 'abs. Zeit' in line:
           break
        head.append(line)
    lines = fo.readlines()
    for line in lines:                  # lese alle Zeilen ein (alle Zeilen mit Werten, da die ersten übersprungen wurden)
        values = line.split()
        hall_U.append(round(float(values[2])*1000,4))            # in mV
        time.append(float(values[1]))

folder = 'Daten/Profil-Umrechnung'
if not os.path.exists(folder):
    os.makedirs(folder)

fre = 14000                 # in Hz
bewegung = 'Hub'            # Hub oder Rotation
# Hub Einstellungen:
richtung_hub = 'ab'         # auf oder ab für die Bewegung
weg_begin = 115             # in mm
weg_Ende = 35               # in mm
# Rotationseinstellungen:
rotation_Begin = 0          # in °
richtung_rot = 'CCW'        # CW oder CCW

# Korrekturwert:
k_f = 5 * (10**(-10)) * (fre**2) + 2 * (10**(-6)) * fre + 1.4512
print(k_f)

# Magnetische Flussdichte berechnen:
for item in hall_U:
    mag_Gauss = (item - U_Null)/(3.125)                 # Faktor in mV/G
    mag_Tesla = mag_Gauss/10000 * 1000                  # in mT
    mag_Tesla_k = mag_Tesla * k_f                       # Korrekturwert draufgerechnet
    magfeld.append(mag_Tesla_k)

# Weg berechnung (Geradlinig - Hub) oder Rotationsbewegung:
if bewegung == 'Hub':
    hub = hub/60        # in mm/s
    for item in time:
        if richtung_hub == 'ab':
            value = weg_begin - (hub*item)
            if value <= weg_Ende:
                value = weg_Ende
            weg_value.append(value)
        if richtung_hub == 'auf':
            value = weg_begin + (hub*item)
            if value >= weg_Ende:
                value = weg_Ende
            weg_value.append(value)

    figure, ax1 = plt.subplots(figsize=(18,10))
    line, = ax1.plot(weg_value, magfeld, 'r', label=label)
    plt.title('Profil B(l)', fontsize=25)
    plt.ylabel("Magnetische Flussdichte B in mT",fontsize=20)
    plt.xlabel("Weg l in mm",fontsize=20)
    plt.legend(loc='best')
    figure.tight_layout()
    plt.grid()
    plt.show()
    SaveName = file_name[-25:].replace('.txt','') + '_Hubbewegung.png'
    new_file_name = file_name[-25:].replace('.txt','') + '_Hubbewegung.txt'
    figure.savefig(folder + '/' + SaveName)

    with open (folder + '/' + new_file_name, 'w', encoding='utf-8') as foAus:
        for item in head:
            foAus.write(f'{item}')
        foAus.write('Zeit [s]'.ljust(20) + 'Weg [mm]'.ljust(20) + 'Magnetische Flussdichte [mT]'.ljust(40) + '\n')
        n = 0
        for item in time:
            foAus.write(f'{item:<20f}{weg_value[n]:<20f}{magfeld[n]:<40f}\n')
            n += 1

if bewegung == 'Rotation':
    rot = rotation*360/60        # in °/s
    print(rot)
    for item in time:
        if richtung_rot == 'CW':
            value = rotation_Begin - (rot*item)
            weg_value.append(value)
        if richtung_rot == 'CCW':
            value = rotation_Begin + (rot*item)
            weg_value.append(value)

    figure, ax1 = plt.subplots(figsize=(18,10))
    line, = ax1.plot(weg_value, magfeld, 'r', label=label)
    plt.title('Profil B(α)', fontsize=25)
    plt.ylabel("Magnetische Flussdichte B in mT",fontsize=20)
    plt.xlabel("Rotation in °",fontsize=20)
    plt.legend(loc='best')
    figure.tight_layout()
    plt.grid()
    plt.show()
    SaveName = file_name[-25:].replace('.txt','') + '_Rotationsbewegung.png'
    new_file_name = file_name[-25:].replace('.txt','') + '_Rotationsbewegung.txt'
    figure.savefig(folder + '/' + SaveName)

    with open (folder + '/' + new_file_name, 'w', encoding='utf-8') as foAus:
        for item in head:
            foAus.write(f'{item}')
        foAus.write('Zeit [s]'.ljust(20) + 'Rotation [°]'.ljust(20) + 'Magnetische Flussdichte [mT]'.ljust(40) + '\n')
        n = 0
        for item in time:
            foAus.write(f'{item:<20f}{weg_value[n]:<20f}{magfeld[n]:<40f}\n')
            n += 1