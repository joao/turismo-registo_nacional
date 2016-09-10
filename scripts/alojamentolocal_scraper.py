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
csv_filename = "alojamento-local"

# Strings to ASCII function for districts
def string_simplify(string):
  "strings to ASCII, useful for district names"
  return unidecode(string).lower().replace (" ", "_")

# replace CSV header with an ASCII version
def replace_csv_header(string):
  return string.replace('"Nº de registo";"Data do registo";"Nome do Alojamento";"Modalidade";"Nº Camas";"Nº Utentes";"Localização (Endereço)";"Localização (Código postal)";"Localização (Localidade)";"Localização (Freguesia)";"Localização (Concelho)";"Localização (Distrito)";"Nome do Titular da Exploração";"Contribuinte";"Contacto (Telefone)";"Contacto (Fax)";"Contacto (Telemovel)";"Contacto (Email)"','"numero_de_registo";"data_do_registo";"nome_do_alojamento";"modalidade";"numero_de_camas";"numero_utentes";"endereco";"codigo_postal";"localidade";"freguesia";"concelho";"distrito";"nome_titular_exploracao";"contribuinte";"telefone";"fax";"telemovel";"email"')

# Current date
today = datetime.date.today().strftime('%d-%m-%Y')


base_url = 'https://rnt.turismodeportugal.pt/RNAL/ConsultaAoRegisto.aspx'


# Print information
print "Getting all the local tourism properties CSVs in Portugal."
print "Usually takes ~9 minutes to donwload all."
print

 # Create CSV directory
if not os.path.exists(csv_directory):
  os.makedirs(csv_directory)


# Setup the CSV file with all the districts
file_CSV_districts = open(csv_directory + "/" + csv_filename + "_" + today + ".csv", "wb")
file_CSV_districts.write('"numero_de_registo";"data_do_registo";"nome_do_alojamento";"modalidade";"numero_de_camas";"numero_utentes";"endereco";"codigo_postal";"localidade";"freguesia";"concelho";"distrito";"nome_titular_exploracao";"contribuinte";"telefone";"fax";"telemovel";"email"\n')
file_CSV_districts.close()

# Browse to RNT - Registo Nacional de Turismo
browser = RoboBrowser(history=True)
browser.open(base_url + '?Origem=CP&FiltroVisivel=True')

# Select Districts Labels and Option IDs
search_form = browser.get_form(id='WebForm1')
districts_select = search_form['wt42'] # Get districts select
district_labels = districts_select.labels
district_labels.pop(0) # Remove first value
district_keys = districts_select.options # Get districts ID keys
district_keys.pop(0) # Remove first value

# Build districts dicionary
districts = {}
for idx, d_label in enumerate(district_labels):
    districts[d_label] = district_keys[idx]



# Encrypted Outsystems variable
OSVSTATE = search_form['__OSVSTATE'].value
#print OSVSTATE


# Set districts value
districts_select.value = districts['Aveiro']

# Output selection
print str(len(districts)) + " districts in Portugal."

# Print all districts. Or not.
#for key, value in districts.iteritems():
  #print string_simplify(key) + ': ' + value
#print ""

# Keep tabs of how many districts have already been sorted
district_number = 0

for key, value in sorted(districts.iteritems()):
  "Iterate over all the districts"
  selected_district = string_simplify(key)
  selected_district_option_id = value
  district_number += 1
  print str(district_number) + '. ' + string_simplify(key).title() + '...'
  
  # Form data
  district_form_data = {
    "__AJAX": "1044,746,wt10,381,42,0,0,98,392,",
    "__EVENTARGUMENT": "",
    "__EVENTTARGET": "wt10",
    "__OSVSTATE": OSVSTATE,
    "__VIEWSTATE": "",
    "__VIEWSTATEGENERATOR": "5C0A81B1",
    "wt131": "",
    "wt32": "__ossli_0",
    "wt42": selected_district_option_id,
    "wtData1": "",
    "wtData2": "",
    "wtInput_FiltroTexto": "",
    "wtInput_FiltroTexto2": "",
    "wtInput_FiltroTexto3": "",
    "wtcbModalidade": "__ossli_0"
  }

  # Request specific district
  browser.open(base_url, method='post', data=district_form_data)
  #print browser.parsed



  # Encrypted Outsystems variable
  # Need to parse the html file with JavaScript code returned via AJAX and extract the OSVSTATE
  OSVSTATE_CSV = str(browser.parsed).split("\"__OSVSTATE\":\"", 1)[1].split("\"},\"blockJs\"", 1)[0]


  # CSV_form_data
  csv_form_data = {
    "__EVENTARGUMENT": "",
    "__EVENTTARGET": "wt84",
    "__OSVSTATE": OSVSTATE_CSV,
    "__VIEWSTATE": "",
    "__VIEWSTATEGENERATOR": "5C0A81B1",
    "wt131": "",
    "wt32": "__ossli_0",
    "wt42": selected_district_option_id,
    "wtData1": "",
    "wtData2": "",
    "wtInput_FiltroTexto": "",
    "wtInput_FiltroTexto2": "",
    "wtInput_FiltroTexto3": "",
    "wtcbModalidade": "__ossli_0"
  }

  # Request CSV
  browser.open(base_url, method='post', data=csv_form_data)

 
   # Write CSV files
  file = open(csv_directory + "/" + selected_district + "_" + csv_filename + "_" + today + ".csv", "wb")
  district_csv = str(browser.parsed).split("<html><body><p>", 1)[1].split("</p></body></html>", 1)[0]
  file.write( replace_csv_header(district_csv) )
  file.close()

  # Append to the all the districts CSV file
  file_CSV_districts = open(csv_directory + "/" + csv_filename + "_" + today + ".csv", "a")
  file_CSV_districts.write( district_csv[district_csv.find('\n')+1:district_csv.rfind('\n')] )
  file_CSV_districts.close()



  # Sleep for 5 seconds, as to not overload the server
  time.sleep(5)

print "THE END :)"




