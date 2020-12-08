import cv2

# Opens the Video file
cap= cv2.VideoCapture('/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Volkswagen_Oficial_Images/volkswagen_2/volkswagen_2.mp4')
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite('/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Volkswagen_Oficial_Images/volkswagen_2/volkswagen_2_'+str(i)+'.png',frame)
    print('volkswagen_2_',str(i),'.png')
    i+=1

cap.release()
cv2.destroyAllWindows()
