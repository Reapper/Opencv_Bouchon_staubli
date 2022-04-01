#!/usr/bin/python3
# -*- coding: utf-8 -*
# Bertrand Vandeportaele 2022
import re  # pour découpage chaine comme sur https://stackoverflow.com/questions/2175080/sscanf-in-python
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
from PyQt5.QtGui import *
import subprocess
import os
import sys

debug = True

global numeroPremiereDonneeCapteur
# TODO: donner une valeur à cette variable en fonction de votre numéro d'étudiant
numeroPremiereDonneeCapteur = 1200

global destIP
global portOut

global etatBouton
etatBouton = 0
global slider1Value
slider1Value = 0
global slider2Value
slider2Value = 0
global slider3Value
slider3Value = 0
global slider4Value
slider4Value = 0

global led0Button


########################################
# https://stackoverflow.com/questions/1051254/check-if-python-package-is-installed
# install automatically watchdog if not already installed

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

if 'PyQt5' in installed_packages:
    if debug:
        print('PyQt5 pip package already installed')
else:
    if debug:
        print('PyQt5 pip package missing, lets install it')
    import pip
    pip.main(['install', 'PyQt5'])

########################################


################################################################################
def close():
    print('close')
    exit(0)
################################################################################


def commutTimer():
    global timer
    print('commutTimer')
    if timer.isActive():
        timer.stop()
        commutTimerButton.setText('start stream sensor')
    else:
        timer.start()
        commutTimerButton.setText('stop stream sensor')
################################################################################


def slider1ValueChanged(value):
    # label.setText( str( value )
    global numeroPremiereDonneeCapteur
    global labelSlider1Value
    global slider1Value
    slider1Value = value
    labelSlider1Value.setText(
        str(numeroPremiereDonneeCapteur+5)+" :  {:6d}".format(slider1Value))
    # print('changed')
################################################################################


def slider2ValueChanged(value):
    # label.setText( str( value )
    global numeroPremiereDonneeCapteur
    global labelSlider2Value
    global slider2Value
    slider2Value = value
    labelSlider2Value.setText(
        str(numeroPremiereDonneeCapteur+6)+" : {:6d}".format(slider2Value))
    # print('changed')
################################################################################


def slider3ValueChanged(value):
    # label.setText( str( value )
    global numeroPremiereDonneeCapteur
    global labelSlider3Value
    global slider3Value
    slider3Value = value
    labelSlider3Value.setText(
        str(numeroPremiereDonneeCapteur+7)+" : {:6d}".format(slider3Value))
    # print('changed')
################################################################################


def slider4ValueChanged(value):
    # label.setText( str( value )
    global numeroPremiereDonneeCapteur
    global labelSlider4Value
    global slider4Value
    slider4Value = value
    labelSlider4Value.setText(
        str(numeroPremiereDonneeCapteur+8)+" : {:6d}".format(slider4Value))
    # print('changed')
################################################################################


def bouton0():
    global numeroPremiereDonneeCapteur
    global labelButtonValue
    global led0Button
    global etatBouton
    etatBouton = (etatBouton+1) % 2
    if etatBouton == 0:
        led0Button.setText('Activer la sortie TOR')
    else:
        led0Button.setText('Desactiver la sortie TOR')
    labelButtonValue.setText(
        str(numeroPremiereDonneeCapteur+2)+" : {:6d}".format(etatBouton))
    print('etatBouton: ' + str(etatBouton) + " \n")

################################################################################


def sendUDP(i):
    global udpSocket
    global destIP
    global portOut
    DestIP = QHostAddress(destIP)
    global slider1Value
    global slider2Value
    global slider3Value
    global slider4Value
    global etatBouton
    global numeroPremiereDonneeCapteur
#  chaine=str(slider1Value)+ " " + str(slider2Value)
# ajout @MAC bidon
#  chaine="00:00:00:00:00:00 "+str(slider1Value)+ " " + str(slider2Value)
# ajout champs vides pour être compatible avec le joystick wifi
# @MAC: BC:DD:C2:FE:6F:F0 num: 0 0 -> 529.0 , 1 -> 534.0 , 2 -> 0.0 , 3 -> 0.0 , 4 -> 0.0 , 5 -> -73.0 , 6 -> 63.0 ,
    chaine = "00:00:00:00:00:00 " + \
             str(numeroPremiereDonneeCapteur) + \
             " 0 0 " + \
             str(etatBouton) + \
             " 0 0 " +\
             str(slider1Value) + \
             " " + \
             str(slider2Value) + \
             " " + \
             str(slider3Value) + \
             " " + \
             str(slider4Value)

# chaines bidons pour générer erreur de parsing sur le serveur
#  chaine="00:00:00:00:00:00 0 0 0 "+"687f"+" 0 0 "+str(slider1Value)+ " " + str(slider2Value)

    chaine = chaine+chr(13)+chr(10)
    print("la chaine envoyée vers ip: "+str(destIP) +
          ":"+str(portOut) + " est: "+chaine)
    udpSocket.writeDatagram(chaine.encode('utf-8'), DestIP, portOut)

################################################################################


def timerUpdate():
    sendUDP(0)
################################################################################


global led0Button
# destIP='192.168.1.50' #pc simulateur
# destIP='192.168.0.112' #pc simulateur
# destIP='192.168.1.49' #pc serveur rapid connecté en filaire à réseau AIP
# destIP='127.0.0.1' #pc serveur sur la boucle locale
# destIP='192.168.3.5' #pc serveur rapid connecté en wifi à réseau AIP
# destIP='192.168.3.4' #pc serveur rapid connecté en ethernet à réseau AIP
# destIP='127.0.0.1' #ip locale
# destIP='10.6.11.62' #un pc de la salle u2 IUT

destIP = '10.6.7.124'  # rapid connecté sur gommette bleu


portOut = 10000
posx = 100
posy = 100
sizex = 500
sizey = 150
################################################################################
app = QApplication(sys.argv)
w = QDialog()
statusLabel = QLabel('En attente de datagrammes UDP depuis le PIC32')
commutTimerButton = QPushButton('stop stream sensor')
quitButton = QPushButton('&Quit')
led0Button = QPushButton('Activer la sortie TOR')

udpSocket = QUdpSocket()
udpSocket.bind(portOut, QUdpSocket.ShareAddress)

quitButton.clicked.connect(close)
commutTimerButton.clicked.connect(commutTimer)
led0Button.clicked.connect(bouton0)
# led1Button.clicked.connect(bouton1)
# led2Button.clicked.connect(bouton2)

#app.connect(quitButton,QtCore.SIGNAL('clicked()'), close)
#app.connect(commutTimerButton,  QtCore.SIGNAL('clicked()'), commutTimer)
#app.connect(led0Button,QtCore.SIGNAL('clicked()'), bouton0)

buttonLayout = QHBoxLayout()
buttonLayout.addStretch(1)
buttonLayout.addWidget(quitButton)
buttonLayout.addWidget(commutTimerButton)
buttonLayout.addStretch(1)

global labelButtonValue
labelButtonValue = QLabel()
labelButtonValue.setGeometry(250, 50, 50, 35)
#labelButtonValue.setText( "x: "+str(0 ) )
labelButtonValue.setText(
    str(numeroPremiereDonneeCapteur+2)+" : {:6d}".format(0))

button1Layout = QHBoxLayout()
button1Layout.addStretch(1)
button1Layout.addWidget(labelButtonValue)
button1Layout.addStretch(1)
button1Layout.addWidget(led0Button)
button1Layout.addStretch(1)


# ""
# http://koor.fr/Python/CodeSamplesQt/PyQtSlider.wp
slider1 = QSlider(Qt.Horizontal)
amplitude = 1800
slider1.setMinimum(int(-amplitude/2))
slider1.setMaximum(int(amplitude/2))
slider1.setGeometry(10, 10, 600, 40)
slider1.valueChanged.connect(slider1ValueChanged)
slider1.setValue(0)
global labelSlider1Value
labelSlider1Value = QLabel()
labelSlider1Value.setGeometry(250, 50, 50, 35)
#labelSlider1Value.setText( "x: "+str(0 ) )
labelSlider1Value.setText(
    str(numeroPremiereDonneeCapteur+5)+" : {:6d}".format(0))
slider1Layout = QHBoxLayout()
slider1Layout.addWidget(labelSlider1Value)
slider1Layout.addWidget(slider1)


#labelSlider1Value=QLabel( )
#labelSlider1Value.setGeometry(250, 50, 50, 35)
#labelSlider1Value.setText( str( slider1.getValue() ) )
sliderLayout = QHBoxLayout()
sliderLayout.addStretch(1)
sliderLayout.addWidget(slider1)
sliderLayout.addStretch(1)
# sliderLayout.addWidget(labelSlider1Value)
# sliderLayout.addStretch(1)


slider2 = QSlider(Qt.Horizontal)
slider2.setMinimum(int(-amplitude/2))
slider2.setMaximum(int(amplitude/2))

slider2.setGeometry(10, 10, 600, 40)
slider2.valueChanged.connect(slider2ValueChanged)
slider2.setValue(0)
global labelSlider2Value
labelSlider2Value = QLabel()
labelSlider2Value.setGeometry(250, 50, 50, 35)
#labelSlider2Value.setText( "Y: "+str(0 ) )
labelSlider2Value.setText(
    str(numeroPremiereDonneeCapteur+6)+" : {:6d}".format(0))
slider2Layout = QHBoxLayout()
slider2Layout.addWidget(labelSlider2Value)
slider2Layout.addWidget(slider2)

sliderLayout.addWidget(slider2)
sliderLayout.addStretch(1)


slider3 = QSlider(Qt.Horizontal)
slider3.setMinimum(int(-amplitude/2))
slider3.setMaximum(int(amplitude/2))

slider3.setGeometry(10, 10, 600, 40)
slider3.valueChanged.connect(slider3ValueChanged)
slider3.setValue(0)
global labelSlider3Value
labelSlider3Value = QLabel()
labelSlider3Value.setGeometry(250, 50, 50, 35)
#labelSlider3Value.setText( "Y: "+str(0 ) )
labelSlider3Value.setText(
    str(numeroPremiereDonneeCapteur+7)+" : {:6d}".format(0))
slider3Layout = QHBoxLayout()
slider3Layout.addWidget(labelSlider3Value)
slider3Layout.addWidget(slider3)

sliderLayout.addWidget(slider3)
sliderLayout.addStretch(1)


slider4 = QSlider(Qt.Horizontal)
slider4.setMinimum(int(-amplitude/2))
slider4.setMaximum(int(amplitude/2))

slider4.setGeometry(10, 10, 600, 40)
slider4.valueChanged.connect(slider4ValueChanged)
slider4.setValue(0)
global labelSlider4Value
labelSlider4Value = QLabel()
labelSlider4Value.setGeometry(250, 50, 50, 35)
#labelSlider2Value.setText( "Y: "+str(0 ) )
labelSlider4Value.setText(
    str(numeroPremiereDonneeCapteur+8)+" : {:6d}".format(0))
slider4Layout = QHBoxLayout()
slider4Layout.addWidget(labelSlider4Value)
slider4Layout.addWidget(slider4)

sliderLayout.addWidget(slider4)
sliderLayout.addStretch(1)

mainLayout = QVBoxLayout()
mainLayout.addLayout(buttonLayout)
mainLayout.addLayout(button1Layout)
mainLayout.addLayout(slider1Layout)
mainLayout.addLayout(slider2Layout)
mainLayout.addLayout(slider3Layout)
mainLayout.addLayout(slider4Layout)

mainLayout.addWidget(statusLabel)
w.setLayout(mainLayout)
chaine = '@BVDP2022: Port Em '+str(portOut) + ' vers IP: '+str(destIP)
print(chaine)
w.setWindowTitle(chaine)

# timer adapted from example 1 of https://www.programcreek.com/python/example/52106/PyQt4.QtCore.QTimer
timer = QtCore.QTimer()
#app.connect(timer,  QtCore.SIGNAL('timeout()'), timerUpdate)
timer.timeout.connect(timerUpdate)
timer.setInterval(100)
timer.start()

w.setGeometry(posx, posy, sizex, sizey)
# donne le focus au bouton 1
led0Button.setDefault(True)

w.show()
app.exec_()
