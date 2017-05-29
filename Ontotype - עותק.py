#!/usr/bin/python

# patientGeneVec(Dictionary - key:gene, value:0/1) - Patient vector, each cell is indicate if gene mutated
def makeOntotype(patientGeneVec):
    pass

def main():
    terms = []
    with open("telomere_len_child_2_parent.txt") as fp:
        for line in fp:
            for s in line.split():
                if s not in terms:
                    terms.append(s)
    print terms
    fp1 = open("telomere_len_gene_2_term.txt",'w')
    with open("goa_human.txt") as fp:
        l = []
        for line in fp:
            i = 0
            gene = ""
            term = ""
            for s in line.split():
                if i == 1:
                    gene = s
                if i == 3:
                    term  = s.replace(":", "_")
                    if term not in terms:
                        term = ""
                    break
                i += 1
            if term == "":
                continue
            s1 = gene + "	" + term + '\n'
            if s1 not in l:
                fp1.write(s1)
                l.append(s1)
    fp1.close()
    pass

if __name__ == "__main__":
    main()
