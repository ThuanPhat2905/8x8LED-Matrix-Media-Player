from PIL import Image, ImageOps
import numpy as np
import csv
import serial
import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print (p)
ser = serial.Serial('COM4')

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

with Image.open('C:/Users/proki/Desktop/project TT KTMT/1.jpg') as img:
    c = ImageOps.pad(img, [8,8])
    bitmap = c.convert('1',dither=0)
    n = ""
    data = np.array(bitmap,dtype=int).T
    print(data)
    bitmap.show()
    for i in data:
        for j in i:
            n+=str((int(not(j))))
    print(n)
    bytes2send = bitstring_to_bytes(n)
    print(bytes2send)
    ser.write(bytes2send)

        