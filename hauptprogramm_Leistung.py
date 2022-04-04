# Vincent Funke

import usbtmc

import numpy as np
import matplotlib.pyplot as plt
import os
import yaml
import datetime

class Kurve:
    def __init__(self, channel_Number, Label_Kurve):
        self.kanalnummer = channel_Number
        self.Label = Label_Kurve

        self.data = []
        self.time = ''

        self.data_Werte()
        self.File_Name()

    def data_Werte(self):
        print(f'Daten werden von {self.kanalnummer} eingelesen!')
        instr.write(":WAV:FORM ASCii")
        instr.write(":WAVeform:SOURce CHAN" + str(self.kanalnummer))
        self.data = instr.ask(":WAVeform:DATA?").split(",")
        self.data[0] = self.data[0].split(' ')[1]
        self.time = instr.ask(":WAVeform:XINCrement?")
        print('Fertig')

    def File_Name(self):
        actual_date = datetime.datetime.now().strftime('%Y_%m_%d')
        FileOutPrefix = actual_date
        FileOutIndex = str(1).zfill(2)
        self.FileOutName = ''

        self.folder = 'Daten/Oszi-Daten_vom_' + FileOutPrefix
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        self.FileOutName = FileOutPrefix + '_Nr' + FileOutIndex + '_Leistung_' + self.Label + '.txt'
        j = 1
        while os.path.exists(self.folder + '/' + self.FileOutName) :
            j = j + 1
            FileOutIndex = str(j).zfill(2)
            self.FileOutName = FileOutPrefix + '_Nr' + FileOutIndex + '_Leistung_' + self.Label + '.txt'
        print ('Output data: ', self.FileOutName)

wann_date = datetime.datetime.now().strftime('%Y_%m_%d')
wann_actual = datetime.datetime.now().strftime('%H:%M:%S')

# Parameterliste einlesen
config_file = 'parameter_Leistung.yml'
with open(config_file) as fi:
    config = yaml.safe_load(fi)

# Keysight initialisieren
hVID = config['Keysight']['VID']
hPID = config['Keysight']['PID']

instr =  usbtmc.Instrument(hVID, hPID) # wenn man anstatt hVID und hPID die Hex Zahlen die in parameter.yml stehen einträgt, klappt das Programm, sonst muss der DEC Wert übergeben werden (wie jetzt)
name_KS = instr.ask("*IDN?")
print(name_KS)
print('Keysight Gerät initialisiert!')

# Kurven Daten auslesen:
channels = {}
for name, data in config['Channel'].items():
    chan = Kurve(**data)
    channels.update({name: chan})

# Daten Auslesen und Plotten:
# Kurve Auslesen:
figure, ax1 = plt.subplots(figsize=(18,10))
kanalcolor= ['gold', 'g', 'b', 'r']

for name, value in channels.items():
    print(f'{name} wird bearbeitet!')
    x = []
    y = []

    with open(value.folder + '/' + value.FileOutName,'w', encoding='utf-8') as fo:
        fo.write(f'Aufnahme der Osziloskop Kurve - {value.Label} - Kanal {value.kanalnummer}\n\n')
        fo.write(f'Zeitschritt = {value.time}\n\n')
        if 'Messung' in config: # So kann man auch einfach andere Kurven aufnehmen und mehr - Die Angaben sind für die Leistungsmessung gut
            array_data = config['Messung']
            wann, Korrektur_Spannung, Gerät_Spannung, Korrektur_Strom, Gerät_Strom = array_data.values()
            fo.write('Aufbau der Messung und Einstellungen:\n')
            fo.write('-------------------------------------\n')
            fo.write(f'Messgerät Spannung: {Gerät_Spannung}\n')
            fo.write(f'Korrekturfaktor U:  {Korrektur_Spannung}\n')
            fo.write(f'Messgerät Stromes:  {Gerät_Strom}\n')
            fo.write(f'Korrekturfaktor I:  {Korrektur_Strom}\n')
            fo.write(f'Messung gemacht: {wann} - {wann_date} | {wann_actual}\n\n')

        for item in value.data:
            fo.write(f'{item}\n')

        fTime = float(value.time)
        n = 0
        for item in value.data:
            if item != '':       # Soll Leerzeilen in der Text-Datei überlesen
                x.append(n)
                try:
                    y.append(float(item))
                except:
                    print(f'Fehlerwert = {item} bei {n}')
                n += fTime

        colornumber = int(value.kanalnummer) - 1
        line1, = ax1.plot(x, y, kanalcolor[colornumber], label=f'{value.Label} - Kanal: {value.kanalnummer}')

plt.title(f'Oszilloskop Plot', fontsize=35)
plt.ylabel('Spannung in V',fontsize=20)
plt.xlabel("Zeit in s",fontsize=20)
plt.legend(loc='best')
plt.grid()

plt.show() # funktuioniert nicht mit plt.ion()

actual_date = datetime.datetime.now().strftime('%Y_%m_%d')
SaveOutPrefix = actual_date
SaveOutIndex = str(1).zfill(2)
Name = ''

Savefolder = 'Daten/Oszi-Daten_vom_' + SaveOutPrefix
if not os.path.exists(Savefolder):
    os.makedirs(Savefolder)

Name = SaveOutPrefix + '_Nr' + SaveOutIndex + '_Leistung_OsziBild' + '.png'
j = 1
while os.path.exists(Savefolder + '/' + Name) :
    j = j + 1
    SaveOutIndex = str(j).zfill(2)
    Name = SaveOutPrefix + '_Nr' + SaveOutIndex + '_Leistung_OsziBild' + '.png'

print ('Output data: ', Name)
figure.savefig(Savefolder + '/' + Name)