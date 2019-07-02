
# imports ######################################################################

import pandas as pd
import sys, os, csv

# variables ####################################################################

data_path = os.path.join('.', 'Resources', 'election_data.csv')

candidates = set()  # set of candidates appearing in data
counties   = set()  # set of counties   ...
votes      = dict() # structure encoding data entries,
                    #      indexed by candidate then county

# functions ####################################################################

def extract_data(header=True):
    """ Process contents of CSV file 'data_path' and populate the variables
        'candidates', 'counties', and 'votes' with relevent data """
    
    with open(data_path) as infile:
        # create reader associated with file-stream
        csvobj = csv.reader(infile, delimiter=',')

        # discard header, if present
        (not header) or next(csvobj)

        # process remaining entries
        for entry in csvobj:

            name    = entry[2]
            county  = entry[1]
            voterid = int(entry[0])

            if not name in candidates:
                # add name to candidates and initialize votes[name]
                candidates.add(name)

                # "votes[name]":
                #    The votes for each candidate are partitioned
                #       by county (i.e. indexed by counties) we 
                #       initialize votes[name] accordingly
                #
                votes[name] = dict()
            
            if not county in votes[name]:
                # add county to counties and initialize votes[candidate][county]

                # votes[name][county]:
                #   Since voters in a particular county can only cast a single
                #    vote, we will identify the portion of votes cast for
                #    'name' from 'county' with the set() of voter-id's of
                #    people who voted for 'name' in 'county'
                #
                votes[name][county] = set()

                # add 'county' to the set() of counties.
                # (done here to cut down on errant calls to 'add')
                counties.add(county)

            # count vote by placing 'voterid' in set() corresponding to
            # 'name' selected and 'county' voted in.            
            votes[name][county].add(voterid)
            pass


def assemble_results():
    """assembles table of results by county, with rows corresponding to
       candidates and columns corresponding to counties

       returns pd.DataFrame of the assembled table
       """    
    # election results by county
    results = \
        dict(map(lambda x : \
                      ( x, dict(map(lambda y : \
                                         ( y, len(votes[x][y]) ),
                                    counties)) ),
                 candidates))    
    # return DataFrame initialized with table
    return pd.DataFrame( results )

def print_summary(results, out=sys.stdout):
    pass

def dump_results(results, pathname):
    pass

if __name__ == "__main__":

    sys.exit(0) # exit cleanly

    
