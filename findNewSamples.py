import csv
import sys, os
import glob



extension = 'csv'
os.chdir("C:\Users\Mari\Documents\uni\year4\semester b\workshop\originalMUTATIONS")
filelst = [i for i in glob.glob('*.{}'.format(extension))]
filelst.remove('allSamples.csv')


genes = ["Missense_Mutation" ,"Nonsense_Mutation", "Frame_Shift_Del"]

with open ("allSamples.csv", "r") as readsamples:
    readD = csv.reader(readsamples)
    sample = list(readD)



for fl in filelst:
    with open (fl, "r") as readClin:
        readC = csv.reader(readClin)
        mutation = list(readC)

    print fl
    mutation = mutation[1:]
    for item in mutation:
        #print item[9]
        if not(item[9] in genes):
            
            substr = item[16].split('-')
            substr = substr[0]+'-'+substr[1]+'-'+substr[2]
            for sam in sample:
                if sam[1] == substr:
                    if item[1] in sample[0]:
                        sam[sample[0].index(item[1])] =""
                
    readClin.close()


with open ("newSmapless.csv", "wb") as writeU:
    writer = csv.writer(writeU)
    for sam in sample:
        writer.writerow(sam)
           
writeU.close()
readsamples.close()
