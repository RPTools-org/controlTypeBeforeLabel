# -*- coding: utf-8 -*-h
# for controlTypeBeforeLabel

try: 	from urllib import urlopen
except Exception: from urllib.request import urlopen
try: 	from urllib import Request
except Exception: from urllib.request import Request

import api, globalVars
import os, wx
# import  gui
from ui import  message, browseableMessage
import addonHandler
addonHandler.initTranslation()
import time, datetime, winUser
import config
from tones import beep
import pickle

def dateTS(sDateTime) :
	# example  = "2023-04-03 10:56"
	return time.mktime(datetime.datetime.strptime(sDateTime, "%Y-%m-%d %H:%M").timetuple())


# functions
def getURLHelp(url) :
	# 2022-12-20 localized
	from languageHandler import getLanguage
	lang = getLanguage()
	if "PT" not in   lang :
		lang = lang.split("_")[0]
	return url.format(lang)
	
# Variables to configure
baseUrl="https://www.rptools.org/"
urlNotif = "" 
urlFileInfos = baseUrl + "fileInfos.php?key=sbcNotif"

# Structure du fichier d'informations,  l'ordre des lignes doit être respecté
# version=2023-04-03 00:00
# name=controlTypeBeforeLabel


def checkNotif() :
	date, tsRemote = getRemoteDateTime()
	if tsRemote == 0 : return False # remote file did not exist 
	tsLocal = getLastDisplayed()
	# print("Remote date : {0}, Remote timestamp : {1}, Local ts : {2}".format(str(date), str(tsRemote), str(tsLocal)))
	if tsRemote <= tsLocal :
		return False
	setLastDisplayed(tsRemote)
	return  True

def getRemoteDateTime() :
	global urlFileInfos
	failDT = "2010-03-29 00:00"
	failTS = 0 # dateTS(failDT)
	try :
		with urlopen  (urlFileInfos) as data :
			data = data.read().decode()
	except :
		# beep(100, 40)
		return failDT, failTS
	if len(data)  < 10 : 
		#beep(100, 20)
		return failDT, failTS
	lines = data.split("\n")
	DT = lines[0].split("=")[1]
	# dt format : YYYY-MM-DD HH:MM
	# must convert v to time stamp
	try : TS = dateTS(DT)
	except : return failDT, failTS
	return DT, TS 

def showNotif() :
	from languageHandler import getLanguage
	lang = getLanguage()
	# lang = "en"
	if "fr" in lang :
		url = "https://www.rptools.org/NVDA-Thunderbird/notificationsSBC.html"
	else :
		url = "https://www-rptools-org.translate.goog/NVDA-Thunderbird/notificationsSBC.html?_x_tr_sl=fr&_x_tr_tl=@lg&_x_tr_hl=@lg&_x_tr_pto=sc"
		url = url.replace("@lg", lang)
	#  the translated content is displayeed via javascript so it cannot be displayed with ui.browseableMessage()
	os.startfile (url)

import addonHandler
import time

def getLastDisplayed() :
	lastNotifFile = api.config.getUserDefaultConfigPath()+"\\addons\\sbcLastNotif.pickle"
	# print("lastNotifFile : " + lastNotifFile)
	if  not os.path.exists(lastNotifFile) : return 1000000000.0
	if os.path.getsize(lastNotifFile) < 10 : return 1000000000.0

	try :
		with open(lastNotifFile, mode="rb") as fileObj :
			ut = (pickle.load(fileObj))
		ut = float(ut)
	except :
		ut = 1000000000.0
		pass
	#print("TB+ update Time : " + str(ut))
	return ut
	
import api
def setLastDisplayed(ts) :
	msg = ""
	lastNotifFile = api.config.getUserDefaultConfigPath()+"\\addons\\sbcLastNotif.pickle"
	# print("setLastDisplayed, lastNotifFile : " + lastNotifFile)
	# print("setLastDisplayed, ts : " + str(ts))
	try :
		with open(lastNotifFile, mode="wb") as fileObj :
			pickle.dump(ts, fileObj)  #, protocol=0
		# os.startfile(lastNotifFile)
		return True
	except :
		msg = _("Error writing file :\n") + lastNotifFile 
		pass
		
	if msg :
		from speech import  cancelSpeech
		cancelSpeech()
		wx.CallLater(1000, message, msg)
		return False

def hasToUpdate(addonName) :
	nextUpdateFile = api.config.getUserDefaultConfigPath()+"\\addons\\" +  addonName + "-nextUpdate.pickle"
	if  not os.path.exists(nextUpdateFile) : return True
	if os.path.getsize(nextUpdateFile) < 5 : return False # mise à jour désactivée

	now = time.time() 
	try :
		with open(nextUpdateFile, mode="rb") as fileObj :
			ut = (pickle.load(fileObj))
		ut = float(ut)
	except :
		ut = now - 3600
		pass
	#print("TB+ update Time : " + str(ut))
	if ut < now :
		return True
	return False

def getFileSizeFromURL(url) :
	req = Request(url, method='HEAD')
	f = urlopen(req)
	#f.status # 200
	return str(f.headers['Content-Length'])

