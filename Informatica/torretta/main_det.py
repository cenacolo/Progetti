import cv2
import time

def trova_centro(frame):
    altezza, larghezza, _ = frame.shape
    centro_x = larghezza // 2
    centro_y = altezza // 2
    return centro_x, centro_y

def movimento(frame, ce_x, ce_y, x, y):
    # Esegui il controllo tra le coordinate del centro e le coordinate date
    print(f'centro x: {ce_x}, centro y: {ce_y}')
    if ce_x < x:
        print("Vai a sinistra")
    elif ce_x > x:
        print("Vai a destra")

    if ce_y < y:
        print("Vai in basso")
    elif ce_y > y:
        print("Vai in alto")

cap = cv2.VideoCapture(0) # apre la webcam

# Crea un kernel per l'erosione e l'espansione
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Inizializza la variabile per la differenza di frame
diff_frame = None

# Inizializza il contatore iniziale
start_time = time.time()

while True:
    ret, frame = cap.read() # acquisisce un frame dalla webcam

    # Trova il centro del frame
    ce_x, ce_y = trova_centro(frame)
    # x:320 y:240

    # Converte il frame in scala di grigi
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Applica un filtro gaussiano per rimuovere il rumore
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Inizializza la differenza di frame ogni volta che la variabile è vuota
    if diff_frame is None:
        diff_frame = gray_frame
        continue
    
    # Calcola la differenza di frame
    delta_frame = cv2.absdiff(diff_frame, gray_frame)
    
    # Applica una soglia binaria alla differenza di frame
    threshold_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # Applica una serie di filtri per ridurre il rumore
    threshold_frame = cv2.erode(threshold_frame, kernel, iterations=2)
    threshold_frame = cv2.dilate(threshold_frame, kernel, iterations=2)

    # Trova i contorni nel frame binario
    contours, hierarchy = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Se ci sono contorni e il tempo trascorso dall'ultimo contorno è maggiore di 1 secondo
    if contours and time.time() - start_time >= 1:
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(largest_contour)
        
        # Stampa le coordinate x e y del rettangolo
        print(f'Coordinate x: {x}, Coordinate y: {y}')
        # Esegui il controllo del movimento
        movimento(frame, ce_x, ce_y, x, y)
        print('SPARA')
        # Disegna il rettangolo delimitatore sul frame originale
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Disegna un punto nel frame correlato alle coordinate x e y
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        
        # Aggiorna il tempo dell'ultimo contorno
        start_time = time.time()
    
    # Aggiorna la differenza di frame
    diff_frame = gray_frame

    # Mostra il frame
    cv2.imshow('Webcam', frame)
    
    # Se non ci sono movimenti, fai diventare il frame grigio
    if not contours:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Webcam', gray_frame)
        print('NON SPARO')
    if cv2.waitKey(1) & 0xFF == ord('q'): # esce se l'utente preme 'q'
        break

cap.release() # rilascia la webcam
cv2.destroyAllWindows() # chiude tutte le finestre
