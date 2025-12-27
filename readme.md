# controlTypeBeforeLabel: Announce control type and state before its label

* Author: Pierre-Louis Renaud;
* URL: [Contact](https://www.rptools.org/NVDA-Thunderbird/toContact.html) ;
* This add-on can be installed from the NVDA add-on store;
* NVDA compatibility: 2019.3 to 2025.x;

## Presentation

This flexible add-on allows NVDA to announce the type and state of user interface elements before their label.

In dialogs with many check boxes or radio buttons, this can significantly improve the efficiency of checking options or settings;

In addition, the labels for element types and states can be shortened. For "check boxes", you could specify "Check", and you would then hear: "check checked".

Currently, the add-on only supports check boxes, radio buttons, checkable menu items, and radio menu items.
Other element types may be added later.

Furthermore, you can decide to use this add-on with specific settings for each application profile via its settings dialog.

Here is an example:

check box checked "Speak the text of elements by modifying their name (better suited for Braille)", Alt+n,

Select the announcement format for the elements below:

Check boxes and radio buttons: combo box "Type state label reduced" Alt+c

Check and radio menus: combo box "Type state label reduced" Alt+m

OK Cancel

Each combo box contains the following options:

* Default: the add-on does not intervene for this type of element and in the current configuration profile;
* Type state label: for example "Check box checked Save configuration on exit", Alt+s;
* State label: example: "checked Save configuration on exit", Alt+s;

## Keyboard Shortcuts

These shortcuts, which can be modified via the Input Gestures dialog, allow you to adjust the add-on to your best convenience.

* Windows+$: displays the configuration dialog for the active profile.<br>
This allows for specific settings for each application. Therefore, make sure to first create a configuration profile for the application where you want the add-on to intervene.;
* Shift+Windows+$: to customize state and element type labels via Notepad.<br>
After installing "Control type Before label", the add-on retrieves the standard labels from your system and saves them directly into the ini file. <br>
After modifying this file, you must restart NVDA or reload add-ons.<br>
To reset these labels to their original values, you can delete this ini file and then restart NVDA. It will be recreated automatically.<br>
This settings file is common to all configuration profiles;

## Change Log

### Version 2025.12.25

Fix by Chai ChaiMee, thanks to him:

The control type and state are no longer announced at the end of the label when they are announced at the beginning;

---

Souhaitez-vous que je vérifie la cohérence de la terminologie technique avec les standards de l'interface NVDA en anglais ?