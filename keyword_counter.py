from Bio import Entrez, Medline
import re

def search():
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',sort='relevance',retmax='1',term='LOX')
    results = Entrez.read(handle)
    return results['IdList']

def medline():
    Keywords = ['lox','of','oxidized']  #Lijst met keywords
    AB = ''
    
    handle = Entrez.efetch(db='pubmed', id=search(), rettype='medline', retmode='text')
    records = Medline.parse(handle)
    records = list(records)    
    for record in records:
        AB = record.get('AB','?')

    wordlist = AB.split()   #split de Abstract string in lijst met woorden
    wordfreq = []
    for i in wordlist:
        if any(word in i for word in Keywords): #zoekt naar matches in wordlist met Keywords
            wordfreq.append(Keywords.count(i))

    print (list(zip(Keywords, wordfreq)))

