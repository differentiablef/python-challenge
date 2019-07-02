
# imports ######################################################################

from us_state_abbrev import us_state_abbrev as abbrev
from datetime import datetime as date
import sys, os, csv

# variables ####################################################################

data_path  = os.path.join('.', 'Resources', 'employee_data.csv')  # input file
clean_path = os.path.join('.', 'employee_data-clean.csv')         # output file

fields = [ 'Emp ID', 'First Name', 'Last Name', 'DOB', 'SSN', 'State' ]
term = lambda e : csv.OrderedDict(\
      [('Emp ID', e.get('Emp ID')),
       ('First Name', e.get('Name').partition(' ')[0]),
       ('Last Name', e.get('Name').partition(' ')[-1]),
       ('DOB', date.strptime(e['DOB'], '%Y-%m-%d').strftime('%m/%d/%Y')),
       ('SSN', '***-**-' + e['SSN'][-4:]),
       ('State', abbrev.get(e['State']))])

data = None

# script #######################################################################

with open(data_path, newline='') as infile:
    data = csv.DictReader(infile)
    with open(clean_path, "w", newline='') as outfile:
        clean = csv.DictWriter(outfile, fields)
        clean.writeheader()
        clean.writerows(map(term, data))
        pass # gg <3
    
