# Evaluation programs:

## Profile
The following two programs are almost identical.

### Profil_Kurvenschar_Zeit_Hall-Spannung.py
The program displays the curves of the measured profiles in a diagram. In the program, the curves or text files are passed on via a dictionary. These are then read out in a loop and processed in the **Kurven_Plot** function and the curve is created. Once all the data has been read out, the diagram is created. This must be saved manually.

### Profil_Kurvenschar_Weg-Rot_Magnetfeld.py
The program displays the curves of the converted profiles in a diagram. In the program, the curves or text files are passed through a dictionary. These are then read out in a loop and processed in the **Kurven_Plot** function and the curve is created. Once all the data has been read out, the diagram is created. This must be saved manually.

### Profil_Umrechnung.py
The profiles are converted in the program. It is important to note that both the file path and the values ​​for the direction of movement, frequency, start and end values ​​must be entered into the program by hand. The correction value for the specified frequency is then calculated. The magnetic flux density is then calculated and immediately corrected with the correction value. A path or angle is then calculated after selection. At the same time, the diagram and the new text file are created based on the decision.

## Calibration
### Auswertung_Text-Datei.py
The program reads the measurement file that was created by the main program (hauptprogramm_Kalibrierung.py). The data is then used to create 5 diagrams that are shown in a plot (with subplots). The data is used to calculate the current and the magnetic flux density. The image is saved by the program at the end.

