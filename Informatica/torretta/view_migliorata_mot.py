import cv2
import time
import numpy as np
import odroid_wiringpi as wpi

camera_port = 0
show_video = True

# Inizializza la fotocamera
camera = cv2.VideoCapture(camera_port)
time.sleep(0.25)

# Inizializza il rilevatore di movimento di OpenCV con una soglia più bassa
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)

# Inizializza il filtro di Kalman
kalman = cv2.KalmanFilter(4, 2)
kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0]], np.float32)
kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], np.float32)
kalman.processNoiseCov = np.array([[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]], np.float32) * 0.03

wpi.wiringPiSetup()
wpi.pinMode(0, 1)## r1 = caricatore pallini
wpi.pinMode(1, 1)## r2 = sparo
wpi.pinMode(2, 1)## r3 = sicura m3  
wpi.pinMode(3, 1)## r4 = marcia+ m3 
wpi.pinMode(4, 1)## r5 = marcia- m3 
wpi.pinMode(5, 1)## r6 = sicura m1
wpi.pinMode(6, 1)## r7 = marcia- m1
wpi.pinMode(10, 1)## r8 = marcia+ m1

wpi.digitalWrite(0, 1)## r1 = caricatore pallini
wpi.digitalWrite(1, 1)## r2 = sparo
wpi.digitalWrite(2, 1)## r3 = sicura m3 
wpi.digitalWrite(3, 1)## r4 = marcia+ m3 
wpi.digitalWrite(4, 1)## r5 = marcia- m3 
wpi.digitalWrite(5, 1)## r6 = sicura m1
wpi.digitalWrite(6, 1)## r7 = marcia- m1
wpi.digitalWrite(10, 1)## r8 = marcia+ m1

# Inizializza le variabili di stato per il filtro di Kalman
last_measurement = current_measurement = np.array((2, 1), np.float32)
last_prediction = current_prediction = np.zeros((2, 1), np.float32)

# Funzione per calcolare il quadrante
def get_quadrant(center_x, center_y):
    if center_x < 400 and center_y < 300:
        return "Sinistra in alto"
    elif center_x < 400 and center_y >= 300:
        return "Sinistra in basso"
    elif center_x >= 400 and center_y < 300:
        return "Destra in alto"
    else:
        return "Destra in basso"

def attiva_motori(motori):
    for motore in motori:
        wpi.digitalWrite(motore, 0)

def disattiva_motori(motori):
    for motore in motori:
        wpi.digitalWrite(motore, 1)
# Funzione per il movimento verso sinistra
def move_left():
    attiva_motori([2, 3, 4])

# Funzione per il movimento verso destra
def move_right():
    disattiva_motori([3, 4])
    attiva_motori([2])

# Funzione per il movimento verso l'alto
def move_up():
    disattiva_motori([6, 10])
    attiva_motori([5])

# Funzione per il movimento verso il basso
def move_down():
    attiva_motori([5, 6, 10])

# Funzione per fermare il movimento
def stop_movement():
    disattiva_motori([2, 3, 4, 5, 6, 10])

# Loop sui frame del video
while True:
    (grabbed, frame) = camera.read()

    if not grabbed:
        break

    frame = cv2.resize(frame, (800, 600))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    fgmask = fgbg.apply(gray)

    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, None, iterations=2)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, None, iterations=2)

    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_area = 1000
    best_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > best_area:
            best_area = area
            best_cnt = cnt

    if best_cnt is not None:
        (x, y, w, h) = cv2.boundingRect(best_cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        center_x = x + w // 2
        center_y = y + h // 2

        current_measurement = np.array([[np.float32(center_x)], [np.float32(center_y)]])
        kalman.correct(current_measurement)

        prediction = kalman.predict()
        center_x, center_y = prediction[0], prediction[1]

        cv2.circle(frame, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)

        quadrant = get_quadrant(center_x, center_y)
        print("Quadrante:", quadrant)

        # Gestione del movimento in base al quadrante
        if quadrant == "Sinistra in alto":
            move_left()
            move_up()
        elif quadrant == "Sinistra in basso":
            move_left()
            move_down()
        elif quadrant == "Destra in alto":
            move_right()
            move_up()
        elif quadrant == "Destra in basso":
            move_right()
            move_down()
        else:
            stop_movement()

    else:
        stop_movement()

    if show_video:
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()
