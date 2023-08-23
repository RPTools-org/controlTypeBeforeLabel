# -*- coding: utf-8 -*-
# from __future__ import unicode_literals # To ensure coding compatibility with python 2 and 3.
import os.path
import sys
import wx
import gui
import gui.guiHelper
import globalVars
import config
import addonHandler
ADDON_SUMMARY = addonHandler.getCodeAddon ().manifest["summary"]
# from copy import deepcopy
from tones import beep
addonHandler.initTranslation()

class ControlTypeBeforeLabelSettingsPanel(gui.SettingsPanel):
	# Translators: name of the dialog.
	title = ADDON_SUMMARY 
	ANNOUNCE_FORMATS = (
		("0", _("Default")),
		("rsc",
		# Translators: control Type  and state before label announcement  
		_("Role State Label")),
		("sc", _("State Label")),
	)


	def __init__(self, parent):
		super(ControlTypeBeforeLabelSettingsPanel, self).__init__(parent)

	def makeSettings(self, sizer):
		helper = gui.guiHelper.BoxSizerHelper(self, sizer=sizer)
		lbl =  _("&Say control role and state label by changing their name (better for Braille)")
		self.sayByNameChangeChk = helper.addItem(wx.CheckBox(self, label=lbl))
		curVal = config.conf['controlTypeBeforeLabel']['sayByNameChange'] 
		self.sayByNameChangeChk.SetValue(curVal)

		# Translators: Help message for a dialog.
		helpLabel = wx.StaticText(self, label=_("Select the format of the controls below :"))
		sizer.Add(helpLabel)

		# checkboxes and radio controls
		announceFormatChoices = [name for format, name in self.ANNOUNCE_FORMATS]
		# print("announceFormatChoices : " + str(announceFormatChoices))
		lbl = _("&Checkboxes and radio buttons :")
		self.checkRadioChoice = helper.addLabeledControl(lbl, wx.Choice, choices=announceFormatChoices)
		self.preselecChoice(self.checkRadioChoice, "fmtCheckRadio")

		lbl = _("Check and radio &Menu items")
		self.menuItemChoice = helper.addLabeledControl(lbl, wx.Choice, choices=announceFormatChoices)
		self.preselecChoice(self.menuItemChoice, "fmtMenuItem")

	def postInit (self):
		self.sayByNameChangeChk.SetFocus ()

	def preselecChoice(self, odropDownList, confKey) :
		# try :
			# curFormat = config.conf['controlTypeBeforeLabel'][confKey]
		# except :
			# odropDownList.SetSelection(1) # rsc
			# return
		curFormat = config.conf['controlTypeBeforeLabel'][confKey]
		# print("curFormat :  " + curFormat)
		for index, (fmt, name) in enumerate(self.ANNOUNCE_FORMATS):
			# print("i : {}, fmt : {}".format(index, fmt))
			if fmt == curFormat:
				# print("found i : {}, fmt : {}".format(index, fmt))
				odropDownList.SetSelection(index)
				break	

	def thisTest(self) :
		opt1 = config.conf['controlTypeBeforeLabel']['sayByNameChange'] 
		opt2 = config.conf['controlTypeBeforeLabel']['fmtCheckRadio'] 
		opt3 = config.conf['controlTypeBeforeLabel']['fmtMenuItem'] 
		print("thisTest : byNameChange ({}) fmtCheckRadio ({}) fmtMenuItem ({})".format(opt1, opt2, opt3))

	def onSave(self):
		# Update Configuration
		config.conf['controlTypeBeforeLabel']['sayByNameChange'] = self.sayByNameChangeChk.GetValue()
		
		announceFormat = self.ANNOUNCE_FORMATS[self.checkRadioChoice.GetSelection()][0]
		config.conf["controlTypeBeforeLabel"]["fmtCheckRadio"] = announceFormat

		announceFormat = self.ANNOUNCE_FORMATS[self.menuItemChoice.GetSelection()][0]
		config.conf["controlTypeBeforeLabel"]["fmtMenuItem"] = announceFormat
