import cv2
import os
import numpy as np
import pandas as pd
import telepot
import pygame
import time
from gtts import gTTS
from mutagen.mp3 import MP3
import time
import serial
import time

# Create Local Binary Patterns Histograms for face recognization
##recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load the trained mode
recognizer.read('trainer/trainer.yml')
##recognizer.read('/home/pi/Desktop/face_recog_folder/Raspberry-Face-Recognition-master/trainer/trainer.yml')

# Load prebuilt model for Frontal Face
cascadePath = "haarcascade_frontalface_default.xml"

# Create classifier from prebuilt model
faceCascade = cv2.CascadeClassifier(cascadePath);

# Set the font style
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize and start the video frame capture
df=pd.read_csv('names.csv')

data = serial.Serial(
         'COM3',
          baudrate = 9600,
          parity=serial.PARITY_NONE,
          stopbits=serial.STOPBITS_ONE,
          bytesize=serial.EIGHTBITS,                  
          timeout=1
          )

def Play(text1):
        print(text1)
        myobj = gTTS(text=text1, lang='en-us', tld='com', slow=False)
        myobj.save("voice.mp3")
        print('\n------------Playing--------------\n')
        song = MP3("voice.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load('voice.mp3')
        pygame.mixer.music.play()
        time.sleep(song.info.length)
        pygame.quit()


        

print('start........')
 
cam = cv2.VideoCapture(0)
names = []
counts = 0
while True:
        # Read the video frame
        ret, im =cam.read()

        # Convert the captured frame into grayscale
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

        # Get all face from the video frame
        faces = faceCascade.detectMultiScale(gray, 1.2,5)


        # For each face in faces
        for(x,y,w,h) in faces:
            counts += 1

            # Create rectangle around the face
            cv2.rectangle(im, (x,y), (x+w,y+h), (0,255,0), 4)

            # Recognize the face belongs to which ID
            Id,i = recognizer.predict(gray[y:y+h,x:x+w])

            if i < 50:
                name=df.loc[(df['id']==Id)]['name'].values[0]
                cv2.putText(im, name, (x,y-40), font, 2, (255,255,255), 3)
                names.append(name)
            else:
                cv2.putText(im, "unknown", (x,y-40), font, 2, (255,255,255), 3)
                names.append("unknown")
                cv2.imwrite('frame.png', im)

        # Display the video frame with the bounded rectangle
        cv2.imshow('im',im)
        
        # If 'q' is pressed, close program
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        if counts > 15:
                break
           
cam.release()
# Close all windows
cv2.destroyAllWindows()
        
counter = 0
num = names[0]

for i in names:
        curr_frequency = names.count(i)
        if(curr_frequency> counter):
                counter = curr_frequency
                num = i

if num == "unknown":
        bot = telepot.Bot("6684438305:AAHIBn07eCMX96he8g2bi4NNHIqS0oI_mWY")
        bot.sendMessage('5675390154', str('unknown person detected'))
        bot.sendPhoto('5675390154', photo = open('frame.png', 'rb'))
        def handle(msg):
            print(msg['text'])
            if msg["text"] == 'Y':
                    print('ppp')
                    data.write(str.encode('C'))
            else:
                    data.write(str.encode('B'))
        bot.message_loop(handle)
else:
        print(num)
        data.write(str.encode('A'))

        


