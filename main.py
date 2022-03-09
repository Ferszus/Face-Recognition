import cv2
import math
import pickle


face_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_eye.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = {"person_name": 1}
with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}


i=0
camera = cv2.VideoCapture(0)



while (True):
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    
    for (x, y, w, h) in faces:
        roi_grey = gray[y:y+h, x:x+y]
        roi_color = gray[y:y+h, x:x+y]
        # RECOGNIZE
        id_, conf = recognizer.predict(roi_grey)
        if conf>=75: # and conf <= 85:
            #print(id_)
            #print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

        img_item = "my-image.png"
        #cv2.imwrite(img_item, roi_grey)

        color = (0, 255, 0) #BGR 0-255
        stroke = 2
        end_cord_x = x+w
        end_cord_y = y+h

        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        eyes = eye_cascade.detectMultiScale(roi_grey)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_grey, (ex, ey), (ex+ew, ey+eh), (255,0,0), 2)



    # Wyswietlanie
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
camera.release()