
# imports ######################################################################

import sys, os, csv

# variables ####################################################################

data_path = os.path.join('.', 'Resources', 'budget_data.csv')
save_path = os.path.join('.', 'budget_summary.txt')

months = [ ]
values = [ ]
deltas = [ ]

# functions ####################################################################

def load_data(header=True):
    """Process contents of CSV file 'data_path', populating the lists
       'months', 'values', and 'deltas' with the relevent information (in order)"""
    
    with open(data_path) as infile:
        # create reader
        csvobj = csv.reader(infile, delimiter=',')

        # burn header, if present
        if header:
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



def print_summary(out=sys.stdout):
    """print summary info. for data to file() 'out'"""
    # extract largest total *decrease* in profit by
    #    finding minimum value of negative changes to profit
    max_dec = min(filter(lambda x : x < 0, deltas))
    max_dec_month = months[ deltas.index(max_dec) + 1 ]

    # extract largest total *increase* in profit by
    #    finding maximum value of postitive changes to profit
    max_inc = max(filter(lambda x : x > 0, deltas))
    max_inc_month = months[ deltas.index(max_inc) + 1 ]
    
    print(file=out,
          "Summary/Analysis\n---------------------------------------\n"
          " Months:\n  {:20s}:{:>15d}\n\n"
          " Profit/Loss:\n  {:20s}: ${:13.2f}\n  {:20s}: ${:13.2f}\n\n"
          " Extrema:\n  {:20s}: ${:13.2f}\n  {:20s}:{:>15s}\n  {:20s}:"
          " ${:13.2f}\n  {:20s}:{:>15s}\n".format("Total", len(months),
                                      "Total", sum(values),
                                      "Average Change", sum(deltas)/len(deltas),
                                      "Max. Increase", max_inc,
                                      "Max. Increase Month", max_inc_month,
                                      "Min. Decrease", max_dec,
                                      "Min. Decrease Month", max_dec_month))
    pass

# script entry-point ###########################################################

if __name__ == "__main__":
    # load data from 'budget_data.csv'
    load_data()

    # produce summary for data
    print_summary()
    
    # write summay to 'save_file'
    with open(save_file, "w") as out:
        print_summary(out=out)
        
    sys.exit(0)      # exit cleanly
