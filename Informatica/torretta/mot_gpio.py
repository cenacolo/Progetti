import odroid_wiringpi as wpi
##controllare se installata la dipendenza
import time
import keyboard
 
## pin fisico 0 = 11, 1= 12, 2= 13
wpi.wiringPiSetup()
wpi.pinMode(0, 1)## r1 = caricatore pallini
wpi.pinMode(1, 1)## r2 = sparo
wpi.pinMode(2, 1)## r3 = marcia+ m3 
wpi.pinMode(3, 1)## r4 = sicura m3
wpi.pinMode(4, 1)## r5 = marcia- m3 
wpi.pinMode(5, 1)## r6 = marcia- m1
wpi.pinMode(6, 1)## r7 = sicura m1
wpi.pinMode(10, 1)## r8 = marcia+ m1

def destra():
    wpi.digitalWrite(3,1)
        
def sinistra():
    wpi.digitalWrite(2,1)
    wpi.digitalWrite(3,1)
    wpi.digitalWrite(4,1)

def alto():
    wpi.digitalWrite(7,1)

def basso():
    wpi.digitalWrite(5,1)
    wpi.digitalWrite(6,1)
    wpi.digitalWrite(10,1)

def ferma():
    wpi.digitalWrite(2, 0)
    wpi.digitalWrite(3, 0)
    wpi.digitalWrite(4, 0)
    wpi.digitalWrite(5, 0)
    wpi.digitalWrite(6, 0)
    wpi.digitalWrite(10, 0)

def sparo():
    wpi.digitalWrite(0,1)
    wpi.digitalWrite(1,1)
    time.sleep(5)
    wpi.digitalWrite(0, 0)
    wpi.digitalWrite(1, 0)
    
try:
    while True:
        destra()
        time.sleep(1)  # Puoi regolare la durata del movimento destro cambiando il valore in sleep
except KeyboardInterrupt:
    print("Interrotto dall'utente")
finally:
    # Alla fine, ferma il motore destro
    wpi.digitalWrite(3, 0)
