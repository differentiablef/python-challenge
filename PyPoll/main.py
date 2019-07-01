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
                #   Since voters in a particular county can only cast a single
                #    vote, we will identify the portion of votes cast for
                #    'candidate' from 'county' with the set() of voter-id's of
                #    people who voted for 'candidate' in 'county'
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
    """assemble matrix of county-level vote totals, with rows corresponding to
       candidates and columns corresponding to counties; 

       returns said matrix
       """
    # election results by county
    results = \
        dict(map(lambda x : \
                      ( x, dict(map(lambda y : \
                                         ( y, len(votes[x][y]) ),
                                    counties)) ),
                 candidates))
    return results

def save_results(results, out=sys.stdout):
    """dump the contents of the structure 'results' to file() 'out'
       using an appropriate file schema"""
    pass


def print_summary(results, out=sys.stdout):
    """print a human-readable summary of 'results' to the file() 'out'
       meeting the requirements of the exercise"""

    ll = len(counties) * 11 - 2
    topfmt = "{:>10s} | {:<" + str(ll) + "s}| {:<10s}"
    rowfmt = " {:>9s} :" + "{:>10.0f} " * (len(counties) - 1)+"{:>10.0f} : {:<9.0f}"


    print("Election Info\n"+"-"*80)
    
    #print(f"Candidates: {len(candidates)}")
    #print(f"Votes-Cast: "
    #      f"{sum([sum(map(len, votes[can].values())) for can in candidates])}")
          
    #pop = sum(map( lambda x : sum(county_results[x].values()), candidates ))
    #cty_pop = dict( [ (cty, sum(map(lambda x : county_results[x].get(cty), candidates))) for cty in sorted(counties) ] )

    print("Results:\n"+"-"*80)
    print(topfmt.format("[Name]", "[Votes] (by county)", "[Total]"))
    print("-"*80)
    for can in sorted(candidates):
        
        total = sum(results[can].values())
        itr   = map(results[can].get, sorted(counties))
        print(rowfmt.format(can, *itr,  total))


    print("-"*80)
    keyfmt = "County-Totals:" +"{:>8d} " + "{:>10d} " * (len(counties)-2)+"{:>10d}"
    bycty = [sum([results[c].get(ct) for c in candidates] ) \
             for ct in sorted(counties)]
    print(keyfmt.format(*bycty))
    keyfmt = "County-Name:" + "{:>10s} " * (len(counties) - 1)+"{:>10s}"
    print(keyfmt.format(*sorted(counties)))
    print(f"Counties: {len(counties)}")


    pass


if __name__ == "__main__":
    output_file = os.path.join('.', 'results')
    
    extract_data()               # extract data from file
    results = compute_results()  # compute/assemble derived 'results'
    print_summary(results)       # print a summary of 'results'
    
    with open(output_file, "w") as ofile:
        save_results(ofile)     # dump 'results' to output file

    
    sys.exit(0) # exit cleanly

    
