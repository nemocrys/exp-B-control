# Vincent Funke

# Profil - Messung der Hall-Spannung in Test-CZ

import serial
import time
import datetime  
from tkinter import *                           
from tkinter import ttk
import numpy as np                              
import matplotlib.pyplot as plt
import os
import yaml
import subprocess                               

global Erste_Messung, buffer_U
     
# Funktionen:
def Read_Ausgabe():                                                       
    st = ''
    back = ser_py.readline().decode()
    st = back.replace('\n', '')                         
    return st 

# Quelle - Labor Softwaretechnik - Aufgabe 2.3 (angepasst an neue Anforderung)
def um(value, value_unit, wish_unit):                 
    einheit = ['nV', 'uV', 'mV', 'V', 'kV']            # Liste der möglichen Einheiten
    for i, unit in enumerate (einheit):                # suche die eingegebenen Einheiten in Liste
        if value_unit == unit:                         # Vergleich der ausgegebenen Einheit des Gerätes mit der Liste um herauszufinden welche Einheit der Rückgabewert hat
            e1 = i                                     # Wert der Quelleinheit in Liste wird gespeichert
        if wish_unit == unit:                          # Vergleich der Wunsch Einheit mit der Liste um herauszufinden in welche Einheit umgerechnet werden soll
            e2 = i                                     # Wert der Zieleinheit in Liste wird gespeichert
    new_value = value * 10**((e1-e2)*3)      # Wenn Einheit gefunden, so wird Zahl umgerechnet in Zieleinheit, durch (e1-e2)*3 wird der Exponent herrausgefunden
    if value_unit == 'mV':
        return round(new_value,8)
    if value_unit == 'kV':
        return round(new_value,2)
    return new_value

def Init_File():                                                          # Erstelle die Köpfe der File-Datei
    global FileOutName, FileOutNameE, FileOutNameEEnd, AutoStop_Pt, AutoStop_Hp, AutoStop_Py, Folder

    # Variablen und Listen Initialisierung:
    actual_date = datetime.datetime.now().strftime('%Y_%m_%d')            # Variablen für den Datei Namen 
    FileOutPrefix = actual_date
    FileOutIndex = str(1).zfill(2)
    FileOutName = ''    

    # Versionsnummer von GitHub Lesen:
    version = (
        subprocess.check_output(["git", "describe", "--tags", "--dirty", "--always"])
        .strip()
        .decode("utf-8")
    )

    # Eindeutige Ordnernamen + Ordner erstellen (Ordner nach Tagen erstellen):
    Folder = 'Daten/Daten_vom_' + FileOutPrefix + '/Profil'                   
    if not os.path.exists(Folder):                                              
        os.makedirs(Folder)                                                     
    
    # Automatische Erzeugung von eindeutigen Filenamen, ohne das eine alte Datei überschrieben wird:
    FileOutName = FileOutPrefix + '_#' + FileOutIndex + '_Profil.txt'             
    j = 1
    while os.path.exists(Folder + '/' + FileOutName) :                          
        j = j + 1                                                               
        FileOutIndex = str(j).zfill(2)
        FileOutName = FileOutPrefix + '_#' + FileOutIndex + '_Profil.txt'
    print ('Output data: ', FileOutName)  

    # Experiment Aufbau Daten:
    array_data_ex = config['Experiment']     
    ort_Mess, pos_Start, speed_gerade, speed_rot, Source_U, Source_Lim_I, Source_Gerät, Hall_U_Null, Eurotherm_OP = array_data_ex.values() 

    # Öffnen und Erstellen der Datei *temp.txt:
    with open(Folder + '/' + FileOutName,"w", encoding="utf-8") as fo:                 
        fo.write("Profilerstellung eines Magnetfeldes\n") 
        fo.write(f"Datum: {actual_date}\n\n")
        fo.write(f"Version: {version}\n\n")
        fo.write("Experiment Aufbau:\n")
        fo.write('------------------\n')
        fo.write(f'Versorgung Hall-Sensor von {Source_Gerät}\n')
        fo.write(f'Versorgungsspannung:         {Source_U} V\n')
        fo.write(f'Strom-Limit:                 {Source_Lim_I} mA\n')
        fo.write(f'Magnetfeld aus - U_Hall:     {Hall_U_Null} mV\n\n')
        fo.write(f'Eurotherm-Einstellung OP:    {Eurotherm_OP} %\n\n')
        fo.write(f'Gerät für die Messung:       {name_KL}\n')
        fo.write(f"Ort der Messung:             {ort_Mess}\n")
        fo.write(f"Startposition:               {pos_Start}\n")
        fo.write(f"Geschwindigkeit Geradlinig:  {speed_gerade}\n")
        fo.write(f"Geschwindigkeit Rotation:    {speed_rot}\n\n")
        fo.write("abs. Zeit".ljust(15) + "rel. Zeit [s]".ljust(20) + 'Hall-Spannung [V]'.ljust(30))
        fo.write('\n')

def fenster_GUI():
    # Definitionen der Aktionen der Knöpfe:
    def button_action_1():                  # Start Knopf
        anweisungs_label_1.config(Start())  

    def button_action_3():                  # Beenden Knopf
        info_label.config(Stop())
        quit()
    
    def task():
        if nStart == True:                         
            get_Measurment()
            fenster.after(1000, task) 
        else:
            fenster.after(10, task)
    
    # X -Button wird verriegelt
    def disable_event():
        pass
    
    # Ein Fenster erstellen:
    fenster = Tk()
    # Den Fenstertitle erstellen:
    fenster.title("Profil")

    # Buttons:
    Start_button_1 = Button(fenster, text="Start", command=button_action_1)                                
    exit_button = ttk.Button(fenster, text="Beenden", command=button_action_3) 

    # Label:
    anweisungs_label_1 = Label(fenster, text="Start \nMessung!")
    info_label = Label(fenster, text="Schließen und Stoppen")

    # Fenstergröße definieren:
    fenster.geometry("200x200")
    
    #### Start und Beenden
    anweisungs_label_1.place(x = 30, y = 30, width=120, height=35)    # Start
    Start_button_1.place(x = 60, y = 70, width=70, height=30)
    info_label.place(x = 10, y = 110, width=200, height=30)           # Beenden
    exit_button.place(x = 60, y = 140, width=70, height=40)
    
    fenster.protocol("WM_DELETE_WINDOW", disable_event)               
    fenster.after(10, task) 
    fenster.mainloop()  

def get_Measurment():
    global Erste_Messung
    
    time_actual = datetime.datetime.now()
    dt = (time_actual - time_start).total_seconds()
    
    ser_py.write((f':MEAS:VOLT:AC? "{buffer_U}", FORM\n').encode()) # wert auf Bildschirm wird ausgegeben!
    if Erste_Messung == True:          # Multimeter spinnt ein wenig beim ersten mal wenn es die Funktion zur Messung ändern soll!
        time.sleep(5)
        Erste_Messung = False
    hallvolt = Read_Ausgabe()                                    # Kommt als String zurück
    teilung = hallvolt.split()
    hallvolt_in_V = um(float(teilung[0]), teilung[1], 'V')

    listTiRe.append(dt)
    listhallmag.append(hallvolt_in_V * 1000)
    
    with open(Folder + '/' + FileOutName,"a", encoding="utf-8") as fo:
        time_abs = datetime.datetime.now().strftime('%H:%M:%S')                                                                                      
        fo.write(f"{time_abs:<15}{dt:<20.1f}{hallvolt_in_V:<30f}\n")

    # Autoscaling:
    AutoScroll(ax1, 2, 2)            
                        
    # Grafik:
    Update_Graph(line1, listhallmag)                                
        
    figure.canvas.draw()            
    figure.canvas.flush_events()

def Update_Graph(Kurve, Update_Y):                                                                                   
    updated = Update_Y
    Kurve.set_xdata(listTiRe)               
    Kurve.set_ydata(updated)

def AutoScroll(Graph, minusY, plusY):                                      
    Graph.axis('auto')                                  
    Graph.relim()                                       
    ymin, ymax = Graph.get_ylim()                       
    Graph.set_ylim(ymin - minusY, ymax + plusY)         
    Graph.set_xlim(0,listTiRe[-1] + 10)                            

def Start():
    global figure, ax1, line1, nStart
    global listhallmag, time_start, listTiRe
    
    if nStart == False:
        # File erzeugen:
        Init_File()

        time_start = datetime.datetime.now()
        listhallmag = []
        listTiRe = []
        
        nStart = True

        # Grafik Erzeugung:
        plt.ion()
        figure, ax1 = plt.subplots(figsize=(9,9))                                                              
            
        # Hall-Spannung:                                                            
        line1, = ax1.plot(listTiRe, listhallmag, 'r', label='Hall-Spannung') 
        plt.title('Profil Bestimmung', fontsize=35)                                                           
        plt.ylabel("Hall-Spannung in mV",fontsize=20)
        plt.xlabel("Zeit in s",fontsize=20)
        plt.legend(loc='best') 
        plt.grid()
        
        figure.tight_layout()
        
def Stop():
    if nStart == True:
        # Variablen und Listen Initialisierung:
        actual_date = datetime.datetime.now().strftime('%Y_%m_%d')            # Variablen für den Datei Namen 
        FileOutPrefix = actual_date
        FileOutIndex = str(1).zfill(2)
        FileOutName = ''
        
        BName = FileOutPrefix + '_#' + FileOutIndex + '_Profil_Bild.png'             
        j = 1
        while os.path.exists(Folder + '/' + BName) :                          
            j = j + 1                                                               
            FileOutIndex = str(j).zfill(2)
            BName = FileOutPrefix + '_#' + FileOutIndex + '_Profil_Bild.png'
        figure.savefig(Folder + '/' + BName)                     
        print ('Output data: ', BName)  
        quit()

# Hauptteil:
nStart = False

# Parameterliste einlesen
config_file = 'parameter_Profil.yml'  
with open(config_file) as fi:   
    config = yaml.safe_load(fi)

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

Erste_Messung = True

print(f"Multimeter {name_KL} initialisiert!\n")

# Spannungs Buffer erzeugen
ser_py.write((f':TRACe:MAKE "{buffer_U}", 10000\n').encode())

fenster_GUI()
