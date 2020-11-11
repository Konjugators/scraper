def verbreturns():
    return infinitives

def formatting(verbs):
    length = len(verbs)
    bad_things = ["⁵", "³", "²"] 
    for i in range(length):
        for z in bad_things:
            verbs[i] = verbs[i].replace(z, "")
        verbs[i] = verbs[i].strip()        
    return verbs


def appverbs(z:list):
    with open("new_verbs.csv", "a") as newverbs:
        csvWriter = csv.writer(newverbs, delimiter=",")
        csvWriter.writerows(z)
    # print("finished")

if __name__ == "__main__" or __name__ != "__main__":
    import csv
    global infinitives
    global conjugations
    conjugations = []
    infinitives = []
    import os
    this_dir, this_filename = os.path.split(__file__)
    path = os.path.join(this_dir, "verbs.csv")
    with open(path, "r", newline="") as file:
        verblist = csv.reader(file)
        for row in verblist:
            infinitives.append(row[0])