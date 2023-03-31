import serial
import time

def on():
    commend='t'
    py_serial.write(commend.encode())
    time.sleep(0.1)
    if py_serial.readable():
        response = py_serial.readline()
        print(response[:len(response)-1].decode())
    print('t')
    
def off():
    commend='f'
    py_serial.write(commend.encode())
    time.sleep(0.1)
    if py_serial.readable():
        response = py_serial.readline()
        print(response[:len(response)-1].decode())
    print('f')

py_serial = serial.Serial(    
    # Window
    port='COM3',
    # 보드 레이트 (통신 속도)
    baudrate=9600,
)
