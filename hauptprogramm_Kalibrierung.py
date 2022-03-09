from numpy import diff
import serial
import yaml
import datetime
import os
import subprocess
import time

import usbtmc

def Read_Ausgabe():                                                       
    st = ''
    back = ser_py.readline().decode()
    st = back.replace('\n', '')                         
    return st 

def um(value, value_unit, wish_unit):                  # Start der Funktion um (Umrechnung)
    einheit = ['nV', 'uV', 'mV', 'V', 'kV']            # Liste der möglichen Einheiten
    for i, unit in enumerate (einheit):                # suche die eingegebenen Einheiten in Liste
        if value_unit == unit:                         # Vergleich der ausgegebenen Einheit des Gerätes mit der Liste um herauszufinden welche Einheit der Rückgabewert hat
            e1 = i                                     # Wert der Quelleinheit in Liste wird gespeichert
        if wish_unit == unit:                          # Vergleich der Wunsch Einheit mit der Liste um herauszufinden in welche Einheit umgerechnet werden soll
            e2 = i                                     # Wert der Zieleinheit in Liste wird gespeichert
    new_value = value * 10**((e1-e2)*3)                # Wenn Einheit gefunden, so wird Zahl umgerechnet in Zieleinheit, durch (e1-e2)*3 wird der Exponent herrausgefunden
    if value_unit == 'mV':
        return round(new_value,8)
    if value_unit == 'kV':
        return round(new_value,2)
    return new_value

# Parameterliste einlesen
config_file = 'parameter.yml'  
with open(config_file) as fi:   
    config = yaml.safe_load(fi)

# Keysight initialisieren
hVID = config['Keysight']['VID']   # Gibt die Werte in DEC zurück (funktioniert auch mit)
hPID = config['Keysight']['PID']   # wenn es in das Hex-Format umgewandelt wird, erkennt das Instrument das nicht: usbtmc.usbtmc.UsbtmcException: Device not found [init]
                                   
instr =  usbtmc.Instrument(hVID, hPID) # wenn man anstatt hVID und hPID die Hex Zahlen die in parameter.yml stehen einträgt, klappt das Programm, sonst muss der DEC Wert übergeben werden (wie jetzt)
name_KS = instr.ask("*IDN?")
print(name_KS)
print('Keysight Gerät initialisiert!')

# Keithley initialisieren
array_data = config['Keithley']     # Dictionerie wird in der variable gespeichert
com, bd, parity, stopbits, bytesize, buffer_U = array_data.values() # Übergabe nur der Werte 
print(buffer_U)
try:
    serial.Serial(port=com)
except serial.SerialException:
    print ('Port ' + com + ' not present')
    quit()

ser_py = serial.Serial(
    port = com,
    baudrate = bd,
    parity = parity,
    stopbits = stopbits,
    bytesize = bytesize,
    timeout = 2.0)

ser_py.write('*RST\n'.encode())         # Resetet das Gerät auf Default Werte und löscht die User erzeugten Buffer
ser_py.write('*IDN?\n'.encode())        # Identifikation des Gerätes erfragen
name_KL = Read_Ausgabe()
print(name_KL)
print('Keithley Gerät initialisiert!')

# Spannungs Buffer erzeugen
ser_py.write((f':TRACe:MAKE "{buffer_U}", 10000\n').encode())

# Frequenzbereich einlesen:
array_data_F = config['Frequenz']    
start, ende, schritt, reverse = array_data_F.values()

# Einlesen der Spulen-Parameter bzw. auch Expriment-Werte:
array_data_S = config['Experiment_Aufbau']    
spuleD, spuleN, vorR, u_hall_Null, Source_U, Source_Lim_I, Source_Gerät = array_data_S.values() 

if reverse == True:         # Umdrehen der Frequenzabarbeitung (True von Hocher Frequenz zu niedriger - sonst andersrum)
    mstart = start
    mende = ende

    start = mende
    ende = mstart

    schritt = schritt * -1 

# Amplitude und Funktion bestimmen
amp = config['Keysight']['amplitude']   
funktion = config['Keysight']['funktion']
channel = config['Keysight']['channel']
sollwert = config['Keysight']['sollwert']
bereich = config['Keysight']['bereich']
berichtige_um = config['Keysight']['berichtige_um']

instr.write(f':WGEN:FUNC {funktion}')
instr.write(f':WGEN:VOLT {amp}')
ak_amp = float(amp)

# Versionsnummer Lesen:
version = (
    subprocess.check_output(["git", "describe", "--tags", "--dirty", "--always"])
    .strip()
    .decode("utf-8")
)

# File erstellen:
actual_date = datetime.datetime.now().strftime('%Y_%m_%d')           
FileOutPrefix = actual_date
FileOutIndex = str(1).zfill(2)
FileOutName = '' 

folder = 'Daten/Daten_vom_' + FileOutPrefix
if not os.path.exists(folder):                                              
    os.makedirs(folder)                                                     

FileOutName = FileOutPrefix + '_#' + FileOutIndex + '_volt.txt'            
j = 1
while os.path.exists(folder + '/' + FileOutName) :                         
    j = j + 1                                                               
    FileOutIndex = str(j).zfill(2)
    FileOutName = FileOutPrefix + '_#' + FileOutIndex + '_volt.txt'
print ('Output data: ', FileOutName)  

with open(folder + '/' + FileOutName,'w', encoding='utf-8') as fo:
    fo.write('Messungen der Hall-Spannung/ Magnetfeldmessungen\n')
    fo.write('------------------------------------------------\n')
    fo.write(f'Datum: {actual_date}\n')
    fo.write(f'Version: {version}\n\n')
    fo.write('Folgende Geräte werden verwendet:\n')
    fo.write('---------------------------------\n')
    fo.write(f'Gerät 1: {name_KS}\n')
    fo.write(f'Gerät 2: {name_KL}\n\n')
    fo.write('Experiment Informationen:\n')
    fo.write('-------------------------\n')
    fo.write(f'Spulendurchmesser: {spuleD} mm\n')
    fo.write(f'Spulenwindungen:   {spuleN} je Spule\n')
    fo.write(f'Vorwiderstand:     {vorR} Ohm\n\n')
    fo.write(f'Versorgung Hall-Sensor von {Source_Gerät}\n')
    fo.write(f'Versorgungsspannung: {Source_U} V\n')
    fo.write(f'Strom-Limit:         {Source_Lim_I} mA\n\n')
    fo.write('Voreinstellungen und Vormessung:\n')
    fo.write('---------------------------\n')
    fo.write(f'Start Amplitude:         {amp} V\n')
    fo.write(f'Genutzte Funktion:       {funktion}\n')
    fo.write(f'Keysight Channel (VRMS): {channel}\n')
    fo.write(f'U_Hall_0:                {u_hall_Null} mV\n\n')
    fo.write(f'Sollwert = {sollwert*1000} mV ± {bereich*1000} mV --> Vpp Anpassung bei Abweichung = {berichtige_um} V\n')
    fo.write(f'Messungen von {start} Hz bis {ende} Hz in {schritt} Hz Schritten\n\n')
    fo.write('Frequenz [Hz]'.ljust(15) + 'Hall-Spannung [V]'.ljust(30) + 'Spannung (VRMS-AC) über R [V]'.ljust(35) + 'Amplitude Vpp (Gen_Out) [V]'.ljust(30))
    fo.write('\n')

for n in range(start, ende + schritt, schritt):
    instr.write(f":WGEN:FREQ {n}")
    #instr.write(":AUToscale") # brauch ca. 4 s
    time.sleep(1)
    ak_Wert = instr.ask(":MEAS:VRMS? AC, CHAN" + str(channel))
    ak_Wert = float(ak_Wert)
    
    while (ak_Wert > sollwert + bereich or ak_Wert < sollwert - bereich):
        if (ak_Wert > sollwert + bereich):
            ak_amp -= berichtige_um
        if (ak_Wert < sollwert - bereich):
            if ak_amp == 12:
                ak_amp = 12
                instr.write(f':WGEN:VOLT {ak_amp}')
                ak_Wert = instr.ask(":MEAS:VRMS? AC, CHAN" + str(channel))
                ak_Wert = float(ak_Wert)
                break
            else:
                ak_amp += berichtige_um
        instr.write(f':WGEN:VOLT {ak_amp}')
        ak_Wert = instr.ask(":MEAS:VRMS? AC, CHAN" + str(channel))
        ak_Wert = float(ak_Wert)
        
    # Messung:
    ser_py.write((f':MEAS:VOLT:AC? "{buffer_U}", FORM\n').encode()) # wert auf Bildschirm wird ausgegeben!
    if n == start:          # Multimeter spinnt ein wenig beim ersten mal wenn es die Funktion zur Messung ändern soll!
        time.sleep(5)
    hallvolt = Read_Ausgabe()                                    # Kommt als String zurück
    teilung = hallvolt.split()
    hallvolt_in_V = um(float(teilung[0]), teilung[1], 'V')
    resvolt = ak_Wert                                            # kein String
    amplitude = instr.ask(":WGEN:VOLT?")
    
    with open(folder + '/' + FileOutName,'a', encoding='utf-8') as fo:
        fo.write(f"{n:<15}{hallvolt_in_V:<30}{resvolt:<35}{amplitude:<30}\n")

print("\nProgramm abgearbeitet!")