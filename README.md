# Documentation

### Overview

Leave this script running to have your own personal SNES Classic availability checker. Only supports gmail right now, but you can easily edit a few lines to make it work with other services.

The script may have a high false positive rate (false alert), since I don't exactly know how the HTML pages will look when the SNESC goes in-stock, but is tuned to ensure zero false negatives (missing the alert when it goes in-stock).

I'll be adding more supported websites as they post their SNESC links, but you can easily add more yourself. Just add the website, its SNESC link, and some HTML code you think is likely to disappear when it goes in-stock.

### Supported Platforms

Runs on anything that can run Python3.

# How to Use

### Dependencies

* [Python3](https://www.python.org/downloads/)
* [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/install.html)

### Install

1. Python3 and pip3 (to help install Python libraries): `sudo apt-get install python3 python3-pip`
	1. Depending on your PC's operating system, PyAutoGUI has some dependencies: 
		1. On OSX, install Quartz: `sudo pip3 install pyobjc-framework-Quartz`
		1. On Linux, install Xlib and Tkinter: `sudo apt-get install python3-xlib python3-tk`
	1. PyAutoGUI: `sudo pip3 install pyautogui`

### Running

1. Run the script
1. Enter your SEND email: I use a low security gmail address because I don't want to mess with two-factor auth or app-specific passwords. Your input will be cached/pickled for future runs of the script.
1. Enter your SEND email password. This is not stored anywhere and you need to enter it each time you run the script.
1. Enter your RECEIVE email: I use my main, secure email for this, since no password is needed. This will be cached/pickled. Note that you can use the same email for both SEND and RECEIVE if you want.

# License
See [here](./LICENSE).