
# imports ######################################################################

from pandas import DataFrame
import sys, os, csv

# variables ####################################################################

data_path = os.path.join('.', 'Resources', 'election_data.csv')
save_path = os.path.join('.', 'election_results.txt')

# methods ######################################################################

def load_data(header=True):
    """Process contents of CSV file 'data_path' and populate global variables
       'candidates', 'counties', and 'votes' with relevent data """
    global candidates, counties, votes
    
    candidates = set()  # set of candidates appearing in data
    counties   = set()  # set of counties   ...
    votes      = dict() # structure encoding data entries

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

                # votes[name]:
                #    The votes for each candidate will be partitioned
                #       by county (i.e. indexed by counties) we 
                #       initialize votes[name] accordingly
                #
                votes[name] = dict()
            
            if not county in votes[name]:
                # add county to counties and initialize votes[name][county]
                
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

            # record vote by placing 'voterid' in set() corresponding to
            # 'name' selected and 'county' voted in.            
            votes[name][county].add(voterid)
            pass    

def get_results():
    """Assemble table of results by county, with columns corresponding to
       candidates and rows corresponding to counties.
       Returns: pd.DataFrame() containing table """
    global candidates, counties, votes
    
    # get vote totals by county and candidate
    results = \
        dict(map(lambda x : \
                 ( x, dict(map(lambda y : \
                               ( y, len(votes[x][y]) ), counties)) ),
                 candidates))
    # return DataFrame initialized with table
    return DataFrame( results )

def print_summary(results, out=sys.stdout):
    """Calculate summary information for 'results', then
       format and print this information to the file() 'out' """
    
    sep = "\n"+"-"*50+"\n" # separater 
    
    totals  = results.sum()   # popular vote
    winner  = totals.idxmax() # popular vote winner
    turnout = totals.sum()    # total votes
    perc    = totals/turnout  # % of popular vote
    
    combined = DataFrame({"votes": totals,
                           "perc": perc.apply("{:.2%}".format)})
    # summary format
    fmt = (f"{sep}"
           f" County Totals: {sep}{results.transpose()}{sep}"
           f"  Popular Vote: {sep}{combined.to_string(header=False)}{sep}"
           f"   Total Votes: {turnout}\n"
           f"        Winner: {winner}{sep}")
    print(fmt, file=out)
    pass

# script entry-point ###########################################################

if __name__ == "__main__":
    # load election data
    load_data()
 
    # extract results
    results = get_results() 

    # display summary of results
    print_summary(results)    

    with open(save_path, "w") as out:
         # write results summary to 'out'
        print_summary(results, out=out)

    # exit cleanly
    sys.exit(0)
