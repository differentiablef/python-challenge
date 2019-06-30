
# imports ######################################################################

import os, csv

# variables ####################################################################

data_path = os.path.join('.', 'Resources', 'budget_data.csv')

months = [ ]
values = [ ]
deltas = [ ]

# routines #####################################################################

def extract_data():
    """Process contents of CSV file 'data_path', populating the lists
       'months', 'values', and 'deltas' with the relevent information (in order)"""
    
    with open(data_path) as infile:
        # create reader
        csvobj = csv.reader(infile, delimiter=',')

        # burn header
        next(csvobj)

        # process remaining entries 
        for entry in csvobj:
            
            month = entry[0]
            value = float( entry[1] )

            if len(values) > 0:
                deltas.append(value - values[-1])
                
            values.append(value)
            months.append(month)            
    return

def print_summary():
    """print summary info. for data extracted using 'extract_data' method"""
    return

# script entry-point ###########################################################

if __name__ == "__main__":
    print("boo")
    
