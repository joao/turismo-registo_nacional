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
csv_filename = "empreendimentos-turisticos"

# Strings to ASCII function for districts
def string_simplify(string):
  "strings to ASCII, useful for district names"
  return unidecode(string).lower().replace (" ", "_")


base_url = 'https://rnt.turismodeportugal.pt/RNET/Registos.ConsultaRegisto.aspx'
csv_url = 'https://rnt.turismodeportugal.pt/RNET/Registos.ConsultaRegisto.aspx' # They have 'Ao' in between the URLs


# Print information
print "Getting all the local tourism enterprises CSV in Portugal..."
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
  "__EVENTTARGET": "wt79",
  "__EVENTARGUMENT": "",
  "__OSVSTATE": OSVSTATE,
  "__VIEWSTATE": "",
  "__VIEWSTATE": "",
  "wt307": "off",
  "wt21": "off",
  "wt245": "off",
  "wt323": "off",
  "wt266": "off",
  "wt348": "off",
  "wt347": "off",
  "wt389": "off",
  "wt150": "off",
  "wt62": "off",
  "wt126": "off",
  "wt100": "off",
  "wt198": "off",
  "wt165": "off",
  "wt384": "off",
  "wt230": "off",
  "wt350": "off",
  "wt340": "off",
  "wt149": "off",
  "wt273": "off",
  "wt270": "off",
  "wt161": "off",
  "wt211": "off",
  "wt328": "off",
  "wt310": "off",
  "wt371": "off",
  "wt300": "off",
  "wt232": "off",
  "wt157": "off",
  "wt398": "off",
  "wt162": "off",
  "wt385": "off",
  "wt57": "off",
  "wt221": "off",
  "wt223": "off",
  "wt69": "off",
  "wt56": "off",
  "wt63": "off",
  "wt175": "off",
  "wt137": "off",
  "wt260": "off",
  "wt115": "off",
  "__VIEWSTATEGENERATOR": "9963D09B",
  "wtData": "",
  "wtSearchInput2": "",
  "wt171": "",
  "wt258": "",
  "wtDistrito": "__ossli_0",
  "wt152": "",
  "wtConcelho": "__ossli_0",
  "wtERT": "__ossli_0",
  "wtNUTII": "__ossli_0",
  "wtNUTIII": "__ossli_0"
}

# Export csv
print "Downloading CSV..."
browser.open(csv_url, method='post', data=csv_download_data)

# Write CSV file
print "Saving CSV..."
file = open(csv_directory + "/" + csv_filename + ".csv", "wb")
cleaned_csv = str(browser.parsed).split("<html><body><p>", 1)[1].split("</p></body></html>", 1)[0]
file.write(cleaned_csv)
file.close()


print "THE END :)"



