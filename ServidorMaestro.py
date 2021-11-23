import socket
import threading
import cv2
import numpy as np

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1002))
server.listen()

print('Esperando')

def slave(connection, numIni, nombre):
    tiempo3 = 0
    while tiempo3 != 50:
        tiempo3 +=1
    connection.send(str(numIni).encode())
    img_index = numIni
    for x in range(0,29):
        tiempo2 = 0
        fotograma = open('./Frames/Frame_' + str(img_index) + '.png', 'rb')
        fotograma_data = fotograma.read(1024)
        while fotograma_data:
            tiempo = 0
            connection.send(fotograma_data)
            while tiempo != 150:                             #Tiempo entre cada envío de cada paquete para evitar corrupción de paquetes
                tiempo +=1
            fotograma_data = fotograma.read(1024)
        fotograma.close()
        connection.send('end'.encode())
        while tiempo2 != 150:
            tiempo2 +=1
        img_index += 1

    # tiempo3 = 0
    # while tiempo3 != 30:
    #     tiempo3 +=1

    img_index = numIni
    for x in range(0,29):
        file = open('./FramesRModificados/Frame_' + str(img_index) + '.png', 'wb')
        file_part = connection.recv(1024)
        while file_part != 'end'.encode():
            file.write(file_part)
            file_part = connection.recv(1024)
        file.close()
        img_index += 1
    

slave1_socket, slave1_address = server.accept()
slave1 = threading.Thread(target=slave, args=(slave1_socket, 0, 'slave1'))
slave1_socket.send(str.encode('Conexión Exitosa'))

slave2_socket, slave2_address = server.accept()
slave2 = threading.Thread(target=slave, args=(slave2_socket, 29, 'slave2'))
slave2_socket.send(str.encode('Conexión Exitosa'))

slave3_socket, slave3_address = server.accept()
slave3 = threading.Thread(target=slave, args=(slave3_socket, 58, 'slave3'))
slave3_socket.send(str.encode('Conexión Exitosa'))

def clienteHilo(client_socket, nombre):
    #---------------------------------------------
    #EMPIEZA A RECIBIR EL VIDEO
    file = open('./archivos/video_cop.mp4', 'wb')
    video_part = client_socket.recv(2048)
    print('Recibiendo')
    while video_part:
        file.write(video_part)
        video_part = client_socket.recv(2048)

    file.close()
    client_socket.close()
    print('Exito')

    #Funcion del video
    video_path = './archivos/video_cop.mp4'
    frame_path = './Frames/Frame_'
    cap = cv2.VideoCapture(video_path)

    #Obteniendo fotogramas del video
    img_index = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite(frame_path + str(img_index) + '.png', frame)
        img_index += 1
    cap.release()
    cv2.destroyAllWindows()

    slave1.start()
    slave2.start()
    slave3.start()

    continueInput = input("Presiona cuando se termine de procesar")

    #--------------Hacer el video--------------
    img_array = []

    img_index = 0
    for x in range(0,87):
        path = './FramesRModificados/Frame_' + str(img_index) + '.png'    
        img = cv2.imread(path)
        alto, ancho, channels= img.shape
        img_array.append(img)
        img_index += 1

    video = cv2.VideoWriter('./archivos/video2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 29, (ancho, alto))
    for i in range(0,len(img_array)):
        video.write(img_array[i])
        
    video.release()
    print('Fin')


    #---------------------------------------------
    #SE ENVIA el video de vuelta al cliente
    client_socket, client_address = server.accept()
    print('Enviando')
    file = open('./archivos/video2.mp4', 'rb')
    image_data = file.read(2048)

    while image_data:
        client_socket.send(image_data)
        image_data = file.read(2048)

    file.close()
    client_socket.close()

client_sock, client_address = server.accept()
client = threading.Thread(target=clienteHilo, args=(client_sock, 'cliente'))
client.start()