# -*- coding: utf-8 -*-
# globalPlugins/controlTypeBeforeLabel/__init__.py

import controlTypes
# controlTypes module compatibility with old versions of NVDA
if not hasattr(controlTypes, "Role"):
    setattr(controlTypes, "Role", type('Enum', (), dict(
        [(x.split("ROLE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("ROLE_")])))
    setattr(controlTypes, "State", type('Enum', (), dict(
        [(x.split("STATE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("STATE_")])))
    setattr(controlTypes, "role", type("role", (), {"_roleLabels": controlTypes.roleLabels}))
# End of compatibility fixes
import globalPluginHandler
import addonHandler
import scriptHandler
# We initialize translation support
addonHandler.initTranslation()
import api
import ui
import speech
import wx
# from time import time
# import winUser
# from winUser import getKeyNameText
from tones import beep
import os
import config
# ,sys
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
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        if hasattr(gui, "NVDASettingsDialog"):
            from gui import NVDASettingsDialog
            NVDASettingsDialog.categoryClasses.append(ctblSettings.ControlTypeBeforeLabelSettingsPanel)
        self.lblChecked = controlTypes.State.CHECKED.displayString  # _("checked")
        self.lblNotChecked = controlTypes.State.CHECKED.negativeDisplayString  # _("not checked")
        self.lblHalfChecked = controlTypes.State.HALFCHECKED.displayString
        # self.lblMenuNotChecked = " "
        self.lblUnavail = controlTypes.State.UNAVAILABLE.displayString  # _("unavailable")

        self.lblCheckbox = controlTypes.Role.CHECKBOX.displayString  # _("radio")
        self.lblRadioBtn = controlTypes.Role.RADIOBUTTON.displayString  # _("radio")
        self.lblRadioMenu = controlTypes.Role.RADIOMENUITEM.displayString  # _("radio")
        self.lblShortcutSep = ", "
        self.loadConfig()
        # super (GlobalPlugin, self).__init__(*args, **kwargs)
        hTaskBar = ctypes.windll.user32.FindWindowExA(None, None, b"Shell_TrayWnd", None)
        if not hTaskBar or globalVars.appArgs.launcher:
            return
        # beep(440, 40)

        if notifCtbl.checkNotif():
            beep(440, 30)
            wx.CallLater(200, notifCtbl.showNotif)

    def loadConfig(self):
        curAddon = addonHandler.getCodeAddon()
        iniFile = api.config.getUserDefaultConfigPath() + "\\" + curAddon.name + "-1.ini"
        oCfg = ConfigObj(iniFile, encoding="UTF-8")
        sect = "Labels"
        if sect not in oCfg:
            oCfg.update({sect: {}})
        section = oCfg[sect]

        if not os.path.exists(iniFile):
            # section.update({"remark": _("In this ini file, change only the values after the equal symbols")})
            section.update({"Checked": self.lblChecked})
            section.update({"NotChecked": self.lblNotChecked})
            section.update({"HalfChecked": self.lblHalfChecked})

            section.update({"CheckBox": self.lblCheckbox})
            section.update({"RadioBtn": self.lblRadioBtn})
            section.update({"RadioMenu": self.lblRadioMenu})
            section.update({"Unavailable": self.lblUnavail})
            section.update({"ShortcutSepar": self.lblShortcutSep})
            oCfg.comments['Labels'] = [
                _("Attention : Change only the values after the equal symbols"),
                _("Then save and restart NVDA.")
            ]
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

    def event_gainFocus(self, obj, nextHandler):
        # Get original name and role
        original_name = obj.name
        role = obj.role
        states = obj.states
        
        # Initialize variables
        tRole = ""
        tState = ""
        fmt = "0"
        
        # Determine which format to use based on control type
        if role == controlTypes.Role.CHECKBOX:
            fmt = config.conf["controlTypeBeforeLabel"]["fmtCheckRadio"]
            if fmt != "0":
                tRole = self.lblCheckbox
                tState = (self.lblChecked if controlTypes.State.CHECKED in states else self.lblNotChecked)
                tState = (self.lblHalfChecked if controlTypes.State.HALFCHECKED in states else tState)
        elif role == controlTypes.Role.RADIOBUTTON:
            fmt = config.conf["controlTypeBeforeLabel"]["fmtCheckRadio"]
            if fmt != "0":
                tRole = self.lblRadioBtn
                tState = (self.lblChecked if controlTypes.State.CHECKED in states else self.lblNotChecked)
        elif role == controlTypes.Role.MENUITEM:
            if controlTypes.State.CHECKED in states:
                fmt = config.conf["controlTypeBeforeLabel"]["fmtCheckRadio"]
                if fmt != "0":
                    tRole = ""
                    tState = self.lblChecked
        elif role == controlTypes.Role.CHECKMENUITEM:
            fmt = config.conf["controlTypeBeforeLabel"]["fmtMenuItem"]
            if fmt != "0":
                tRole = ""
                tState = (self.lblChecked if controlTypes.State.CHECKED in states else self.lblNotChecked)
        elif role == controlTypes.Role.RADIOMENUITEM:
            fmt = config.conf["controlTypeBeforeLabel"]["fmtMenuItem"]
            if fmt != "0":
                tRole = self.lblRadioMenu
                tState = (self.lblChecked if controlTypes.State.CHECKED in states else self.lblNotChecked)

        # If format is "0" (default), let NVDA handle it normally
        if fmt == "0":
            return nextHandler()
            
        # Add unavailable state if applicable
        if controlTypes.State.UNAVAILABLE in states:
            tState = self.lblUnavail + tState

        # Get the clean name (without any existing state/role information)
        # We need to handle the fact that NVDA might have already added state/role
        # The original name might be something like "Rate boost, Alt+t"
        # But after NVDA processes it, it becomes "Rate boost, Alt+t, check box not checked"
        # We need to extract just the main label
        
        # First, split by double space which NVDA uses to separate label from role/state
        parts = original_name.split('  ')
        main_label = parts[0].strip() if parts else original_name
        
        # Now clean any trailing commas or spaces
        main_label = main_label.rstrip(', ')
        
        # Remove any keyboard shortcut from main_label if it's at the end
        if obj.keyboardShortcut:
            shortcut_str = str(obj.keyboardShortcut)
            # Check if shortcut is at the end of main_label
            if main_label.endswith(', ' + shortcut_str):
                main_label = main_label[:-len(', ' + shortcut_str)]
            elif main_label.endswith(self.lblShortcutSep + shortcut_str):
                main_label = main_label[:-len(self.lblShortcutSep + shortcut_str)]
            elif main_label.endswith(shortcut_str):
                main_label = main_label[:-len(shortcut_str)].rstrip(', ')
        
        # Now we have the clean label
        display_name = main_label
        
        # Build the final announcement
        if fmt == "rsc":
            # Role State Label format
            t = tRole + tState + display_name
        elif fmt == "sc":
            # State Label format (what the user wants)
            t = tState + display_name
        else:
            # Should not happen, but fallback
            t = display_name
        
        # Add keyboard shortcut if present and not already in the name
        if obj.keyboardShortcut:
            shortcut_str = str(obj.keyboardShortcut)
            # Only add if not already at the end
            if not t.endswith(shortcut_str):
                t += self.lblShortcutSep + shortcut_str
        
        # Apply the change
        if config.conf["controlTypeBeforeLabel"]["sayByNameChange"]:
            obj.name = t
        
        # Speak the modified text
        wx.CallAfter(sayElement, t)
        
        # IMPORTANT: Don't call nextHandler to prevent NVDA's default announcement
        # which would cause duplication
        return

    @scriptHandler.script(gesture="kb:windows+$", description=_("display settings dialog for the current profile"),
                          category=ctblSettings.ADDON_SUMMARY)
    def script_showSettings(self, gesture):
        wx.CallAfter(gui.mainFrame._popupSettingsDialog, gui.settingsDialogs.NVDASettingsDialog,
                     ctblSettings.ControlTypeBeforeLabelSettingsPanel)

    @scriptHandler.script(gesture="kb:shift+windows+$", description=_("Edit ini file of states and roles labels"),
                          category=ctblSettings.ADDON_SUMMARY)
    def script_editIniFile(self, gesture):
        curAddon = addonHandler.getCodeAddon()
        iniFile = api.config.getUserDefaultConfigPath() + "\\" + curAddon.name + "-1.ini"
        # avoid NVDA's bug in Windows 11
        startProgramMaximized(r"C:\Windows\notepad.exe", iniFile)


def sayElement(text):
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
