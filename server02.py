import socket
import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setwarnings(False)
p = GPIO.PWM(4, 100)
q = GPIO.PWM(23, 105)
p.start(100)
q.start(100)

HOST = '192.168.0.12'
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'socket created'

try:
    s.bind((HOST, PORT))
except socket.error as err:
    print 'Bind Failed, Error Code : ' + str(err[0]) + ', Message: ' + err[1]
    sys.exit()

print 'Socket Bind Success!'

s.listen(10)
print 'Socket is now listening'

while 1:
    GPIO.setwarnings(False)
    conn, addr = s.accept()
    print 'Connect with ' + addr[0] + ' : ' + str(addr[1])
    buf = conn.recv(64)
    print buf
    data = float(buf)
    
    try:
        duty=float(buf) /10.0+2.5
        
        if data % 10 == 0 :
            p.ChangeDutyCycle(duty)
            time.sleep(0.5)
        else :
            q.ChangeDutyCycle(duty)
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
s.close()
