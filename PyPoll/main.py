# imports ######################################################################

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
        if header:
            next(csvobj)

        # process remaining entries
        for entry in csvobj:

            candidate = entry[2]
            county    = entry[1]
            voterid   = int(entry[0])

            if not candidate in candidates:
                # add candidate and initialize votes[candidate]
                
                candidates.add(candidate)

                # "votes[candidate]":
                #
                #    The votes for each candidate are partitioned
                #       by county (i.e. indexed by counties) so we use
                #       a dict()
                #
                votes[candidate] = dict()

            
            if not county in votes[candidate]:
                # add county to counties and initialize votes[candidate][county]

                # votes[candidate][county]:
                #
                #   Since voters in a particular county can only cast a single vote,
                #    we will identify the portion of votes cast for 'candidate' 
                #    from 'county' with the set() of voter-id's of people
                #    who voted for 'candidate' in 'county'
                #
                votes[candidate][county] = set()

                # add 'county' to the set() of counties.
                # (done here to cut down on errant calls to 'add')
                counties.add(county)


            # count vote by placing 'voterid' in set() corresponding to
            # 'candidate' selected and 'county' voted in.            
            votes[candidate][county].add(voterid)
            pass


def compute_results():
    """computes matrix of county-level results, with rows corresponding to counties 
       and columns corresponding to candidates; as well as vector of popular vote
       totals indexed by candidate

       returns tuple consisting of the matrix in the first coordinate and 
       vector in the second
       """

    results = \
        dict(map(lambda x : \
                      ( x, sum(map(len, votes[x].values())) ),
                 candidates))
    
    county_results = \
        dict(map(lambda x : \
                      ( x, dict(map(lambda y : \
                                         ( y, len(votes[y][x]) ),
                                    candidates)) ),
                 counties))
    
    return (county_results, results)


if __name__ == "__main__":
    print("something dumber")
    sys.exit(0) # exit cleanly

    
