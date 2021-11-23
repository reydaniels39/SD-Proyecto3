import socket
import cv2
from random import randint
import threading

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
        print('========= Registro correcto... =========')
        print('')
    if data.strip() == 'Hola esclavo':
        print('iniciar escucha y decir')
        break

def escuchar():
    frame_gris = './FramesModificados/Frame_'
    while True:
        data = sock.recv(2048).decode()  #Recibimos el mensaje
        print(data)
        archivo = frame_gris + data + '.png'
        file = open(frame_gris + data + '.png', 'wb')    #la posicion 0 de nombreArchivo contiene el nombre y extensión
        img_part = sock.recv(1024)
        print("\nRecibiendo archivo")
        while img_part:
            file.write(img_part)
            img_part = sock.recv(1024)
        file.close()
        print("Archivo Recibido")

        print(archivo)
        #colorgris(archivo)
        # imagen = cv2.imread(archivo)
        # gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite(archivo, gris)
       
def decir():
    while True:
        sock.sendto(''.encode(), servidor)

def colorgris(ruta):
    imagen = cv2.imread(ruta)
    #Convertimos a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    #Guardamos la imagen
    cv2.imwrite(ruta, gris)

escuchar = threading.Thread(target=escuchar)   #creamos el hilo para la función escuchar


escuchar.start()    #Iniciamos el hilo escuchar

        




#Cambia el color
# def color(img_cont):
#     #Direccion de donde sacamos la imagen
#     ruta = 'C:\\Users\\juan2\\Documents\\Sistemas Distribuidos\\Video\\Frames\\Frame_'
#     imagen = cv2.imread(ruta + str(img_cont) + '.png')
#     #Convertimos a escala de grises
#     gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
#     #Guardamos la imagen
#     cv2.imwrite(ruta + str(img_cont) + '.png', gris)

# print('Iniciando el cambio de color')
# threads = []
# img_cont = 0
# for _ in range(p):
#     t = threading.Thread(target= color, args=[img_cont])
#     t.start()
#     threads.append(t)
#     img_cont += 1

# for thread in threads:
#     thread.join()
# print('Finalizado cambio de color')

# #Direccion de donde sacamos la imagen
# imagen = cv2.imread('C:\\Users\\juan2\\Documents\\Sistemas Distribuidos\\Video\\Frames\\Frame_1.png')
# #Convertimos a escala de grises
# gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
# #Guardamos la imagen
# cv2.imwrite('C:\\Users\\juan2\\Documents\\Sistemas Distribuidos\\Video\\' + 'imagen' + '.png', gris)
