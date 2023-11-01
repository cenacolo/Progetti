import cv2
import time
import numpy as np

camera_port = 0  # Puoi cambiare questa porta fotocamera se necessario
show_video = True  # Imposta su True se desideri visualizzare il video

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

# Loop sui frame del video
while True:
    # Acquisisci il frame corrente
    (grabbed, frame) = camera.read()

    # Se il frame non può essere acquisito, abbiamo raggiunto la fine del video
    if not grabbed:
        break

    # Ridimensiona il frame e convertilo in scala di grigi
    frame = cv2.resize(frame, (800, 600))  # Aumentato le dimensioni del frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calcola la maschera di movimento utilizzando il background subtractor
    fgmask = fgbg.apply(gray)

    # Applica una serie di operazioni morfologiche per rimuovere il rumore
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, None, iterations=2)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, None, iterations=2)

    # Trova i contorni nell'immagine della maschera
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_area = 1000  # Riduci la soglia per considerare anche i piccoli movimenti
    best_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > best_area:
            best_area = area
            best_cnt = cnt

    if best_cnt is not None:
        # Calcola il bounding box per il contorno, disegnalo sul frame
        (x, y, w, h) = cv2.boundingRect(best_cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calcola il centro del riquadro
        center_x = x + w // 2
        center_y = y + h // 2

        # Misura il movimento
        current_measurement = np.array([[np.float32(center_x)], [np.float32(center_y)]])
        kalman.correct(current_measurement)

        # Stampa la posizione corretta dal filtro di Kalman
        prediction = kalman.predict()
        center_x, center_y = prediction[0], prediction[1]

        # Disegna il punto rosso al centro del riquadro
        cv2.circle(frame, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)

        # Ottieni il quadrante e stampalo su terminale
        quadrant = get_quadrant(center_x, center_y)
        print("Quadrante:", quadrant)

    # Suddividi il video in 4 quadranti
    cv2.line(frame, (400, 0), (400, 600), (0, 255, 0), 2)  # Aggiorna le coordinate
    cv2.line(frame, (0, 300), (800, 300), (0, 255, 0), 2)  # Aggiorna le coordinate

    # Mostra il frame e registra se l'utente preme un tasto
    if show_video:
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        # Se il tasto 'q' viene premuto, esci dal loop
        if key == ord("q"):
            break

# Libera la fotocamera e chiudi tutte le finestre aperte
camera.release()
cv2.destroyAllWindows()
