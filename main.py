# "www.verbformen.de"
# verbs = ["machen"]

import csvinterface as csvi
import re
import requests
from bs4 import BeautifulSoup as bs

# PARSES ONE CONJUGATION OF A CERTAIN TENSE
def trtext(tr)->str:
    outstr = []
    for td in tr.find_all("td"):
        for item in td.contents:
            notags = re.sub("<.*?>", "", str(item))
            outstr.append(notags)
    return "".join(outstr)

def get_conjugations(verb: str)->list:
    # sleep(1)
    url = f"https://www.verbformen.de/konjugation/?w={verb}"
    r = requests.get(url)
    soup = bs(r.text, "html5lib")

    mainsection = ""

    maindiv = soup.find_all("div", attrs={"class": "rAbschnitt"})
    for section in maindiv[0].find_all("section"):
        verbtype = section.find("header").find("h2")
        if verbtype is not None and verbtype.text == "Indikativ":
            mainsection = section
            break
    else:
        return []

    # ITER THRU EACH TENSE
    conjugs = []
    for table in mainsection.find_all("div", class_="vTbl"):
        for tr in table.find_all("tr"):
            conjugs.append(trtext(tr))
    
    return conjugs

infinitives = csvi.verbreturns()
bigverbs = []
zed = 0
from time import sleep
from random import randint
for verb in infinitives:
    try:
        oneVerbConjugs = get_conjugations(verb)
        # print(oneVerbConjugs)
        if len(oneVerbConjugs) == 0:
            continue
        oneVerbConjugs.insert(0, verb)
        # print(oneVerbConjugs)
        zed += 1
        csvi.appverbs([oneVerbConjugs])
        print(f"successfully conjugated {verb}")
        # bigverbs.append(oneVerbConjugs)
    except:
        print(f"Err on {verb}")
        sleep(randint(2, 6))
# "https://www.verbformen.de/konjugation/?w=machen"
# csvi.appverbs(bigverbs)
print(f"Conjugated {zed} verbs")