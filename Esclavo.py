import socket
import cv2
from random import randint

servidor = ('localhost', 1002)

print('')
print('=========== Conectando con el servidor ===========')
print('')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

direccion = '127.0.0.1' #Esta dirección es quivalente a poner localhost
puerto = randint(1004, 5000)

sock.bind((direccion, puerto))

print('=========== Registrando con el servidor... ===========')

sock.sendto('hola'.encode(), servidor)

while True:
    data = sock.recv(128).decode()

    if data.strip() == 'Hecho':
        print('')
        print('========= Registro correcto, esperando datos del otro Cliente... =========')
        print('')
        break
    

# #Direccion de donde sacamos la imagen
# imagen = cv2.imread('C:\\Users\\juan2\\Documents\\Sistemas Distribuidos\\Video\\Frames\\Frame_1.png')
# #Convertimos a escala de grises
# gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
# #Guardamos la imagen
# cv2.imwrite('C:\\Users\\juan2\\Documents\\Sistemas Distribuidos\\Video\\' + 'imagen' + '.png', gris)
