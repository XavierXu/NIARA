"""EntropyExtractor.py: compute the Shannon entropy of a string. This
is representative of the average minimum number of bits required to 
represent the string"""

__author__      = "James Marquardt"
__copyright__   = "Copyright 2015, UWT"

import math
from sets import Set

def domain_entropy(st):
    stList = list(st)
    alphabet = list(Set(stList)) # list of symbols in the string

    # calculate the frequency of each symbol in the string
    freqList = []
    for symbol in alphabet:
        ctr = 0
        for sym in stList:
            if sym == symbol:
                ctr += 1
        freqList.append(float(ctr) / len(stList))

                                                # Shannon entropy
        ent = 0.0
        for freq in freqList:
            ent = ent + freq * math.log(freq, 2)
        ent = -ent
                                                        
        return ent
                                                        
