# -*- coding: utf-8 -*-
 
import re
from robobrowser import RoboBrowser
import time
import sys # sys.exit() to stop the script for debugging
from unidecode import unidecode
import datetime
import os # needed to create CSV directory

# Setup
csv_directory = "../data"
csv_filename = "agentes-animacao-turistica"

# Strings to ASCII function for districts
def string_simplify(string):
  "strings to ASCII, useful for district names"
  return unidecode(string).lower().replace (" ", "_")


base_url = 'https://rnt.turismodeportugal.pt/RNAAT/ConsultaRegisto.aspx'
csv_url = 'https://rnt.turismodeportugal.pt/RNAAT/ConsultaAoRegisto.aspx' # They have 'Ao' in between the URLs



# Print information
print "Getting all the local tourism animation agencies in Portugal..."
print

 # Create CSV directory
if not os.path.exists(csv_directory):
  os.makedirs(csv_directory)



# Browse to RNT - Registo Nacional de Turismo
print "Checking website..."
browser = RoboBrowser(history=True,parser="lxml")
browser.open(base_url)


# Encrypted Outsystems variable
page_forms = browser.get_form(id='WebForm1')
OSVSTATE = page_forms['__OSVSTATE'].value

  
# AJAX data to download CSV
csv_download_data = {
  "__EVENTTARGET": "wt49",
  "__EVENTARGUMENT": "",
  "__OSVSTATE": OSVSTATE,
  "__VIEWSTATE": "",
  "wt153": "off",
  "wt19": "off",
  "wt158": "off",
  "wt181": "off",
  "wt202": "off",
  "wt45": "off",
  "__VIEWSTATEGENERATOR": "AF4B5C7A",
  "wtData": "",
  "wt232": "",
  "wtInput_FiltroTexto": "",
  "wt13": "",
  "wtInput_FiltroConcelho": "",
  "wt88": "__ossli_0",
  "wt28": "__ossli_0",
  "wt77": "__ossli_0",
  "wtNUTII": "__ossli_0",
  "wtNUTIII": "__ossli_0",
  "wt49": "on",
  "wt57": "on"
}

# Export CSV
print "Downloading CSV..."
browser.open(csv_url, method='post', data=csv_download_data)

# Write CSV file
print "Saving CSV..."
file = open(csv_directory + "/" + csv_filename + ".csv", "wb")
cleaned_csv = str(browser.parsed).split("<html><body><p>", 1)[1].split("</p></body></html>", 1)[0]
file.write(cleaned_csv)
file.close()


print "THE END :)"




