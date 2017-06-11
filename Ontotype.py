#!/usr/bin/python

from goatools.obo_parser import GODag
from Bio.UniProt.GOA import gafiterator
import gzip
from collections import deque
import csv
import xlrd


terms = {}

annotations = {}
# GO graph
GOgraph = {}
# topological sorted GO graph order
SampleGeneDic = {}

convertIdToName = {}


def kahnTopsort(graph):
    in_degree = {u: 0 for u in graph}  # determine in-degree
    for u in graph:  # of each node
        for v in graph[u]:
            in_degree[v] += 1

    Q = deque()  # collect nodes with zero in-degree
    for u in in_degree:
        if in_degree[u] == 0:
            Q.appendleft(u)

    L = []  # list for order of nodes

    while Q:
        u = Q.pop()  # choose node of zero in-degree
        L.append(u)  # and 'remove' it from graph
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                Q.appendleft(v)

    if len(L) == len(graph):
        return L
    else:  # if there is a cycle,
        return []  # then return an empty list

# SampleGeneVec(Dictionary - key:gene, value:0/1) - Sample vector, each cell is indicate if gene mutated
# terms - GO terms according to gene annotations
def makeOntotype(sampleGeneVec, terms, order):
    for gene in sampleGeneVec:
        for term in annotations[gene]:
            terms[term] += sampleGeneVec[gene]

    for t in order:
        for a in GOgraph[t]:
            terms[a] += terms[t]

    return terms
    pass


def xls2csv():
    wb = xlrd.open_workbook('united.xlsx')
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open('united_csv.csv', 'wb')
    wr = csv.writer(your_csv_file)
    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    your_csv_file.close()
    pass

def getSampleData():
    print "convert xls to csv"
    xls2csv()
    print "get sample data"
    with open("united_csv.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sampleId = row['SampleID']
            if sampleId == '':
                continue
            if row['Gender'] == 'male':
                SampleGeneDic[sampleId] = {'TL': row['TL'], 'Age': row['Age'], 'Gender': '0'}
            elif row['Gender'] == 'female':
                SampleGeneDic[sampleId] = {'TL': row['TL'], 'Age': row['Age'], 'Gender': '1'}
            else:
                continue
            SampleGeneDic[sampleId]['geneVec'] = {}
            for gene in annotations:
                try:
                    if row[convertIdToName[gene]] == '1.0':
                        print "gene id: ", gene
                        print "gene name: ", convertIdToName[gene]
                        print "yes"
                        SampleGeneDic[sampleId]['geneVec'][gene] = 1;
                    else:
                        print "no"
                        SampleGeneDic[sampleId]['geneVec'][gene] = 0;
                except:
                    print "fuck"
                    SampleGeneDic[sampleId]['geneVec'][gene] = 0
    pass

def creatingGraph():
    obo_file = "go-basic.obo"
    g = GODag(obo_file)
    for t in terms:
        GOgraph[t] = []
        for a in g[t].parents:
            if a.id not in terms:
                continue
            GOgraph[t].append(a.id)

    order = kahnTopsort(GOgraph)
    return order
    pass


def makeConvertIdToNameDic():
    with open("convertIdToName.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            convertIdToName[row['ID']] = row['name']
    pass

def creatingValidAnnotation(fieldnames):
    try:
        fp = gzip.open('goa_human.gaf.gz', 'rt')
    except ValueError:
        fp = gzip.open('goa_human.gaf.gz', "r")
    with fp:
        for annotation in gafiterator(fp):
            if annotation['DB_Object_ID'] not in convertIdToName:
                continue
            if annotation['DB_Object_ID'] in annotations:
                if annotation['GO_ID'] not in annotations[annotation['DB_Object_ID']]:
                    annotations[annotation['DB_Object_ID']].append(annotation['GO_ID'])
            else:
                annotations[annotation['DB_Object_ID']] = [annotation['GO_ID']]
            if annotation['GO_ID'] not in terms:
                terms[annotation['GO_ID']] = 0
                fieldnames += [annotation['GO_ID']]
    return fieldnames
    pass

def main():
    print "create convert from gene id to gene name dic"
    makeConvertIdToNameDic()
    fieldnames = ['TL','Age','Gender']
    print "creating annotations"
    fieldnames = creatingValidAnnotation(fieldnames)
    print "creating graph"
    order = creatingGraph()
    getSampleData()
    termDict = {}
    print "go over each sample"
    with open("Database.csv", "ab") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        i = 0
        for sampleID in SampleGeneDic:
            print i
            i += 1
            print "sample id:", sampleID
            for t in terms:
                terms[t] = 0
            termDict[sampleID] = makeOntotype(SampleGeneDic[sampleID]['geneVec'], terms, order)
            dic = {'TL':SampleGeneDic[sampleID]['TL'],'Age':SampleGeneDic[sampleID]['Age'],'Gender':SampleGeneDic[sampleID]['Gender']}
            for t in termDict[sampleID]:
                dic[t] = termDict[sampleID][t]
            writer.writerow(dic)
            print "*********************************"


if __name__ == "__main__":
    main()
    pass
