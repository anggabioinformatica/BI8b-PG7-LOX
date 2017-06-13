from Bio import Entrez, Medline
from Keyword_list import Keywords
import json

def search(zoek):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',sort='relevance',retmax='10',term= zoek)
    results = Entrez.read(handle)
    return results['IdList']

def medline(zoek):   
    handle = Entrez.efetch(db='pubmed', id=search(zoek), rettype='medline', retmode='text')
    records = Medline.parse(handle)
    records = list(records)

    d = []

    
    for record in records:
        ID = record.get('PMID','?')
        AB = record.get('AB','?').upper()

        wordlist = AB.split() #split de Abstract string in lijst met woorden
        wordfreq = []
        
        wordfreq = [wordlist.count(p) for p in Keywords]
        freqdict = dict(zip(Keywords,wordfreq))

        data = [(freqdict[key], key) for key in freqdict]
        data.sort()
        data.reverse()

        data2 = [(t[1],t[0]) for t in data]

        #print(data2)
        
        result = {ID: data2}
        d.append(result)


    with open('Output.json','w') as f:
        json.dump(d, f)
        #print(result)
        #print(records)
        #print(ID)
        #print(data)
 
        #with open('Output.json','w') as outfile:
            #json.dump(data, outfile)


        
