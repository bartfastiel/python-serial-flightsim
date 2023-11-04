import serial

ser = serial.Serial('COM4', 9600)

while True:
    readline = ser.readline()
    intValue = int(readline)
    print(intValue)
