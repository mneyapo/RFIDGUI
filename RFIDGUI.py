#!/usr/bin/env python3.5
#-- coding: utf-8 --
from gpiozero import LED, Buzzer
from guizero import App, Box, Text, TextBox, warn,Picture,Window,PushButton
import csv
import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs
from pirc522 import RFID
import time
from PIL import Image
rc522 = RFID() #On instancie la lib

print('En attente d\'un badge (pour quitter, Ctrl + c): ') #On affiche un message demandant à l'utilisateur de passer son badge
 
#def open_window():
#    window.show()
    
def open_window():
    app.show(wait=True)
    
def close_window():
    app.destroy()

def clearDisplay():
    print("Clear display")
    rfidStatus.value = "---"
    rfidText.value = ""
    #led8.off()
    picture.value = "images/rfid-reader-icon-14.png"
    rfidStatus.repeat(1000, checkRFidTag)
    
    
def taguid():
    rc522.wait_for_tag() #On attnd qu'une puce RFID passe à portée
    (error, tag_type) = rc522.request() #Quand une puce a été lue, on récupère ses infos
    if not error : #Si on a pas d'erreur
        (error, uid) = rc522.anticoll() #On nettoie les possibles collisions, ça arrive si plusieurs cartes passent en même temps
        if not error : #Si on a réussi à nettoyer
            print('Vous avez passé le badge avec l\'id : {}'.format(uid)) #On affiche l'identifiant unique du badge RFID
            rfidText.value = ''.join('{:02x}'.format(x) for x in uid[:4]).upper()
            time.sleep(1) #On attend 1 seconde pour ne pas lire le tag des centaines de fois en quelques milli-secondes
    return rfidText.value

def resizing_Image(image):
    basewidth = 300
    path='images/'+image
    img = Image.open(path)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(path)
    print("Path Imgae: ",path)
    
def checkRFidTag():
    tagId = taguid()
    if tagId != "":
        RFidRegistered = False
        print(tagId)
        with open("Database.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["RFid"] == tagId:
                    RFidRegistered = True
                    print("Welcome " + row["User"])
                    rfidStatus.value = "Welcome " + row["User"]
                    if rfidText.value=="9336D424":
                        resizing_Image("9336D424.png")
                        picture.value = "images/9336D424.png"
                    rfidStatus.after(5000, clearDisplay)
                    #picture.repeat(5000, destroy(), args=None)
                    
        if RFidRegistered == False:
            print("RFid tag is not registered")
            rfidStatus.value = "RFid tag is not registered"
            picture.value = "images/images.png"
            rfidStatus.after(3000, clearDisplay)
        
        rfidStatus.cancel(checkRFidTag)

app = App(title="RFID Simple GUI", width=750, height=750, layout="auto")

instructionText = Text(app, text="En attente d\'un badge\n scan your RFid tag.")
rfidText = TextBox(app)
rfidText.focus()
rfidStatus = Text(app, text="---")
rfidStatus.repeat(1000, checkRFidTag)
picture = Picture(app, image="images/rfid-reader-icon-14.png",width=512, height=512)
designBy = Text(app, text="Design by Maroiane Nasrellah - YAPO MAROC", align="bottom")
#
close_button = PushButton(app, text="Close", command=close_window,align="bottom")
app.display()
