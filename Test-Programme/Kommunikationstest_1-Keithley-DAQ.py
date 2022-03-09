# Geräteadresse = 18 (GPIB)
# https://download.tek.com/manual/DAQ6510-901-01B_Sept_2019_Ref.pdf
    # - Manual für das gerät mit SCPI Befehlen und Beispielen 

import serial
import time

###########################################################################
def Read_Ausgabe():                                                       
###########################################################################
    st = ''
    back = ser_py.readline().decode()
    #print('Reading From ' + ser_py.port + ': ' + repr(back))
    st = back.replace('\n', '')                         
    return st 

portName = "/dev/ttyUSB0"

try:
    serial.Serial(port=portName)
except serial.SerialException:
    print ('Port ' + portName + ' not present')

ser_py = serial.Serial(
    port = portName,
    baudrate = int(115200),
    parity = 'N',
    stopbits = int(1),
    bytesize = int(8),
    timeout = 2.0)

ser_py.write('*RST\n'.encode())
ser_py.write((':TRACe:MAKE "voltMeasBuffer", 10000\n').encode())
for n in range(0,5,1):
    ser_py.write((':MEAS:VOLT:AC? "voltMeasBuffer", FORM, READ\n').encode())
    if n == 0:          # Multimeter spinnt ein wenig beim ersten mal wenn es die Funktion zur Messung ändern soll!
        time.sleep(5)
    answer = Read_Ausgabe()
    print(answer)

#ser_py.write((':MEAS:VOLT?\n').encode())
#answer = Read_Ausgabe()
#print(answer)

#ser_py.write((':TRACe:MAKE "currMeasBuffer", 10000\n').encode())
#ser_py.write((':MEAS:CURR? "currMeasBuffer", FORM, READ\n').encode())
#answer = Read_Ausgabe()
#print(answer)