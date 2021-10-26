import cv2

#Direccion de donde sacamos la imagen
imagen = cv2.imread('C:\\Users\\juan2\\Documents\\Sistemas Distribuidos\\Video\\Frames\\Frame_1.png')
#Convertimos a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
#Guardamos la imagen
cv2.imwrite('C:\\Users\\juan2\\Documents\\Sistemas Distribuidos\\Video\\' + 'imagen' + '.png', gris)
