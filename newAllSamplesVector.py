import csv
import sys, os
import glob


extension = 'csv'
os.chdir("C:\\try")

with open ("genes.csv", "r") as readgenes:
    readC = csv.reader(readgenes)
    allGenes = list(readC)

with open ("allSamples.csv", "r") as readsamples:
    readD = csv.reader(readsamples)
    sample = list(readD)

indexes = [0,1,2,3,4,5]

i=-1;
for gen in sample[0]:
    i=i+1
    if gen in allGenes[0]:
        indexes.append(i)

readgenes.close()
readsamples.close()

print "aaaaaaaa"

with open ("vectors.csv", "wb") as writeU:
    writer = csv.writer(writeU)
    with open ("allSamples.csv", "r") as readsamples:
        readE = csv.reader(readsamples)
        sample = list(readE)

    for item in sample:
        writer.writerow([item[j] for j in indexes])
    readsamples.close()

writeU.close()
            
