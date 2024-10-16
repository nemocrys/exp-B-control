## 1. Keithley - DAQ6510            

### 1.1. Inbetriebnahme
Das Gerät ist mit der Python Bibliothek serial über die RS232 Schnittstelle des Gerätes verwendbar. das Programm "Kommunikationstest_1-Keithley-DAQ.py" dient als Testprogramm und zeigt ein Paar Beispiel Befehle. Das Multimeter soll zur Messung der Hall-Spannung verwendet werden.

1. Kommunikationseinstellungen herausfinden
    - über den Bildschirm des Gerätes herausfindbar
    1. Menü Knopf betätigen
    2. in der Spalte "System" auf "Communication" drücken
    3. RS232 auswählen 
    4. Baudrate ist hier einstellbar, die anderen Werte kann man ablesen    
    <img src="../Bilder/System_RS232.jpg" alt="System Kommunikation" title="Menü" width=500/>

    - in dem Dokument "DAQ6510-901-01B_Sept_2019_Ref.pdf" kann man auf folgenden Seiten dies nachlesen:
        - S. 91 - Menü Übersicht (Schritt 2)
        - S. 125 - 126 - Erklärung von dem was auf dem oben gezeigten Bild dargestellt ist
        - ab S. 416 (Kapitel 11) - SCPI Befehle

### 1.2. Befehle
Die Geräte von Keysight und Keithley benutzen SCPI Befehle. SCPI bedeutet "Standard Commands for Programmable Instruments". 

Alle Formalitäten für die Programmierung stehen in dem Dokument "DAQ6510-901-01B_Sept_2019_Ref.pdf" auf den Seiten 416 bis 421. Hier nur eine kurze Aufzählung der Besonderheiten:

- Befehle beginnen mit einen : (Doppelpunkt) (siehe S. 416)(Ausnahme S. 417)
- Abfragen werden mit einem Fragezeichen gekennzeichnet (siehe S. 417)
- die Großbuchstaben in den Befehlen sind die Mindestzeichen die der Befehl haben muss, die klein Buchstaben können weggelassen werden, aber wenn mit geschrieben dann vollständig (siehe S. 418)
- Bei "common commands" (S. 417) reicht es ein * vor dem Befehl zu setzten
- Parameter kommen nach dem Befehl, Befehl und Parameter werden durch ein Leerzeichen getrennt (siehe S. 417)
- weiteres kann man auf den Seiten nachlesen

(für die Absätze (bis hier) wurde die Quelle "DAQ6510-901-01B_Sept_2019_Ref.pdf" S. 416 - 421 genutzt)

*Von uns verwendete Befehle*:   
Seitenangaben beziehen sich auf das Dokument "DAQ6510-901-01B_Sept_2019_Ref.pdf"!   

**Werte Messen**:   
1. :MEASure?
    - nur Lesen möglich
    - S. 431 - 433
    - Nutzende Funktion: **VOLTage** oder **CURRent**
    - Beispiel: **:MEAS:VOLT? "voltMeasBuffer", FORM, READ**
        - das in den Anführungsstrichen ist ein Buffer mit dem man den gelesenen Wert umformatieren kann
    - Beispiel: **:MEAS:VOLT?**
    <img src="../Bilder/Beispiel_Buffer.png" alt="Beispiel" title='Unterschied :MEAS:VOLT? und :MEAS:VOLT? "voltMeasBuffer", FORM, READ' width=700/>          
    In dem Bild kann man den Unterschied zu den beiden Beispielen sehen. Durch den Buffer kann man mit **Form** den Gerätebildschirm Wert anzeigen lassen und mit **Read** wird der Wert einfach ausgelesen und in Exponentialschreibweise dargestellt. Die Exponentialschreibweise wird ohne Buffer Angabe auch gewählt. (Die Unterschiedlichen Werte kommen daher, da das Gerät extrem schwankte in dem Test.)
    - ein gutes Beispiel für die Nutzung des Befehls (auch für Testprogramm verwendet) ist auf Seite 433 zu finden

    - in den `hauptprogram.py` Datein wird der Befehl so benutzt:    
    **:MEAS:VOLT:AC? "{buffer_U}", FORM**
        - bei Default wird der DC Wert ausgelesen, deswegen muss AC angegeben werden 
        - der Buffer kommt aus der Parameter Liste
        - mit Form wird der Wert wie auf dem Bildschirm ausgegeben
        - in unseren Fall benötigen wir AC für die Hall-Spannungsmessung
        - in den Programmen muss ein Delay eingebaut werden, da das Gerät den AC Kanal einstellen muss

**Buffer estellen**:    
1. :TRACe:MAKE 
    - mit dem Befehl kann man einen Buffer erstellen der dann vom Nutzer ausgelesen werden kann
    - S. 616 - 617
    - Beispiel: **:TRACe:MAKE "voltMeasBuffer", 10000**

**Weitere Befehle:**
1. *RST
    - Reset des Gerätes, Buffer vom Benutzer erstellt werden gelöscht
    - verhindert eine Fehlermeldung wegen des Buffers auf dem Gerät
    - S. 1230

2. *IDN?
    - Erfragung des Gerätenamens
    - S. 1228

**Programmierung mit Python:**
Beim senden eines Befehls wird am Ende des Befehls ein \n angehangen, was beim dekodieren wieder ausgefiltert wird. 

### 1.3. Quellen
-  DAQ6510-901-01B_Sept_2019_Ref.pdf
    - zu finden auf: https://download.tek.com/manual/DAQ6510-901-01B_Sept_2019_Ref.pdf 

---
## 2. Keysight - DSOX1204G   

So sieht das genutzte Gerät aus:      
<img src="../Bilder/Oszi_Keysight.jpg" alt="Gerät" title="Keysight - DSOX1204G" width=500/>


### 2.1. Inbetriebnahme
In dem Kapitel wird erklärt wie man das Gerät zu Kommunikation mit dem Computer antriebt. Das Testprogramm "Kommunikationstest_2-Keysight-Oscilloscope.py" zeigt Grundlegende SCPI Befehle (auch die auskommentierten), die Nutzung von usbtmc und eine kleine For-Schleife die die Frequenz auf dem Gerät ändert.

1. Verwende die Python-Bibliothek: https://github.com/python-ivi/python-usbtmc
    - Auf der Seite steht wie man die Bibliothek dann richtig installiert, hier aber kurz zusammengefasst: 
    1. Lade die Bibliothek runter
    2. entpacke die Zip-datei
    3. gehe in den Ordner der Datei (im entpackten Ordner) `setup.py`
    4. öffne in dem Ordner das Konsolenfenster
    5. führe `sudo python setup.py install` unter Linux aus

2. gebe in der Konsole "lsusb" ein
    - dadurch erfährt man die idVendor und idProduct
    - so sah es bei uns aus: Bus 001 Device 058: ID 2a8d:0396
    - 2a8d = idVendor, 0396 = idProduct
    - **Tip**: Einmal vor dem Einschalten ausführen um zu sehen was sich ändert, dadurch erfährt man schnell was zu dem Gerät gehört

3. Erstelle wie auf GitHub beschrieben die Datei "usbtmc.rules" im Ordner /etc/udev/rules.d
    - auch hier eine Kurze Vorgehensweise:
    1. Gehe in den Ordner  /etc/udev/rules.d 
    2. mit "sudo touch usbtmc.rules" kann man die Datei erstellen
    3. führe "sudo mc" aus
    4. gehe auf die Datei "usbtmc.rules" und betätige Bearbeiten
    5. trage den Text von der GitHub Seite mit den richtigen IDs ein
    6. Speichern und Beenden 

4. Weiteres    
    1. führe "sudo groupadd usbtmc" aus um die Gruppe hinzuzufügen
    2. führe "sudo usermod -a -G usbtmc pi" aus
    3. Neustart des Computers

5. führe das kleine Testprogramm auf der Github-Seite aus
    - sollte folgender Fehler auftreten dann könnte es helfen den USB-Stecker vom Gerät einmal aus und wieder ein zu stecken    
    Fehler: **usb.core.USBError: [Errno 13] Access denied (insufficient permissions)**

6. Starten   
    - Um mit der Messung zu starten muss man folgendes tun:
    1. Etwas anschließen an "Gen Out" und einen Kanal
    2. Knopf "Wave Gen" betätigen
    3. Optional: "Auto Scale" drücken

### 2.2. Befehle
Das Gerät verwendet SCPI Befehle. Mit dem Oszilloskop wollen wir in dem Experiment für die Kalibrierung die Frequenz ändern und eventuell auch den Strom messen. 

Folgende Befehle sind für das Programm relevant:     
Mit der Funktion "write" wird ein Befehl übergeben und mit "ask" gelesen. In dem Dokument "9018-07747.pdf" sind die Befehlstabellen in drei Spalten geteilt: Command für schreiben, Query für Lesen und die dritte Spalte zeigt was für Optionen man hat und was das Gerät antworten wird. Die folgenden Seitenangaben beziehen sich auf das gerade genannte Dokument!    

**Wave Generator**:     
Abkürzung: WGEN  
1. :WGEN:FREQuency `<frequency>`
    - damit kann man die Frequenz angeben die die Welle haben soll
    - Beispiel Lesen: **:WGEN:FREQuency?**
    - Beispiel Schreiben: **:WGEN:FREQuency 50**
    - S. 107 - Tabelle 38 
2. :WGEN:FUNCtion `<signal>`
    - damit kann man die Form/Funktion angeben die die Welle haben soll
    - z.B. Sinus oder Rampe 
    - Beispiel Lesen: **:WGEN:FUNCtion?**
    - Beispiel Schreiben: **:WGEN:FUNCtion SINusoid**
    - S. 107 - Tabelle 38 
3. :WGEN:VOLTage `<amplitude>`
    - damit kann man die Amplitude angeben die die Welle haben soll
    - Beispiel Lesen: **:WGEN:VOLTage?**
    - Beispiel Schreiben: **:WGEN:VOLTage 10**
    - Der Angegebene Wert ist eine Vpp Spannung (Spitze-Spitze)
    - S. 109 - Tabelle 38 

**Messungen**:    
1. :MEASure:VPP [`<source>`]
    - Misst die Spitze Spitze Spannung des angegebenen Kanals 
    - Beispiel Lesen: **:MEAS:VPP?** oder **:MEAS:VPP? CHAN2**
    - S. 83 - Tabelle 18 
2. :MEASure:VRMS [`<interval>`][,] [`<type>`][,] [`<source>`]
    - Misst die Effektive Spannung des angegebenen Kanals (RMS - Root Mean Sqaure)
    - Beispiel Lesen: **:MEAS:VRMS?** oder **:MEAS:VRMS? CHAN2**
    - S. 83 - Tabelle 18 
    - Nutzung in Programm - Kalibrierung:    
    **:MEAS:VRMS? AC, CHAN" + str(channel)**
        - Auch hier ist Default DC, also muss man auch hier AC auslesen lassen
        - der Kanal wird über die jeweilige Parameterliste angegeben

**Weitere**:
1. *IDN?
    - nur Lesbar
    - gibt die Identität des Gerätes zurück
    - Beispiel Lesen: ***IDN?** 
    - Beispiel Antwort: KEYSIGHT TECHNOLOGIES,DSOX1204G,CN61367122,02.11.2020062221
    - S. 57 - Tabelle 2 
2. :AUToscale
    - der Befehl löst ein AutoScale auf dem Bildschirm des Oszilloskops aus, jedoch kann der in den Programm nicht genutzt werden, da er das Programm stark verlangsamt 
    - S. 141 - Tabelle 45

Im **hauptprogramm_Leistung.py** werden noch weitere Befehle genutzt. Diese dienen dem Auslesen der gesamten Daten des Bildschirmes.

**Bildschirm Auslesen:**
1. :WAVeform:FORMat `<value>`
    - damit kann man das Format der Datenausgabe festlegen - ASCII bei uns 
    - Beispiel: **:WAV:FORM ASCii**
    - S. 653 - Tabelle 87
2. :WAVeform:SOURce `<source>`
    - mit dem Befehl sagt man dem Gerät welcher der 4 Kanäle ausgelesen werden soll 
    - Beispiel: **:WAVeform:SOURce CHAN" + str(self.kanalnummer)**    
    (Parameterliste - Kanalnummer)
    - S. 654 - Tabelle 87
3. :WAVeform:DATA? 
    - der Befehl liest die y-Achse des Oszilloskop vollständig aus, die Daten werden in einem String zurückgegeben und von Kommern getrennt, für Python heißt das, dass die Funktion **split** aufgerufen werden sollte
    - ***ACHTUNG***: Am Ersten Wert hängt der Header z.B. #800001000 (Beispiel der S. 663 entnommen) - im Programm wird dieser gelöscht (weggeschnitten)
    - Beispiel: **:WAVeform:DATA?**
    - S. 653 - Tabelle 87
4. :WAVeform:XINCrement?
    - der Befehl gibt die Sampling Time zurück, also die Schritte der x-Achse
    - S. 655 - Tabelle 87
    - Beispiel Ausgabe: +4.00000000E-009

### 2.3. Quellen
- https://github.com/python-ivi/python-usbtmc 
    - Python-Bibliothek für die Kommunikation über USB
- 9018-07747.pdf 
    - zu finden unter: https://www.keysight.com/de/de/assets/9018-07747/programming-guides/9018-07747.pdf (man muss eine E-Mail angeben um zugreifen zu können)
    - in dem PDF sind die Befehle zur Kommunikation gegeben
    - die Seitenzahlen beziehen sich auf das Dokument
- https://stackoverflow.com/questions/50625363/usberror-errno-13-access-denied-insufficient-permissions 
    - Lösung für Zugriffsfehler hier gefunden
- https://www.batronix.com/files/Keysight/Oszilloskope/1000X/1000X-Manual.pdf 
    - Manual