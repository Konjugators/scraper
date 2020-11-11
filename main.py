# "www.verbformen.de"
# verbs = ["machen"]

import re
from random import randint
from time import sleep

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver

import csvinterface as csvi

gecko = r"C:\Users\adity\Downloads\geckodriver-v0.27.0-win64\geckodriver.exe"
driver = webdriver.Firefox(executable_path=gecko)

# PARSES ONE CONJUGATION OF A CERTAIN TENSE
def trtext(tr) -> str:
    outstr = []
    badchars = {"¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹", "⁰"}
    for td in tr.find_all("td"):
        for item in td.contents:
            notags = re.sub("<.*?>", "", str(item))
            for exp in badchars:
                notags = notags.replace(exp, "")
            outstr.append(notags)
    return "".join(outstr)


def get_conjugations(verb: str) -> list:
    url = f"https://www.verbformen.de/konjugation/?w={verb}"
    driver.get(url)
    sleep(2)

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);return document.body.scrollHeight;"
    )
    sleep(2)

    r = requests.get(url)
    soup = bs(r.text, "lxml")

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
    conjugs = [verb]
    for table in mainsection.find_all("div", class_="vTbl"):
        for tr in table.find_all("tr"):
            conjugs.append(trtext(tr))
    return conjugs


infinitives = csvi.verbreturns()
del infinitives[0]
zed = 0

try:
    for verb in infinitives:
        try:
            oneVerbConjugs = get_conjugations(verb)
            if len(oneVerbConjugs) == 0:
                continue
            csvi.txtwrite(oneVerbConjugs)
            print(f"successfully conjugated {verb}")
            zed += 1
        except:
            print(f"error on {verb}")
            sleep(1)
except KeyboardInterrupt:
    pass
finally:
    print(f"Conjugated {zed} verbs")
    driver.quit()
