# -*- coding: iso8859-15 -*-
# VeritableRadioReveil.py Created by @Knarou on December 2013 - fabrice.mounin@gmail.com
# You are free to add, modify, delete, burn, eat this code ;-) 
# Feel free to contact me if you want to 
# Ce code est sans aucune pr�tention, il � �t� fait par rapport � un projet personnel en mode prototype
# Si vous avez mal � la t�te en lisant ce code, c'est normal, je vous conseille : 
# - de boire un coup 
# - de m'aider � reecrire ce code
# - de l'essayer en croisant les doigts pour que cela marche
# ;-)
# VeritableRadioReveil.py Created by @Knarou on December 2013 - fabrice.mounin@gmail.com
# 


# Gaugette import Rotary + switch + tout petit petit ecran lcd ;-)
import gaugette.rotary_encoder
import gaugette.switch
import time
from subprocess import call
import subprocess
import alsaaudio, sys, os
import gaugette.ssd1306

# GPIO utilis� pour le lcd
RESET_PIN = 15
DC_PIN    = 16

led = gaugette.ssd1306.SSD1306(reset_pin=RESET_PIN, dc_pin=DC_PIN)
led.begin()
led.clear_display()

# Trouver le mixer et utilise le 1er.
try :
    mixer = alsaaudio.Mixer('PCM', 0)
except alsaaudio.ALSAAudioError :
    sys.stderr.write("No such mixer\n")
    sys.exit(1)
# pour afficher la date en FR
dic_jour={'Mon':'Lundi','Tue':'Mardi','Wed':'Mercredi','Thu':'Jeudi','Fri':'Vendredi','Sat':'Samedi','Sun':'Dimanche'}
dic_mois={'Jan':'Janvier','Feb':'Fevrier','Mar':'Mars','Apr':'Avril','May':'Mai','Jun':'Juin','Jul':'Juillet','Aug':'Aout','Sep':'Septembre','Oct':'Octobre','Nov':'Novembre','Dec':'Decembre'}

# GPIO utilis� pour le rotary encoder+switch
A_PIN  = 7
B_PIN  = 1 
SW_PIN = 3
# Variable globale
global listeRadio
global statusRadio
global radioTitre
global wifi
global snooze
global timerRadio
global timerAlarm
global alarmeActive
global choixMenu
global sr
global etat
global alarm_snooze
global timer

listeRadio = []
statusRadio=0
radioTitre=1
wifi=1
snooze=0
timerRadio=0
timerAlarm=0
alarmeActive=0
choixMenu=0
etat=1
# valplus = volume son
valplus=30
io=0.01
timeok=time.time()
# sr position menu en memoire
sr=0
alarm_snooze=""
timer=""

# liste des radio enregistr� avec MPC
listeRadio.append("ShoutCast")
listeRadio.append("Fip")
listeRadio.append("Nova")
listeRadio.append("Classique")
listeRadio.append("France INTER")
listeRadio.append("RTL")

ALARM="00:00"
ALARMCHOIX=ALARM
ALARMDUR="00:00"

#ici Rotary Encoder
encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
encoder.start()
switch = gaugette.switch.Switch(SW_PIN)
last_state = None
# Stop Radio
call(["mpc", "stop"])


def get_time():
	d=time.asctime()
	d=d.split()
	date=dic_jour[d[0]]+" "+d[2]+" "+dic_mois[d[1]]+" "+d[4]
	heure=d[3]
	heure=heure.split(":")
	heure=heure[0]+":"+heure[1]
	return date,heure

def volume(deltak):
	global valplus
	os.system('clear')
	if deltak > 0: valplus=valplus+1
	else: valplus=valplus-1
	if valplus>=100: valplus=100
	call(["mpc", "volume", str(valplus)])	
	led.draw_text2(0,24,"Volume :" + str(valplus) +" % ",1)
	led.display()	
	
def radioplay(val):
	global wifi
	global statusRadio
	global radioTitre
	global snooze
	global ALARM
	global ALARMDUR
	if val > len(listeRadio): 
		call(["mpc", "stop"])
		snooze=0
		statusRadio=0
		ALARM=ALARMDUR
	else: 
		radioTitre=val
		if wifi==0:
			led.clear_display()
			led.draw_text2(0,24,"Wifi Activation",1)
			led.display()
			call(["ifup", "wlan0"])
			time.sleep(15)
			led.clear_display()
			led.draw_text2(0,24,"Wifi Actif",1)
			led.display()
			wifi=1
		call(["mpc", "play", str(radioTitre)])
		statusRadio=1

def rotarychoix(menu,choix):
	global sr
	if choix > 0:
		if sr==len(menu)-1: sr=len(menu)-1
		else: sr=sr+1
	elif choix < 0:
		if sr==0: sr=0
		else: sr=sr-1
	a=(sr*10)*-1
	led.clear_display()
	for i in menu:
		if menu[sr]==i: led.draw_text2(0,a,">" + str(i[:35].rstrip('\n\r')),1,0)
		else: led.draw_text2(0,a," " + str(i[:35].rstrip('\n\r')),1,0) 
		a=a+10
	led.display()

def menuGeneral(choix):
	menu = []
	menu.append("REGLAGES")
	menu.append("RADIO")
	menu.append("STOP RADIO")
	menu.append("TIMER 30Min")
	menu.append("RETOUR")
	rotarychoix(menu,choix)

def menuReglage(choix):
	menu = []
	menu.append("REVEIL :" + ALARM)
	if alarmeActive==1: menu.append("ALARME OFF")
	else: menu.append("ALARME ON")
	menu.append("RETOUR")
	menu.append("ETEINDRE")
	rotarychoix(menu,choix)

def menuRadio(choix):
	global listeRadio
	rotarychoix(listeRadio,choix)

def clock():
	if alarmeActive==1: plus=" �"
	else: plus=""
	led.clear_display()
	led.draw_text2(0,0,time.strftime("%H:%M:%S", time.localtime()) + plus,2,2)
	if wifi==0: led.draw_text2(0,24,"Wifi Inactif",1)
	if statusRadio==1: led.draw_text2(0,24,listeRadio[radioTitre-1]+" "+timer,1)
	led.display()

def clockAlarm():
	#affiche l'heure quand alarm regl�
	led.clear_display()
	led.draw_text2(0,0,time.strftime("%H:%M:%S", time.localtime()),2,2)
	led.display()
	led.draw_text2(0,18,ALARM,1,0)
	led.display()
	time.sleep(1)
# vous connaissez le snooze ;-) c'est celui qui vous permet de dormir 10 minutes de plus ;-)
def snoozeit():
	global ALARM
	global snooze
	global statusRadio
	global alarm_snooze
	plus=0
	alarm_snooze=get_time()
	alarm_snooze=(alarm_snooze[1])
	h=alarm_snooze.split(":")
	varsnooze=10
	if (int(h[1])+varsnooze)>59: 
		newM=(int(h[1])+varsnooze)-60
		plus=1
	else: newM=(int(h[1])+varsnooze)
	if len(str(newM))<2: 
		newM=str('0')+str(newM)
	if len(str(int(h[0])+plus))<2: newH=str('0')+str(int(h[0])+plus)
	else: newH=str(int(h[0])+plus)
	alarm_snooze=str(newH)+":"+str(newM)
	#snooze=0
	call(["mpc", "stop"])
	statusRadio=0
	led.clear_display()
	led.draw_text2(0,0,time.strftime("%H:%M:%S", time.localtime()),2,0)
	led.draw_text2(0,24,"Dodo pour "+str(alarm_snooze),1)
	led.display()
	time.sleep(0.5)

def timerRadio(varsnooze=30):
	global timer
	plus=0
	timer=get_time()
	timer=(timer[1])
	h=timer.split(":")
	#varsnooze=30
	if (int(h[1])+varsnooze)>59: 
		newM=(int(h[1])+varsnooze)-60
		plus=1
	else: newM=(int(h[1])+varsnooze)
	if len(str(newM))<2: 
		newM=str('0')+str(newM)
	if len(str(int(h[0])+plus))<2: newH=str('0')+str(int(h[0])+plus)
	else: newH=str(int(h[0])+plus)
	timer=str(newH)+":"+str(newM)
	
def alarm(deltak,type):
	global etat
	global ALARM
	global ALARMDUR
	global INFOAL
	global ALARMCHOIX
	os.system('clear')
	h=ALARM.split(":")
	if len(str(int(h[0])))<2: res=str('0')+str(int(h[0]))
	else: res=str(int(h[0]))
	ALARMCHOIX=str(int(h[0]))+str(int(h[1]))
	if type=='heure':
		if deltak > 0:
			if len(str(int(h[0])+1))<2: res=str('0')+str(int(h[0])+1)
			else: res=str(int(h[0])+1)
			if str(res)=="24": res="00"
			ALARM=str(res)+":"+str(h[1])
		elif deltak < 0:
			if len(str(int(h[0])-1))<2: res=str('0')+str(int(h[0])-1)
			else: res=str(int(h[0])-1)
			if str(res)=="-1" or str(res)=="-1": res="23"
			ALARM=str(res)+":"+str(h[1])
		ALARMCHOIX=">"+str(res)+":"+str(h[1])
	if type=='minute':
		if len(str(int(h[1])))<2: res=str('0')+str(int(h[1]))
		else: res=str(int(h[1]))
		if deltak > 0:
			if len(str(int(h[1])+1))<2: res=str('0')+str(int(h[1])+1)
			else: res=str(int(h[1])+1)
			if str(res)=="60": res="00"
			ALARM=str(h[0])+":"+str(res)	
		elif deltak < 0:
			if len(str(int(h[1])-1))<2: res=str('0')+str(int(h[1])-1)
			else: res=str(int(h[1])-1)
			if str(res)=="-1": res="59"
			ALARM=str(h[0])+":"+str(res)
		ALARMCHOIX=str(h[0])+":>"+str(res)
	ALARMDUR=ALARM
	led.clear_display()
	led.draw_text2(0,0,time.strftime("%H:%M:%S", time.localtime()),2,0)
	led.draw_text2(0,18,ALARMCHOIX,2,0)
	led.display()
#click est celui qu'on appelle quand on tourne le bouton
def rotation(etat):
	global io
	global timeok
	global wifi
	global statusRadio
	global radioTitre
	global snooze
	delta = encoder.get_delta()
	if delta!=0:
		#io=0.01
		timeok=time.time()
		if delta >= 0: deltak=1
		else: deltak=-1
		if etat==1 or etat==5:
			io=0.01
			volume(deltak)
		elif etat==30:
			io=0.2
			menuRadio(deltak)		
		elif etat==20:
			io=0.2
			menuReglage(deltak)
		elif etat==11:
			io=0.2
			menuGeneral(deltak)
		elif etat==2:
			io=0.2

