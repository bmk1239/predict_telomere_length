#!/usr/bin/python

from goatools.obo_parser import GODag
from Bio.UniProt.GOA import gafiterator
import gzip
from collections import deque
import csv
import urllib2, urllib




def main():
    annotations = []
    with open("convertIdToNam1e.csv", "wb") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['ID','name'])
        writer.writeheader()
        try:
            fp = gzip.open('goa_human.gaf.gz', 'rt')
        except ValueError:
            fp = gzip.open('goa_human.gaf.gz', "r")
        with fp:
            i = 0
            for annotation in gafiterator(fp):
                print i
                if (annotation['DB_Object_ID'] not in annotations):
                    annotations += [annotation['DB_Object_ID']]
                    url = 'http://www.uniprot.org/mapping/'
                    params = {'from': 'ACC', 'to': 'GENENAME', 'format': 'tab', 'query': annotation['DB_Object_ID']}
                    data = urllib.urlencode(params)
                    request = urllib2.Request(url, data)
                    response = urllib2.urlopen(request)
                    try:
                        gene_name = response.read(200000).split("\t")[2].split('\n')[0]
                        print gene_name, annotation['DB_Object_ID']
                        writer.writerow({"ID": annotation['DB_Object_ID'], "name": gene_name})
                    except:
                        print "somting wrong ", annotation['DB_Object_ID']
                i += 1

if __name__ == "__main__":
    main()
    pass
