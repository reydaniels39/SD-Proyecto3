import socket
#import cv2 #Es la libreria de OpenCV. Se debe instalar con el comando "pip install opencv-contrib-python"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1002))

# #Aquí enviamos la imagen encriptada
print('Enviando')
file = open('./archivos/video.mp4', 'rb')
video_data = file.read(2048)

while video_data:
    client.send(video_data)
    video_data = file.read(2048)

file.close()
client.close()
print('Exito')


#------------------------------------------
#SE RECIBE EL VIDEO CONVERTIDO EN BLANCO Y NEGRO
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1002)) #192.168.1.252

print('Pidiendo video')
file = open('./archivos/videoGris.mp4', 'wb')
video_part = client.recv(2048)
print('Recibiendo')
while video_part:
    file.write(video_part)
    video_part = client.recv(2048)

file.close()
client.close()
print('Exito')