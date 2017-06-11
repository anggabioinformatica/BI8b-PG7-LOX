from Bio import Entrez, Medline
from Keyword_list import Keywords



def search():
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',sort='relevance',retmax='10',term='LOX')
    results = Entrez.read(handle)
    return results['IdList']

def medline():   
    handle = Entrez.efetch(db='pubmed', id=search(), rettype='medline', retmode='text')
    records = Medline.parse(handle)
    records = list(records)    
    for record in records:
        AB = record.get('AB','?').upper()

        wordlist = AB.split() #split de Abstract string in lijst met woorden
        wordfreq = []
        for i in Keywords:
            wordfreq.append(wordlist.count(i))

        #print('String\n' + AB+ '\n')
        print(list(zip(Keywords, wordfreq)))
        print()

