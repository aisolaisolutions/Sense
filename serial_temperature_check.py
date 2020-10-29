import serial
ser=serial.Serial("/dev/ttyUSB0",9600)  #change USB number as found from ls /dev/tty/USB*
ser.baudrate=9600

## Code edit for arduino Wired communication
read_ser=ser.readline()
command = read_ser.decode("utf-8").strip()#Convert byte to string ASCII utf-8
print(command)
print(type(command)) #Edit Sameer

if sensor ==1:
            cv2.putText(frame, dist, (10,90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
else:
    cv2.putText(frame, dist, (10,90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    




