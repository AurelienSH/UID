import sys
from os import path

def myTXM(files):
    source, selected, unSelected, tracker = files
    with open(source, "r") as f_in:
        doc = f_in.readlines()

    with open(tracker, "r") as f:
        i = len(f.readlines())

    size = len(doc)

    with open(tracker, "a") as tracker_f:
        with open(unSelected, "a") as unSelected_f:
            with open(selected, "a") as selected_f:
                for l in doc[i:]:
                    print(l)
                    print(f"[{i}/{size}] is there a cc [y/N]")
                    writer(selected_f, unSelected_f, l)
                    tracker_f.write("\n")
                    i+=1

    print("fichier fini")
    return("prout")

def writer(selected, unSelected, text):
    rep = input()
    if rep == "y":
        selected.write(text)
    elif rep == "n" or not rep:
        unSelected.write(text)
    else:
        print("input unclear, type 'y' or 'n' to proceed")
        writer(selected, unSelected, text)

def createFiles(check):
    if check == "that" or check == "nothat":
        source = f"{check}CCutterances.txt"
        selected = f"{check}Selected.txt"
        unSelected = f"{check}UnSelected"
        tracker = f"{check}Tracker.pkl"
        for file in [selected, unSelected, tracker]:
            if not path.isfile(file):
                open(file, 'w').close()
        return [source, selected, unSelected, tracker]
    else:
        print('The only arguments available are "that" or "nothat" depending on the type of CC you wish to select')
        newCheck = input()
        createFiles(newCheck)

if __name__ == '__main__':
    that = sys.argv[1]
    files = createFiles(that)
    myTXM(files)



