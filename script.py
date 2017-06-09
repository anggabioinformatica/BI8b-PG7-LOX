from Bio import Entrez, Medline

def main():
    # search()
    medline()

def search():
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='20',
                            term='LOX')
    results = Entrez.read(handle)
    return results["IdList"]



def medline():
    handle = Entrez.efetch(db="pubmed", id=search(), rettype="medline",
                               retmode="text")
    records = Medline.parse(handle)
    records = list(records)
    for record in records:
        print("title:", record.get("TI", "?"))
        print("authors:", record.get("AU", "?"))
        print("source:", record.get("SO", "?"))
        print("")


main()


# def fetch_details(id_list):
#     ids = ','.join(id_list)
#     Entrez.email = 'your.email@example.com'
#     handle = Entrez.efetch(db='pubmed',
#                            retmode='xml',
#                            id=ids)
#     results = Entrez.read(handle)
#     return results
#
#
# if __name__ == '__main__':
#     results = search('fever')
#     id_list = results['IdList']
#     papers = fetch_details(id_list)
#     for i, paper in enumerate(papers):
#         print("%d) %s" % (i+1, paper['MedlineCitation']['Article']['ArticleTitle']))
#     # Pretty print the first paper in full to observe its structure
#     import json
#     print(json.dumps(papers[0], indent=2, separators=(',', ':')))
#