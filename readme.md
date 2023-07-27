# Say control type befor label

Note: this page has been translated from French to English by Google Translate.

* Author: Pierre-Louis Renaud;
* URL: [Contact in French and English](https://www.rptools.org/NVDA-Thunderbird/toContact.html) ;
<!-- * Download the [stable version][1] ; -->
* Download the [Latest version on RPTools.org](https://www.rptools.org/?p=9200) ;
* NVDA Compatibility: 2019.3 and above;
<!-- * [Source code on GitHub][2] ; --> 

## Presentation
This flexible add-on allows NVDA to announce the type and state of GUI controls before their label.

For example, we will hear Checkbox checked before its label, which can be long.
In dialogs with lots of checkboxes or radio buttons, this can greatly improve the efficiency of checking options or settings;

In addition, the labels of controls types and states can be shortened. For "checkboxes", you can indicate "box", you will then hear: box checked.

At this time, the add-on only supports checkboxes, radio buttons, checkable and radio menu items.
Other types of controls  could be added later.

In addition, you can decide to use this add-on with settings specific to each application profile via its settings dialog.

Here is an example:

checkbox checked, Say the text of the control by modifying their name (better for Braille), Alt+n,

Select the ad format from the items below:

Check Boxes and Radio Buttons: Collapsed Label State Type drop-down list Alt+c

Check and radio menus: drop-down list Type status reduced label Alt+m

OK Cancel

Each drop-down list contains the following options:

* Default: the add-on does not change  the announcement for this type of control and in the current configuration profile;
* Type State label : for example Checkbox checked Save configuration on exit, Alt+s;
* State label : example: checked Save configuration on exit, Alt+s;

## Keyboard shortcuts

These shortcuts, which can be modified via the Input gestures dialog, allow you to adjust the add-on to your best convenience.

* Windows+$: displays the configuration dialog for the active profile.
  This allows settings specific to each application. So be sure to first create a configuration profile for the application where you want the add-on to intervene. ;
* Shift+Windows+$ : to customize the labels of states and control  types via notepad.
  After installing controlTypeBeforeLabel, the add-on retrieves your system's standard labels and saves them directly to the ini file.
  After sabving this file, you must restart NVDA or reload the add-ons.
  To reset these labels to their original values, you can delete this ini file and then relaunch NVDA. It will be recreated automatically.
  This settings file is common to all configuration profiles;

<!-- links section -->

[1]: https://github.com/RPTools-org/controlTypeBeforeLabel/releases/download/v2023.07.27/controlTypeBeforeLabel-2023.07.27.nvda-addon

[2]: https://github.com/RPTools-org/controlTypeBeforeLabel/
