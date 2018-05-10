import smbus
import time

# Remplacer 0 par 1 si nouveau Raspberry
bus = smbus.SMBus(0)
address = 0x12

for i in range(1,6):
    print "Envoi de la valeur "+str(i)
    bus.write_byte(address, i)
    # Pause de 1 seconde pour laisser le temps au traitement de se faire
    time.sleep(1)
    reponse = bus.read_byte(address)
    print "La reponse de l'arduino : ", reponse
    time.sleep(1)
