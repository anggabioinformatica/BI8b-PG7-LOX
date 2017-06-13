#####################################
### Author: Jacco Schaap
### E-mail: jacco_schaap@hotmail.com
### Last update 13-6-17
#####################################

from flask import Flask, render_template, request
app = Flask(__name__)
from Bio import Entrez, Medline
from Keyword_list import Keywords

# lox1 = ["LOX1", "LOX-1", "1-LOX", "1-lipoxygenase", "lipoxygenase-1", "lipoxygenase1", "1lipoxygenase", "Lipoprotein Receptor-1"]
# lox2 = ["LOX2", "LOX-2", "2-LOX", "2-lipoxygenase", "lipoxygenase-2", "lipoxygenase2", "2lipoxygenase", "Lipoprotein Receptor-2"]
# lox3 = ["LOX3", "LOX-3", "3-LOX", "3-lipoxygenase", "lipoxygenase-3", "lipoxygenase3", "3lipoxygenase", "Lipoprotein Receptor-3"]
# lox4 = ["LOX4", "LOX-4", "4-LOX", "4-lipoxygenase", "lipoxygenase-4", "lipoxygenase4", "4lipoxygenase", "Lipoprotein Receptor-4"]
# lox5 = ["LOX5", "LOX-5", "5-LOX", "5-lipoxygenase", "lipoxygenase-5", "lipoxygenase5", "5lipoxygenase", "Lipoprotein Receptor-5"]
# lox6 = ["LOX6", "LOX-6", "6-LOX", "6-lipoxygenase", "lipoxygenase-6", "lipoxygenase6", "6lipoxygenase", "Lipoprotein Receptor-6"]
# lox7 = ["LOX7", "LOX-7", "7-LOX", "7-lipoxygenase", "lipoxygenase-7", "lipoxygenase7", "7lipoxygenase", "Lipoprotein Receptor-7"]
# lox8 = ["LOX8", "LOX-8", "8-LOX", "8-lipoxygenase", "lipoxygenase-8", "lipoxygenase8", "8lipoxygenase", "Lipoprotein Receptor-8"]
# lox9 = ["LOX9", "LOX-9", "9-LOX", "9-lipoxygenase", "lipoxygenase-9", "lipoxygenase9", "9lipoxygenase", "Lipoprotein Receptor-9"]
# lox10 = ["LOX10", "LOX-10", "10-LOX", "10-lipoxygenase", "lipoxygenase-10", "lipoxygenase10", "10lipoxygenase", "Lipoprotein Receptor-10"]
# lox11 = ["LOX11", "LOX-11", "11-LOX", "11-lipoxygenase", "lipoxygenase-11", "lipoxygenase11", "11lipoxygenase", "Lipoprotein Receptor-11"]
# lox12 = ["LOX12", "LOX-12", "12-LOX", "12-lipoxygenase", "lipoxygenase-12", "lipoxygenase12", "12lipoxygenase", "Lipoprotein Receptor-12"]
# lox13 = ["LOX13", "LOX-13", "13-LOX", "13-lipoxygenase", "lipoxygenase-13", "lipoxygenase13", "13lipoxygenase", "Lipoprotein Receptor-13"]
# lox14 = ["LOX14", "LOX-14", "14-LOX", "14-lipoxygenase", "lipoxygenase-14", "lipoxygenase14", "14lipoxygenase", "Lipoprotein Receptor-14"]
# lox15 = ["LOX15", "LOX-15", "15-LOX", "15-lipoxygenase", "lipoxygenase-15", "lipoxygenase15", "15lipoxygenase", "Lipoprotein Receptor-15"]


def main():
    # search()
    # medline()
    app.run(debug=True)


def search(zoek):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='10',
                            term=zoek)
    results = Entrez.read(handle)
    return results["IdList"]


def medline(zoek):
    handle = Entrez.efetch(db="pubmed", id=search(zoek), rettype="medline",
                           retmode="text")
    records = Medline.parse(handle)
    records = list(records)
    return records


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/results', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        zoek = request.form['s']
        lijst = medline(zoek)
        sturen = []
        d = []

        for item in lijst:
            ID = item.get('PMID', '?')
            AB = item.get('AB', '?').upper()

            wordlist = AB.split()  # split de Abstract string in lijst met woorden
            wordfreq = []

            wordfreq = [wordlist.count(p) for p in Keywords]
            freqdict = dict(zip(Keywords, wordfreq))

            data = [(freqdict[key], key) for key in freqdict]
            data.sort()
            data.reverse()

            data2 = [(t[1], t[0]) for t in data]

            # print(data2)

            result = {ID: data2}
            # print result
            d.append(result)


            tijdelijk = []
            if len(item) == 0:
                continue
            ### first item in temporary list
            tijdelijk.append(item.get("TI", "?"))  # first item of list is title

            ### second item in temporary list
            hits = []  # empty hit list per abstract
            if "AB" in item:  # select abstract only ant iterate over it
                abstractje = item.get("AB", "?")
                abstract = abstractje.lower()
                abstract = abstract.split(' ')  # split abstract to list for lox search
                for woord in abstract:
                    woord = woord.replace('(', '').replace(')', '').replace(',', '').replace('.', '').replace(';', '')
                    if 'lox' in woord and woord not in hits:
                        hits.append(woord)
                        # print hits
            tijdelijk.append("; ".join(hits))

            ### third item in temporary list is organism
            tijdelijk.append('***ANGGA***')

            ### fourth item in temporary list is the kingdom
            tijdelijk.append('***ANGGA***')

            ### fith item are the applications found in the abstract
            toepassing_list = []
            for key, value in result.iteritems():
                for toepassing in value:
                    if toepassing[1] != 0:
                        toepassing_list.append(toepassing[0])
            tijdelijk.append("; ".join(toepassing_list))

            ### sith item are the authors of the article
            tijdelijk.append(item.get("AU", "?"))

            ### seventh item is the PubMedID of the article
            tijdelijk.append(item.get("PMID", "?"))

            ### ninth item is the date of publication
            tijdelijk.append(item.get("DP", "?"))

            ### tenth item is the MeSH of publication
            tijdelijk.append(item.get("MH", "?"))

            ### eleventh item is the abstract of the article
            tijdelijk.append(item.get("AB", "?"))

            sturen.append(tijdelijk)
        # print sturen
        return render_template('index.html', sturen=sturen)

main()
