# -*- coding: utf-8 -*-
 
# Adapted to Python 3.x and RNAL site content as of 2019-09-14

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

# Print information
print("Getting all the local hosts in Portugal...")
print(" ")


# replace CSV header with an ASCII version
def replace_csv_header(string):
  return string.replace('"Nº de registo";"Data do registo";"Nome do Alojamento";"Imovél Posterior 1951";"Data Abertura Público";"Modalidade";"Nº Camas";"Nº Utentes";"Nº Quartos";"Nº Beliches";"Localização (Endereço)";"Localização (Código postal)";"Localização (Localidade)";"Localização (Freguesia)";"Localização (Concelho)";"Localização (Distrito)";"NUTT II";"Nome do Titular da Exploração";"Titular Qualidade";"Contribuinte";"Titular Tipo";"Titular País";"Contacto (Telefone)";"Contacto (Fax)";"Contacto (Telemovel)"','"numero_de_registo";"data_do_registo";"nome_do_alojamento";"edif_posterior_1951";"data_abertura_publico";"modalidade";"numero_de_camas";"numero_utentes";"num_quartos";"num_beliches";"endereco";"codigo_postal";"localidade";"freguesia";"concelho";"distrito";"nut_ii";"nome_titular_exploracao";"qualidade_titular";"contribuinte";"tipo_titular";"pais_titular";"telefone";"fax";"telemovel"')

# Current date
today = datetime.date.today().strftime('%d-%m-%Y')


base_url = 'https://rnt.turismodeportugal.pt/RNAL/ConsultaAoRegisto.aspx'


# Print information
print("Getting all the local tourism properties CSVs in Portugal,")
print("with CSV files for each disctrict and a joint national one.")
print("Usually takes ~35 minutes to download all.")
print(" ")

 # Create CSV directory
if not os.path.exists(csv_directory):
  os.makedirs(csv_directory)


# Setup the CSV file with all the districts
file_CSV_districts = open(csv_directory + "/" + csv_filename + ".csv", "wb")
file_CSV_districts.write(b'"numero_de_registo";"data_do_registo";"nome_do_alojamento";"modalidade";"numero_de_camas";"numero_utentes";"endereco";"codigo_postal";"localidade";"freguesia";"concelho";"distrito";"nome_titular_exploracao";"contribuinte";"telefone";"fax";"telemovel";"email"\n')
file_CSV_districts.close()

# Browse to RNT - Registo Nacional de Turismo
browser = RoboBrowser(history=True,parser="lxml")
browser.open(base_url + '?Origem=CP&FiltroVisivel=True')

# Select Districts Labels and Option IDs
search_form = browser.get_form(id='WebForm1')
districts_select = search_form['wt163'] # Get districts select, previous wt42, wt161
district_labels = districts_select.labels
district_labels.pop(0) # Remove first value
district_keys = districts_select.options # Get districts ID keys
district_keys.pop(0) # Remove first value

# Build districts dicionary
districts = {}
for idx, d_label in enumerate(district_labels):
    districts[d_label] = district_keys[idx]
# print districts

# Encrypted Outsystems variable
OSVSTATE = search_form['__OSVSTATE'].value
# print OSVSTATE


# Output selection
print(str(len(districts)) + " districts in Portugal.")


# Print all districts. Or not.
for key in districts:
  print(string_simplify(key) + ': ' + districts[key])
print("")


# Keep tabs of how many districts have already been sorted
district_number = 0

for key in sorted(districts.keys()):
  "Iterate over all the districts"
  value = districts[key]
  selected_district = string_simplify(key)
  selected_district_option_id = value
  district_number += 1
  print(str(district_number) + '. ' + string_simplify(key).title() + '...')
  
  # Form data
  district_form_data = {
    #"__AJAX": "1044,746,wt10,381,42,0,0,98,392,",
    #"__AJAX": "1241,608,wt132,338,722,167,0,793,354,",
    "__AJAX": "1137,942,wt131,388,747,0,0,784,407,",
    "__EVENTARGUMENT": "",
    "__EVENTTARGET": "wt131",
    "__OSVSTATE": OSVSTATE,
    "__VIEWSTATE": "",
    "__VIEWSTATEGENERATOR": "5C0A81B1",
    "wt159": "",
    "wt140": "__ossli_0",   
    "wt163": selected_district_option_id,    
    "wtData1": "",
    "wtData2": "",    
    "wtInput_FiltroTexto": "",
    "wtInput_FiltroTexto3": "",
    "wtcbModalidade": "__ossli_0"
  }

  # Request specific district
  browser.open(base_url, method='post', data=district_form_data)
  #print(browser.parsed

  # Encrypted Outsystems variable
  # Need to parse the html file with JavaScript code returned via AJAX and extract the OSVSTATE
  OSVSTATE_CSV = str(browser.parsed).split("\"__OSVSTATE\":\"", 1)[1].split("\"},\"blockJs\"", 1)[0]


  # CSV_form_data
  csv_form_data = {
    "__EVENTARGUMENT": "",
    "__EVENTTARGET": "wt103",
    "__OSVSTATE": OSVSTATE_CSV,
    "__VIEWSTATE": "",
    "__VIEWSTATEGENERATOR": "5C0A81B1",
    "wt157": "",
    "wt139": "__ossli_0",
    "wt161": selected_district_option_id,
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
  file = open(csv_directory + "/" + csv_filename + "_" + selected_district +  ".csv", "wb")
  district_csv = str(browser.parsed).split("<html><body><p>", 1)[1].split("</p></body></html>", 1)[0]
   
  file.write(replace_csv_header(district_csv).encode())
  file.close()

  # Append to the all the districts CSV file
  file_CSV_districts = open(csv_directory + "/" + csv_filename + ".csv", "a")
  file_CSV_districts.write( district_csv[district_csv.find('\n')+1:district_csv.rfind('\n')] )
  file_CSV_districts.close()


  # Sleep for 5 seconds, as to not overload the server
  time.sleep(5)

print ("THE END :)")




