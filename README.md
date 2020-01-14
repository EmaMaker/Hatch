# What is this?
This is a universal account checker, bruteforce tool, based on Metachar's Hatch ( https://github.com/metachar/Hatch ) by nsgodshall ( https://github.com/nsgodshall/Hatch )

<br>
Options:
  -h, --help            show this help message and exit <br>
  -u USERNAME, --username=USERNAME 
                        Choose the username  <br>
  --usernamesel=USERNAMESEL
                        Choose the username selector <br>
  --passsel=PASSSEL     Choose the password selector <br>
  --loginsel=LOGINSEL   Choose the login button selector <br>
  --passlist=PASSLIST   Enter the password list directory <br>
  --website=WEBSITE     Choose a website <br>
  --usecombo=USECOMBO   Choose wether use a combo list or a single username <br>
                        with password list. Combo lists must be in 
                        username:password format <br>
  --combolist=COMBOLIST
                        Pass a whole combolist file <br>
  --workers=WORKERS     Spawn # concurrent workers <br>
  --succfile=SUCCFILE   file used to store successfully forced accounts <br>

## Installation Instructions
```
git clone https://github.com/EmaMaker/AccountChecker
python2 ao/account_checker.py
```

## Requirements
```
pip2 install selenium
pip2 install requests
```
Chrome and chromedriver are required

You can download chromedriver here: http://chromedriver.chromium.org/downloads
for this fork, create a folder in your C drive called 'webdrivers' and place the executable file inside. If you want to use a different directory, simply change the CHROME_DVR_DIR variable inside the python file.

<br>
## How to use (text)
1). Find a website with a login page<br>
2). Inspect element to find the Selector of the username form<br>
3). Do the same for the password field<br>
4). The login form <br>
6). Choose wether to use combo list or password list with single username
7). Provide list file and eventually the username
8). Choose number of concurrent workers

6). Watch it go!
