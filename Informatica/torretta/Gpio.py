import odroid_wiringpi as wpi
import time
 
## pin fisico 0 = 11, 1= 12, 2= 13
wpi.wiringPiSetup()
wpi.pinMode(0, 1)
wpi.pinMode(1, 1)
wpi.pinMode(2, 1)
 
##while True:
  ##  wpi.digitalWrite(0, 1)
    ##time.sleep(1)
    ##wpi.digitalWrite(0, 0)
    ##time.sleep(1)

def main():

    try:
        while True:
            # Tutti i pin spenti
            wpi.digitalWrite(0, 0)
            wpi.digitalWrite(1, 0)
            wpi.digitalWrite(2, 0)
            time.sleep(2)

            # Pin 1 acceso
            wpi.digitalWrite(0, 1)
            time.sleep(2)
            ## Pin 1 spento
            wpi.digitalWrite(0, 0)
            time.sleep(2)

            # Tutti i pin accesi
            ##wpi.digitalWrite(1, 1)
            ##wpi.digitalWrite(2, 1)
            ##time.sleep(2)

    except KeyboardInterrupt:
        # Interrompi il programma se viene premuto Ctrl+C
        pass

    finally:
        # Pulisci le impostazioni dei pin alla fine del programma
        GPIO.cleanup()

if __name__ == "__main__":
    main()
