# -*- coding: utf-8 -*-
# globalPlugins/controlTypeBeforeLabel

import controlTypes
# controlTypes module compatibility with old versions of NVDA
if not hasattr(controlTypes, "Role"):
	setattr(controlTypes, "Role", type('Enum', (), dict(
	[(x.split("ROLE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("ROLE_")])))
	setattr(controlTypes, "State", type('Enum', (), dict(
	[(x.split("STATE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("STATE_")])))
	setattr(controlTypes, "role", type("role", (), {"_roleLabels": controlTypes.roleLabels}))
# End of compatibility fixes
import globalPluginHandler, addonHandler, scriptHandler
# from scriptHandler import getLastScriptRepeatCount
# We initialize translation support
addonHandler.initTranslation ()
import api
import ui
import speech
import wx
# from time import time
# import winUser
# from winUser import getKeyNameText 
from tones import beep
import os, config # ,sys
import ctypes
from configobj import ConfigObj
import globalVars
import gui
from .shared import controlTypeBeforeLabelSettings as ctblSettings, notifCtbl

confspec = {
"sayByNameChange": "boolean(default=True)",
"fmtCheckRadio": "string(default=rsc)",
"fmtMenuItem": "string(default=rsc)",
}
config.conf.spec["controlTypeBeforeLabel"] = confspec

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super (GlobalPlugin, self).__init__(*args, **kwargs)
		if hasattr (gui, "NVDASettingsDialog"):
			from gui import NVDASettingsDialog
			NVDASettingsDialog.categoryClasses.append(ctblSettings.ControlTypeBeforeLabelSettingsPanel)
		self.lblChecked = controlTypes.State.CHECKED.displayString # _("checked")
		self.lblNotChecked = controlTypes.State.CHECKED.negativeDisplayString # _("not checked")
		self.lblHalfChecked = controlTypes.State.HALFCHECKED.displayString
		# self.lblMenuNotChecked = " "
		self.lblUnavail = controlTypes.State.UNAVAILABLE.displayString  # _("unavailable")
		
		self.lblCheckbox = controlTypes.Role.CHECKBOX.displayString # _("radio")
		self.lblRadioBtn = controlTypes.Role.RADIOBUTTON.displayString # _("radio")
		self.lblRadioMenu = controlTypes.Role.RADIOMENUITEM.displayString # _("radio")
		self.lblShortcutSep = ", "
		self.loadConfig()
		# super (GlobalPlugin, self).__init__(*args, **kwargs)
		hTaskBar = ctypes.windll.user32.FindWindowExA(None, None, b"Shell_TrayWnd", None)
		if not hTaskBar or  globalVars.appArgs.launcher : 
			return
		# beep(440, 40)

		if notifCtbl.checkNotif() :
			beep(440, 30)
			wx.CallLater(200, notifCtbl.showNotif)

	def loadConfig(self) :
		curAddon=addonHandler.getCodeAddon()
		iniFile = api.config.getUserDefaultConfigPath()+"\\" + curAddon.name + "-1.ini"
		oCfg = ConfigObj(iniFile, encoding="UTF-8")
		sect = "Labels"
		if sect not in oCfg : oCfg.update({sect:{}})
		section = oCfg[sect]

		if  not os.path.exists(iniFile) :
			# section.update({"remark": _("In this ini file, change only the values after the equal symbols")})
			section.update({"Checked": self.lblChecked})
			section.update({"NotChecked": self.lblNotChecked})
			section.update({"HalfChecked": self.lblHalfChecked})

			section.update({"CheckBox": self.lblCheckbox})			
			section.update({"RadioBtn": self.lblRadioBtn})			
			section.update({"RadioMenu": self.lblRadioMenu})			
			section.update({"Unavailable": self.lblUnavail})			
			section.update({"ShortcutSepar": self.lblShortcutSep})
			oCfg.comments['Labels'] = [_("Attention : Change only the values after the equal symbols"), _("Then save and restart NVDA.")]
			oCfg.write()
		# init
		self.lblChecked = section["Checked"] + " "
		self.lblNotChecked = section["NotChecked"] + " "
		self.lblHalfChecked = section["HalfChecked"] + " "
		
		self.lblCheckbox = section["CheckBox"] + " "
		self.lblRadioBtn = section["RadioBtn"] + " "
		self.lblRadioMenu = section["RadioMenu"] + " "
		self.lblUnavail = section["Unavailable"] + " "
		self.lblShortcutSep = section["ShortcutSepar"]

	def event_gainFocus (self,obj,nextHandler):
		# return nextHandler()
		role, states, fmt = obj.role, obj.states, "0"
		if role   == controlTypes.Role.CHECKBOX :
			fmt = config.conf["controlTypeBeforeLabel"]["fmtCheckRadio"]
			if fmt != "0" :
				tRole = self.lblCheckbox
				tState = (self.lblChecked if controlTypes.State.CHECKED in states else self.lblNotChecked)
				tState = (self.lblHalfChecked if controlTypes.State.HALFCHECKED in states else tState)
		if role  == controlTypes.Role.RADIOBUTTON :
			fmt = config.conf["controlTypeBeforeLabel"]["fmtCheckRadio"]
			if fmt != "0" :
				tRole = self.lblRadioBtn
				tState = (self.lblChecked if controlTypes.State.CHECKED in states else self.lblNotChecked)
		elif role == controlTypes.Role.MENUITEM :
			if controlTypes.State.CHECKED in states : 
				fmt = config.conf["controlTypeBeforeLabel"]["fmtCheckRadio"]
				if fmt != "0" :
					tRole = ""
					tState = self.lblChecked
		elif role == controlTypes.Role.CHECKMENUITEM :
			fmt = config.conf["controlTypeBeforeLabel"]["fmtMenuItem"]
			if fmt != "0" :
				tRole = ""
				tState = (self.lblChecked if controlTypes.State.CHECKED in states else self.lblNotChecked)
		elif role == controlTypes.Role.RADIOMENUITEM :
			fmt = config.conf["controlTypeBeforeLabel"]["fmtMenuItem"]
			if fmt != "0" :
				tRole = self.lblRadioMenu
				tState = (self.lblChecked if controlTypes.State.CHECKED in states else self.lblNotChecked)

		if  fmt == "0" :
			return nextHandler()
		if controlTypes.State.UNAVAILABLE in states :
			tRole = self.lblUnavail +  str(tRole)


		if fmt == "rsc" :
			t = tRole + tState + str(obj.name) + ("" if obj.keyboardShortcut is None  else self.lblShortcutSep + str(obj.keyboardShortcut)) + ", "
		elif fmt == "sc" :
			t = tState + str(obj.name) + ("" if obj.keyboardShortcut is None  else self.lblShortcutSep + str(obj.keyboardShortcut)) + ", "

		if config.conf["controlTypeBeforeLabel"]["sayByNameChange"] :
			obj.name = t
		else :
			wx.CallAfter(sayElement, t)
		nextHandler()
		
	@scriptHandler.script(gesture="kb:windows+$", description=_("display settings dialog for the current profile"), category=ctblSettings.ADDON_SUMMARY)
	def script_showSettings(self, gesture):
		wx.CallAfter(gui.mainFrame._popupSettingsDialog, gui.settingsDialogs.NVDASettingsDialog, ctblSettings.controlTypeBeforeLabelSettingsPanel)

	@scriptHandler.script(gesture="kb:shift+windows+$", description=_("Edit ini file of states and roles labels"), category=ctblSettings.ADDON_SUMMARY)
	def script_editIniFile(self, gesture):
		curAddon=addonHandler.getCodeAddon()
		iniFile = api.config.getUserDefaultConfigPath()+"\\" + curAddon.name + "-1.ini"
		# avoid NVDA's bug in Windows 11
		startProgramMaximized (r"C:\Windows\notepad.exe", iniFile)

def sayElement(text) :
		speech.cancelSpeech()
		speech.speakText(text)

def startProgramMaximized(exePath, exeParams=""):
	import subprocess
	SW_MAXIMIZE = 3
	info = subprocess.STARTUPINFO()
	info.dwFlags = subprocess.STARTF_USESHOWWINDOW
	info.wShowWindow = SW_MAXIMIZE
	if exeParams != "":
		exePath += " " + exeParams 
	subprocess.Popen(exePath, startupinfo=info)
