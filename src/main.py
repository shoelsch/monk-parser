#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import os
import operator

from lxml import etree
from nltk.corpus import stopwords
from optparse import OptionParser
from collections import Counter

PUNCTUATION = string.punctuation
STOPWORDS = stopwords.words('english')

def main():
    print PUNCTUATION
    parser = OptionParser()
    parser.add_option("-d", "--dir", action="store", type="string", dest="filedir", help="Path to corpus directory")
    (options, args) = parser.parse_args()
    
    tokenID = dict() # Token-UID mapper
    uuid = 0 # Keep track of unique tokens

    # Iterate over user-defined directory
    with open("corpus.dat", "wb") as fh:
        for subdir, dirs, files in os.walk(options.filedir):
            for f in files:
                # Only read XML files
                if f.split(".")[1] == "xml":
                    fname = os.path.join(subdir, f)
                    print "[INFO] Reading %s" % (fname)
                    tree = etree.iterparse(fname, tag="{*}w")
                    tokenFreq = Counter()

                    # Iterate over XML tree
                    for event, element in tree:
                        token = element.get('lem').lower()
                        if token not in PUNCTUATION and token not in STOPWORDS:
                            if token not in tokenID:
                                tokenID[token] = uuid
                                tokenFreq[uuid] += 1
                                uuid += 1
                            else:
                                tokenFreq[tokenID[token]] += 1

                    fh.write(" ".join([str(len(tokenFreq))] + ["%i:%i" % (k,v) for k,v in tokenFreq.most_common()]) + "\n")

    print "[INFO] Writing vocabulary file"
    with open("vocab.txt", "wb") as fh:
        for k,v in sorted(tokenID.items(), key=operator.itemgetter(1)):
            fh.write(k.encode('utf-8') + "\n")

if __name__ == "__main__":
    main()