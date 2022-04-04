# Auswertungsprogramme:

## Profil:
Die beiden folgenden Programme sind nahezu identisch. 
### Profil_Kurvenschar_Zeit_Hall-Spannung.py
Mit dem Programm werden die Kurven der gemessenen Profile in einem Diagramm dargestellt. In dem Programm übergibt man die Kurven bzw. Text-Datein über ein Dictionerie. Diese werden dann in einer Schleife ausgelesen und in der Funktion **Kurven_Plot** bearbeitet und die Kurve erstellt. Wenn alle Daten ausgelesen sind wird das Diagramm erstellt. Dieses muss von Hand gespeichert werden. 

### Profil_Kurvenschar_Weg-Rot_Magnetfeld.py
Mit dem Programm werden die Kurven der umgerechneten Profile in einem Diagramm dargestellt. In dem Programm übergibt man die Kurven bzw. Text-Datein über ein Dictionerie. Diese werden dann in einer Schleife ausgelesen und in der Funktion **Kurven_Plot** bearbeitet und die Kurve erstellt. Wenn alle Daten ausgelesen sind wird das Diagramm erstellt. Dieses muss von Hand gespeichert werden. 

### Profil_Umrechnung.py
In dem Programm werden die Profile umgerechnet. Beachten muss man das sowohl der Datei-Pfad als auch die Werte für Bewegungsrichtung, Frequenz, Start- und Endwerte in dem Programm per Hand eingetragen werden müssen. Im folgenden wird der Korrekturwert für die angegebene Frequenz berechnet. Danach wird die Magnetische Flussdichte berechnet und gleich mit dem Korrekturwert berichtigt. Im Anschluss wird nach Auswahl ein Weg oder ein Winkel berechnet. Zur gleichen Zeit wird an der Entscheidung das Diagramm und die neue Text-Datei erstellt. 

## Kalibrierung:
### Auswertung_Text-Datei.py
Das Programm liest die Messdatei aus die vom Hauptprogramm (hauptprogramm_Kalibrierung.py) erstellt wurde. Aus den Daten werden dann 5 Diagramme erstellt die in einem Plot (mit Subplots) gezeigt werden. Mit den Daten werden der Strom und die Magnetische Flussdichte berechnet. Das Bild wird am Ende vom Programm gespeichert. 



