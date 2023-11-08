import subprocess

# Esegui il comando 'netsh wlan show networks' per ottenere l'elenco delle reti disponibili
networks_info = subprocess.check_output(['netsh', 'wlan', 'show', 'network']).decode('utf-8').split('\n')

# Inizializza una lista per memorizzare le informazioni sulle reti disponibili
available_networks = []

# Analizza le informazioni ottenute
for line in networks_info:
    line = line.strip()
    if "SSID" in line:
        network_name = line.split(":")[1].strip()
        available_networks.append(network_name)

# Stampa l'elenco delle reti WiFi disponibili
print("Reti WiFi disponibili nella zona:")
for network in available_networks:
    print(network)
