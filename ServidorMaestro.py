import socket
import cv2
import numpy as np

def conectarCliente():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1002)) 
    server.listen()

    print('Esperando Cliente')

    client_socket, client_address = server.accept()

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
    print('Exito, video recibido')

    #Funcion del video
    video_path = './archivos/video_cop.mp4'
    frame_path = './Frames/Frame_'
    #frame_gris = './FramesModificados/Frame_'
    cap = cv2.VideoCapture(video_path)


    # img_index = 0
    # while (cap.isOpened()):
    #     ret, frame = cap.read()
    #     if ret == False:
    #         break
    #     cv2.imwrite(frame_path + str(img_index) + '.png', frame)
    #     #imagen = cv2.imread(frame_path+str(img_index)+'.png')
    #     #gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    #     #cv2.imwrite(frame_gris + str(img_index) + '.png', gris)
    #     img_index += 1

    # cap.release()
    # cv2.destroyAllWindows()

    #--------------Hacer el video--------------
    # img_array = []

    # img_index = 0
    # for x  in range(0,87):
    #     path = './FramesModificados/Frame_' + str(img_index) + '.png'    
    #     img = cv2.imread(path)
    #     alto, ancho, channels= img.shape
    #     img_array.append(img)
    #     img_index += 1

    # video = cv2.VideoWriter('./archivos/video2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 29, (ancho, alto))
    # for i in range(0,len(img_array)):
    #     video.write(img_array[i])
        
    # video.release()
    # print('Fin')


    #---------------------------------------------
    #SE ENVIA el video de vuelta al cliente
    # client_socket, client_address = server.accept()
    # print('Enviando')
    # file = open('./archivos/video2.mp4', 'rb')
    # image_data = file.read(2048)

    # while image_data:
    #     client_socket.send(image_data)
    #     image_data = file.read(2048)

    # file.close()
    # client_socket.close()

def conectarEsclavos():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('localhost', 1002)) #192.168.1.252

    slaves = []

    while True:
        data, address = server.recvfrom(128)

        print('Esclavo conectado: "{}"'.format(data.decode()) + ' desde: {}.'.format(address))
        slaves.append(address)

        server.sendto(b'Hecho', address)

        if len(slaves) == 3:
            print('')
            print('Conectados todos los esclavos')
            print('')
            conectarCliente()
            
            server.sendto(b'Hola esclavo', slaves[0])
            server.sendto(b'Hola esclavo', slaves[1])
            server.sendto(b'Hola esclavo', slaves[2])
            break
    
    enviarAEsclavos(server, slaves)

def enviarAEsclavos(server, slaves):
    frame_path = './Frames/Frame_'
    cont = 0
    while True:
        if(cont < 28):
            msg = str(cont)
            server.sendto(msg.encode(), slaves[0])
            file = open(frame_path + str(cont) + '.png', 'rb')
            img_data = file.read(1024)
            while img_data:
                server.sendto(img_data, slaves[0])
                img_data = file.read(1024)
            server.sendto(''.encode(), slaves[0])  #Envia un mensaje vacío para salir del ciclo de recibir
            #print('esclavo1')
            #print(slaves[0])
        elif(cont >=29 and cont < 58):
            msg = str(cont)
            server.sendto(msg.encode(), slaves[1])
            file = open(frame_path + str(cont) + '.png', 'rb')
            img_data = file.read(1024)
            while img_data:
                server.sendto(img_data, slaves[1])
                img_data = file.read(1024)
            server.sendto(''.encode(), slaves[1])
            # print('esclavo2')
            # print(slaves[1])
        elif(cont >=58 and cont < 87):
            msg = str(cont)
            server.sendto(msg.encode(), slaves[2])
            file = open(frame_path + str(cont) + '.png', 'rb')
            img_data = file.read(1024)
            while img_data:
                server.sendto(img_data, slaves[2])
                img_data = file.read(1024)
            server.sendto(''.encode(), slaves[2])
            # print('esclavo3')
            # print(slaves[2])
        cont = cont + 1



conectarEsclavos()
