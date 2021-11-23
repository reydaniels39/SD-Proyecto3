import socket
import cv2
from random import randint

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
puerto = randint(1004, 5000)
client.bind(('localhost', puerto))
client.connect(('localhost', 1002))

data = client.recv(2048)
print(data.decode('utf-8')) #Recibimos el mensaje de confirmación de conexión y lo mostramos

data = client.recv(1024)
numIni = int(data.decode('utf-8')) #Recibimos el numero de imagen inicial

img_index = numIni
for x in range(0,29):
    file = open('./FramesRecibidos/Frame_' + str(img_index) + '.png', 'wb')
    file_part = client.recv(1024)
    while file_part != 'end'.encode():
        file.write(file_part)
        file_part = client.recv(1024)
    file.close()
    img_index += 1

tiempo = 0
while tiempo != 100:
    tiempo += 1

img_index = numIni
for x in range(0,29):
    frame_path = './FramesRecibidos/Frame_'
    frame_gris = './FramesModificados/Frame_'
    imagen = cv2.imread(frame_path+str(img_index)+'.png')
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(frame_gris + str(img_index) + '.png', gris)
    img_index += 1
cv2.destroyAllWindows()

##### Se envían las imagenes modificadas
tiempo3 = 0
while tiempo3 != 100:
    tiempo3 +=1

img_index = numIni
for x in range(0,29):
    tiempo2 = 0
    fotograma = open('./FramesModificados/Frame_' + str(img_index) + '.png', 'rb')
    fotograma_data = fotograma.read(1024)
    while fotograma_data:
        tiempo = 0
        client.send(fotograma_data)
        while tiempo != 150:                             #Tiempo entre cada envío de cada paquete para evitar corrupción de paquetes
            tiempo +=1
        fotograma_data = fotograma.read(1024)
    fotograma.close()
    client.send('end'.encode())
    while tiempo2 != 150:
        tiempo2 +=1
    img_index += 1