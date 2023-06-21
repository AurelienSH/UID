import os
import sys

folder = sys.argv[1]

files = [f"{folder}/{file}" for file in os.listdir(folder)]

with open(f"{folder}/concat.conllu", 'w') as fout:
    for file in files:
        print(f"Traitement du fichier : {file}")
        with open(file, 'r') as fin:
            l = fin.readline()
            while l:
                fout.write(l)
                l = fin.readline()