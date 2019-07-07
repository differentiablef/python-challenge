
# imports ######################################################################

import os, sys, re

from nltk.tokenize import word_tokenize
from nltk import download

# script #######################################################################

data_dir = os.path.join('.', 'Resources')

summary_fmt = """{sep}
Filename:             {path}
Sentence Count:       {sent_count}
Mean Sentence Length: {mean_sent_length}
Word Count:           {word_count}
Mean Word Length:     {mean_word_length}"""

sep =  ('-' * 50)

# script #######################################################################

# initialize list of files to process
data_paths = list()
for filename in os.listdir(data_dir):
    data_paths.append(
        os.path.join(data_dir, filename))

# make sure the trained punkt model distributed with nltk is up-to-date
download('punkt')

# process the prose contained in each file listed in 'data_paths'
for path in data_paths:
    with open(path, newline='') as infile:
        prose = infile.read()
        pass
    
    # extract list of tokens using 'nltk.tokenize.word_tokenize'
    tokens = word_tokenize( prose )

    # filter out non-essential punct. 
    parts = filter(lambda t: re.fullmatch('[^.!?\w]+', t) == None, tokens)

    # simultaneously compute the relevant summary values.
    word_count = 0
    mean_word_length = 0.0
    sent_count = 0
    mean_sent_length = 0.0
    sent_length = 0

    for tok in parts:
        if tok != '.':
            word_count += 1
            mean_word_length += len(tok)
            sent_length += 1
        else:
            sent_count += 1
            mean_sent_length += sent_length
            sent_length = 0

    mean_word_length = mean_word_length/word_count
    mean_sent_length = mean_sent_length/sent_count

    # display summary information for contents of 'path'
    print(summary_fmt.format(sep=sep,
                             word_count=word_count,
                             mean_word_length=mean_word_length,
                             sent_count=sent_count,
                             mean_sent_length=mean_sent_length,
                             path=path))
    pass

print(f'{sep}')
