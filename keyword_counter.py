from Bio import Entrez, Medline
from Keyword_list import Keywords
import json




def search():
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',sort='relevance',retmax='10',term='LOX')
    results = Entrez.read(handle)
    return results['IdList']

def medline():   
    handle = Entrez.efetch(db='pubmed', id=search(), rettype='medline', retmode='text')
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

        result = {ID: data}
        d.append(result)


    with open('Output.json','w') as f:
        json.dump(d, f)
        #print(result)
        #print(records)
        #print(ID)
        #print(data)
 
        #with open('Output.json','w') as outfile:
            #json.dump(data, outfile)



        
