#!/usr/bin/python

from goatools.obo_parser import GODag
from Bio.UniProt.GOA import gafiterator
import gzip

annotations = {}
# GO graph
GOgraph = {}
# topological sorted GO graph order
order = []

from collections import deque


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

# patientGeneVec(Dictionary - key:gene, value:0/1) - Patient vector, each cell is indicate if gene mutated
# terms - GO terms according to gene annotations
def makeOntotype(patientGeneVec, terms):
    for gene in patientGeneVec:
        for term in annotations[gene]:
            terms[term] += patientGeneVec[gene]

    for t in order:
        for a in GOgraph[t]:
            terms[a] += terms[t]

    return terms

if __name__ == "__main__":
    terms = {}
    try:
        fp = gzip.open('goa_human.gaf.gz', 'rt')
    except ValueError:
        fp = gzip.open('goa_human.gaf.gz', "r")
    with fp:
        for annotation in gafiterator(fp):
            if annotation['DB_Object_ID'] in annotations:
                if annotation['GO_ID'] not in annotations[annotation['DB_Object_ID']]:
                    annotations[annotation['DB_Object_ID']].append(annotation['GO_ID'])
            else:
                annotations[annotation['DB_Object_ID']] = [annotation['GO_ID']]
            if annotation['GO_ID'] not in terms:
                terms[annotation['GO_ID']] = 0

    obo_file = "go-basic.obo"
    g = GODag(obo_file)
    for t in terms:
        GOgraph[t] = []
        for a in g[t].parents:
            if a.id not in terms:
                continue
            GOgraph[t].append(a.id)

    order = kahnTopsort(GOgraph)
    patientGeneDic = {1:{"Q5KU26":1,"Q5K651":1},2:{},3:{}}
    termDict = {}
    for patientID in patientGeneDic:
        for t in terms:
            terms[t] = 0
        termDict[patientID] = makeOntotype(patientGeneDic[patientID], terms)
        print termDict[patientID]["GO:0005737"]
    #rec = g.query_term('GO:0006915', verbose=True)
    #g.draw_lineage([rec])

    pass
