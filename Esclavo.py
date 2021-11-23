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
while tiempo != 50:
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

# #Direccion de donde sacamos la imagen
# imagen = cv2.imread('C:\\Users\\juan2\\Documents\\Sistemas Distribuidos\\Video\\Frames\\Frame_1.png')
# #Convertimos a escala de grises
# gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
# #Guardamos la imagen
# cv2.imwrite('C:\\Users\\juan2\\Documents\\Sistemas Distribuidos\\Video\\' + 'imagen' + '.png', gris)
