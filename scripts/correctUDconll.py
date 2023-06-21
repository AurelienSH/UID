import sys
import re
file = sys.argv[1]
d = re.compile(r"\d")
dot = re.compile(r"\d+\.\d+")
dash = re.compile(r"\d+-\d+")
with open(file, "r") as f:
    with open(f"{file.split('.')[0]}_corrected.conllu", "w") as fc:
        l = f.readline()
        id = 0
        oldtonew = {}
        lines = []
        olds = []
        while l:
            if l !="\n" and not l.startswith("#"):
                lines.append(l)
                if re.match(d,l) and not re.match(dash,l):
                    id+=1
                    oldtonew[l.split('\t')[0]] = str(id)
                    olds.append(l.split('\t')[0])
            if l == "\n":
                id=0
                for lin in lines:
                    line = lin
                    for old in olds[::-1]:
                        new = oldtonew[old]
                        line = re.sub(f"(?<=[^\d]){old}(?=[^\d])|^{old}",new,line)
                    fc.write(line)
                oldtonew = {}
                olds=[]
                lines = []
            if l == "\n" or l.startswith("#"):
                fc.write(l)


            l = f.readline()
