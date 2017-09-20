import csv
import sys, os
import glob

extension = 'csv'
os.chdir("c:\\try\\mutations\\new")
filelst = [i for i in glob.glob('*.{}'.format(extension))]

filelst.remove('Patients.csv')

print filelst
result= []
for fl in filelst:
    print fl
    with open ("Patients.csv", "r") as readU: ##nameeee
        reader = csv.reader(readU)
        readL = list(reader)
    first = readL[0]
    #print first
    with open (fl, "r") as readClin:
        readC = csv.reader(readClin)
        clin = list(readC)
    with open ("vector1New.csv", "a+") as writeU:
        writer = csv.writer(writeU)

        for known in readL: #item in sample
            flag = False
            for item in clin: #item in mutation
                #if item[0] == 'Hugo_Symbol':
                    #break;
                #print known[1]
                substr = item[2].split('-')
                if len(substr[3])>2:
                    substr[3] = substr[3][:2]
                substr = substr[0]+'-'+substr[1]+'-'+substr[2]+'-'+substr[3]
                #print substr

                if substr == known[2]:
                    #print "aaaaaaa"
                    #print first.index(item[0])
                    flag = True 
                    if item[4] == 'None':
                        
                        if item[0] in first:
                            known[first.index(item[0])]='0'
                    else:
                        
                        if item[0] in first:
                            known[first.index(item[0])]='1'
            if flag:
                writer.writerow(known)
    writeU.close()
    readClin.close()
    readU.close()
#with open ("vector.csv", "wb") as writeU:
#    writer = csv.writer(writeU)
#    for item in result:
#        writer.writerow(item)
#writeU.close()
            
