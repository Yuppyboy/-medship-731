import cv2
import numpy as np
import tensorflow as tf
from keras.preprocessing import image as im
import skvideo.io

def classify_video(vid, filename, face_detector, model):
    print('VIDEO ', vid)
    vid_array = np.frombuffer(vid.read(), np.uint8)
    print('READING VIDEO NP ', vid_array)
    # print('FILENAME ', filename)
    # videodata = skvideo.io.vread(filename)
    print('VIDEO SHAPE ', vid_array.shape)
    return None



def classify(frame, face_detector, model):

    emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    gray = frame
    detected_faces = face_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
    face_prop = []

    if len(detected_faces) > 0:

        for (x, y, w, h) in detected_faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            img = cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

            adjust_img = img[y:y+h, x:x+w]
            adjust_img = cv2.resize(adjust_img, (48, 48))

            img_tensor = tf.keras.utils.img_to_array(adjust_img)
            img_tensor = np.expand_dims(img_tensor, axis=0)

            img_tensor /= 255

            predictions = model.predict(img_tensor)
            label = emotions[np.argmax(predictions)]

            confidence = np.max(predictions)
            confidence *= 100

            detect = dict()
            detect['label'] = label
            detect['score'] = str(confidence).split(".")[0]
            detect['x'] = str(x)
            detect['y'] = str(y)
            detect['width'] = str(w)
            detect['height'] = str(h)

            face_prop.append(detect)
            print(face_prop)
            
            cv2.putText(frame, label + " : " + str(confidence), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    cv2.imwrite("somefile.jpeg", frame)

    return face_prop