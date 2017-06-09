from flask import Flask, render_template, request
app = Flask(__name__)
from Bio import Entrez, Medline

LOX_list = ['LOX-1', 'LOX-2', 'LOX-3', 'LOX-4', 'LOX-5', 'LOX-6', 'LOX-7', 'LOX-8', 'LOX-9', 'LOX-10', 'LOX-11', 'LOXL1',
            '12-LOX', '13-LOX']

def main():
    # search()
    # medline()
    app.run(debug=True)


def search(zoek):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='100',
                            term=zoek)
    results = Entrez.read(handle)
    return results["IdList"]


def medline(zoek):
    handle = Entrez.efetch(db="pubmed", id=search(zoek), rettype="medline",
                           retmode="text")
    records = Medline.parse(handle)
    records = list(records)
    # for record in records:
        # print("Title:", record.get("TI", "?"))
        # print("Abstract:", record.get("AB", "?"))
    #     print("source:", record.get("SO", "?"))
    #     print("")
    return records
# @app.route('/')
# def start():
#     return 'Hello, World!'



@app.route('/')
def home():
    return render_template("index.html")

# @app.route('/results')
# def results():
#     lijst = medline()
#     return render_template("index.html", lijst=lijst)

@app.route('/results', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        zoek = request.form['s']
        lijst = medline(zoek)
        for item in lijst:
            if 'Atherosclerosis' in item.get("MH", "?"):
                print item.get("MH", "?")
        return render_template('index.html', lijst=lijst)

main()
