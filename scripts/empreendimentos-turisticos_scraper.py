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



# Print information
print "Getting all the local tourism properties CSV in Portugal..."
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

  
# AJAX search data for all types of properties
search_data = {
  "__EVENTTARGET": "wtbtnSearch",
  "__EVENTARGUMENT": "",
  "__OSVSTATE": OSVSTATE,
  "__VIEWSTATE": "",
  "wt123": "off",
  "wt255": "off",
  "wt192": "off",
  "wt349": "off",
  "wt204": "off",
  "wt30": "off",
  "wt233": "off",
  "wt345": "off",
  "wt147": "off",
  "wt244": "off",
  "wt248": "off",
  "wt262": "off",
  "wt164": "off",
  "wt35": "off",
  "wt101": "off",
  "wt107": "off",
  "wt110": "off",
  "wt143": "off",
  "wt202": "off",
  "wt84": "off",
  "wt184": "off",
  "wt37": "off",
  "wt332": "off",
  "wt166": "off",
  "wt185": "off",
  "__VIEWSTATEGENERATOR": "9963D09B",
  "wtData": "",
  "wtSearchInput2": "",
  "wt77": "",
  "wt92": "",
  "wt151": "",
  "wt126": "",
  "wtERT": "__ossli_0",
  "wtDistrito": "__ossli_0",
  "wtConcelho": "__ossli_0",
  "wtNUTII": "__ossli_0",
  "wtNUTIII": "__ossli_0",
  "wt264": "on",
  "wt343": "on",
  "wt206": "on",
  "wt223": "on",
  "wt17": "on",
  "wt125": "on",
  "wt313": "on",
  "wt176": "on",
  "wt179": "on",
  "wt373": "on",
  "wt252": "on",
  "wt127": "on",
  "wt396": "on",
  "wt60": "on",
  "wt62": "on",
  "wt269": "on",
  "wt208": "on",
  "-668772924": "True",
  "_AJAX": "1151,824,wtbtnSearch,723,44,123,0,87,727,"
}

# Search every type of tourism property
print "Searching..."
browser.open(base_url, method='post', data=search_data)

# AJAX CSV download data
csv_download_data = {
  "__EVENTTARGET": "wt243",
  "__EVENTARGUMENT": "",
  "__OSVSTATE": OSVSTATE,
  "__VIEWSTATE": "",
  "wt123": "off",
  "wt255": "off",
  "wt192": "off",
  "wt349": "off",
  "wt204": "off",
  "wt30": "off",
  "wt233": "off",
  "wt345": "off",
  "wt147": "off",
  "wt244": "off",
  "wt248": "off",
  "wt262": "off",
  "wt164": "off",
  "wt35": "off",
  "wt101": "off",
  "wt107": "off",
  "wt110": "off",
  "wt143": "off",
  "wt202": "off",
  "wt84": "off",
  "wt184": "off",
  "wt37": "off",
  "wt332": "off",
  "wt166": "off",
  "wt185": "off",
  "__VIEWSTATEGENERATOR": "9963D09B",
  "wtData": "",
  "wtSearchInput2": "",
  "wt77": "",
  "wt92": "",
  "wt151": "",
  "wt126": "",
  "wtERT": "__ossli_0",
  "wtDistrito": "__ossli_0",
  "wtConcelho": "__ossli_0",
  "wtNUTII": "__ossli_0",
  "wtNUTIII": "__ossli_0",
  "wt264": "on",
  "wt343": "on",
  "wt206": "on",
  "wt223": "on",
  "wt17": "on",
  "wt125": "on",
  "wt313": "on",
  "wt176": "on",
  "wt179": "on",
  "wt373": "on",
  "wt252": "on",
  "wt127": "on",
  "wt396": "on",
  "wt60": "on",
  "wt62": "on",
  "wt269": "on",
  "wt208": "on",
  "-668772924": "True"
}

# Download csv
print "Downloading CSV..."
browser.open(base_url, method='post', data=csv_download_data)

# Write CSV file
print "Saving CSV..."
file = open(csv_directory + "/" + csv_filename + ".csv", "wb")
cleaned_csv = str(browser.parsed).split("<html><body><p>", 1)[1].split("</p></body></html>", 1)[0]
file.write(cleaned_csv)
file.close()


print "THE END :)"




