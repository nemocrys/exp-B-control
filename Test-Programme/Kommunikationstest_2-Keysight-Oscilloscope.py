# konsole lsusb
# Bus 001 Device 058: ID 2a8d:0396

# Visa Adresse: USB0::10893::918::CN61367122::INSTR

'''
Von Windows:
Das Gerät USB\VID_2A8D&PID_0396\CN61367122 wurde konfiguriert.

Treibername: null
Klassen-GUID: {00000000-0000-0000-0000-000000000000}
Treiberdatum: 
Treiberversion: 
Treiberanbieter: 
Treiberabschnitt: 
Treiberrang: 0x0
Passende Geräte-ID: 
Treiber mit niedrigerem Rang: 
Gerät wurde aktualisiert: false
Übergeordnetes Gerät: USB\VID_8564&PID_4100\5&17d83e5a&0&2
'''

# Bei "usb.core.USBError: [Errno 13] Access denied (insufficient permissions)" einfach mal den USB-Stecker am Gerät neu einstecken.
# Antwort auf "*IDN?" = KEYSIGHT TECHNOLOGIES,DSOX1204G,CN61367122,02.11.2020062221

import usbtmc

import numpy as np                              # Bibliothek für das Arbeiten mit Vektoren usw.
import matplotlib.pyplot as plt                 # Bibliothek für die Ausgabe von Graphen
import os


instr =  usbtmc.Instrument(0x2a8d, 0x0396)
print(instr.ask("*IDN?"))

instr.write(":WGEN:FUNCtion SIN")
#instr.write(":WGEN:VOLTage 12")

'''
print(instr.ask(":MEAS:VRMS? CHAN2"))
print(instr.ask(":MEAS:VPP? CHAN2"))

instr.write(":WGEN:FREQ 100")
print(instr.ask(":WGEN:FREQ?"))

instr.write(":WGEN:FUNCtion SIN")
print(instr.ask(":WGEN:FUNCtion?"))

instr.write(":WGEN:VOLTage 10")
print(instr.ask(":WGEN:VOLTage?"))

# Weiteres:
# instr.write(":RUN")
# print(instr.ask(":FFT?"))       # FFT (Fast Fourier Transform)
# #instr.write(":FFT:CENT 60")
# instr.write(":FUNC:FFT:CENT 20")
# print(instr.ask(":FFT:CENT?"))
'''
'''
list = [18000, 20000]

for item in list:
    instr.write(f":WGEN:FREQ {item}")
    print(instr.ask(":MEAS:VRMS? AC, CHAN" + "1"))
    print(instr.ask(":MEAS:VPP? CHAN1"))
    instr.write(":AUToscale")
'''
amplitude = instr.ask(":WGEN:VOLT?")
print(amplitude)
print(instr.ask(":MEAS:VRMS? AC, CHAN" + "1"))

print(instr.ask(":HARDcopy:AREA?")) # Anwort = SCR --> Screen

# Kurve Auslesen:
data = []
x = []
y = []

instr.write(":WAV:FORM ASCii")
data = instr.ask(":WAVeform:DATA?").split(",")
data[0] = data[0].split(' ')[1]
time = instr.ask(":WAVeform:XINCrement?")
with open('Daten_3.txt','w', encoding='utf-8') as fo:
    for item in data:
        fo.write(f'{item}\n')
    fo.write(f'Zeitschritt = {time}')

fTime = float(time)
n = 0
for item in data:
    x.append(n)
    y.append(float(item))
    n += fTime

plt.ion()
figure, ax1 = plt.subplots(figsize=(18,10))                                                              
                                                                       
line1, = ax1.plot(x, y, 'r', label='Oszi-Plot') 
plt.title('Oszilloskop Plot', fontsize=35)                                                           
plt.ylabel("Spannungen V",fontsize=20)
plt.xlabel("Zeit in s",fontsize=20)
plt.legend(loc='best') 
plt.grid()

SaveOutIndex = str(1).zfill(2)
Name = 'Bild_#' + SaveOutIndex + '.png'
folder = 'Daten/Bilder/'
if not os.path.exists(folder):                                              
    os.makedirs(folder)  

j = 1
while os.path.exists(folder + '/' + Name) :
    j = j + 1
    SaveOutIndex = str(j).zfill(2)
    Name = '_Bild_#' + SaveOutIndex + '.png'
print ('Output data: ', Name)             
figure.savefig(folder + '/' + Name)  

# Quellen:
# Quelle Befehle: https://www.keysight.com/de/de/assets/9018-07747/programming-guides/9018-07747.pdf?success=true#page=328&zoom=100,85,128
 