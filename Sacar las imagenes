#pip install opencv-python
import cv2
#--------------obtener las imagenes--------------
video_path = 'C:\\Users\\juan2\\Documents\\Sistemas Distribuidos\\Video\\video.mp4'
frame_path = 'C:\\Users\\juan2\\Documents\\Sistemas Distribuidos\\Video\\Frames\\Frame_'
cap = cv2.VideoCapture(video_path)

img_index = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite(frame_path + str(img_index) + '.png', frame)
    img_index += 1

cap.release()
cv2.destroyAllWindows()

#--------------Hacer el video--------------
img_array = []

img_index = 0
for x  in range(0,87):
    path = 'C:\\Users\juan2\\Documents\\Sistemas Distribuidos\\Video\\Frames modificados\\Frame_' + str(img_index) + '.png'    
    img = cv2.imread(path)
    img_array.append(img)
    img_index += 1

alto, ancho = img.shape[:2]
video = cv2.VideoWriter('Video2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 29, (ancho, alto))
for i in range(0,len(img_array)):
    video.write(img_array[i])
    
video.release()
print('Fin')
