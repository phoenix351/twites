from flask import Flask
from collections import OrderedDict
import simplejson as js
from itertools import combinations
from spacy import displacy
import spacy
import ast
from NER import predict_NER
from koneksi_database import connectDB
app = Flask(__name__)

### Fungsi Prediksi Berita ###
@app.route('/predict')
def predict():
    """Memprediksi berita menggunakan model NER"""
    predict_NER()
    alert = "Berhasil"

    return alert, 200, {'Access-Control-Allow-Origin': 'http://localhost', 'Access-Control-Allow-Methods': '*'}

### Fungsi Visualisasi NER ###
@app.route('/ner/<text>/<model>')
def ner(text, model):
    """visualisasi NER menggunakan displaCy ENT visualizer."""
    nlp = spacy.load(model)
    doc = nlp(text)
    colors = {"INDICATOR": "#e04747", "LOCATION": "#db732e", "ORGANIZATION": "#2edb6a", "PERSON": "#2e92db",
              "POSITION": "#aa55db", "QUOTE": "#e055ab"}
    options = {"ents": ["INDICATOR", "LOCATION", "ORGANIZATION", "PERSON", "POSITION", "QUOTE"], "colors": colors}
    html = displacy.render(doc, style="ent", options=options, page=True)

    # Menyimpan hasil displaCy dengan format .php
    with open("C:/xampp/htdocs/SKRIPSI/application/views/_ner/ner.php", 'w') as f:
        f.write(html)

    return html, 200, {'Access-Control-Allow-Origin': 'http://localhost',
                                   'Access-Control-Allow-Methods': '*'}

### Fungsi Visualisasi SNA ###
@app.route('/sna/<indikator>/<tahun>', methods=['POST'])
def indikator_json(indikator, tahun):
    mydb, mycursor = connectDB()

    nodes_list = []
    links_list = []
    # triwulan I 2018
    mycursor.execute("""SELECT `nama_tokoh` FROM `output` WHERE `indikator` LIKE '%""" + indikator + """%' 
        AND `tanggal` BETWEEN '""" + tahun + """/1/1' AND '""" + tahun + """/3/31' ORDER BY `tanggal` ASC""")
    records = mycursor.fetchall()
    for row in records:
        nama = row[0]
        x = ast.literal_eval(nama)
        x = [n.strip() for n in x]
        for r in x:
            nodes = OrderedDict()
            nodes['id'] = r
            nodes['group'] = 1
            if nodes not in nodes_list:
                nodes_list.append(nodes)

    for row1 in records:
        tokoh_list = []
        tokoh = row1[0]
        x = ast.literal_eval(tokoh)
        x = [n.strip() for n in x]
        for t in x:
            if t not in tokoh_list:
                tokoh_list.append(t)

        if len(tokoh_list) > 1:
            comb = combinations(tokoh_list, 2)
            for i in list(comb):
                links = OrderedDict()
                links['source'] = i[0]
                links['target'] = i[1]
                links['value'] = 1
                links_list.append(links)

    # triwulan II 2018
    mycursor.execute("""SELECT `nama_tokoh` FROM `output` WHERE `indikator` LIKE '%""" + indikator + """%' 
        AND `tanggal` BETWEEN '""" + tahun + """/4/1' AND '""" + tahun + """/6/30' ORDER BY `tanggal` ASC""")
    records1 = mycursor.fetchall()
    for row in records1:
        nama = row[0]
        x = ast.literal_eval(nama)
        x = [n.strip() for n in x]
        for r in x:
            nodes = OrderedDict()
            nodes['id'] = r
            nodes['group'] = 2
            if nodes not in nodes_list:
                nodes_list.append(nodes)

    for row1 in records1:
        tokoh_list = []
        tokoh = row1[0]
        x = ast.literal_eval(tokoh)
        x = [n.strip() for n in x]
        for t in x:
            if t not in tokoh_list:
                tokoh_list.append(t)

        if len(tokoh_list) > 1:
            comb = combinations(tokoh_list, 2)
            for i in list(comb):
                links = OrderedDict()
                links['source'] = i[0]
                links['target'] = i[1]
                links['value'] = 1
                links_list.append(links)

    # triwulan III 2018
    mycursor.execute("""SELECT `nama_tokoh` FROM `output` WHERE `indikator` LIKE '%""" + indikator + """%' 
        AND `tanggal` BETWEEN '""" + tahun + """/7/1' AND '""" + tahun + """/9/30' ORDER BY `tanggal` ASC""")
    records1 = mycursor.fetchall()
    for row in records1:
        nama = row[0]
        x = ast.literal_eval(nama)
        x = [n.strip() for n in x]
        for r in x:
            nodes = OrderedDict()
            nodes['id'] = r
            nodes['group'] = 3
            if nodes not in nodes_list:
                nodes_list.append(nodes)

    for row1 in records1:
        tokoh_list = []
        tokoh = row1[0]
        x = ast.literal_eval(tokoh)
        x = [n.strip() for n in x]
        for t in x:
            if t not in tokoh_list:
                tokoh_list.append(t)

        if len(tokoh_list) > 1:
            comb = combinations(tokoh_list, 2)
            for i in list(comb):
                links = OrderedDict()
                links['source'] = i[0]
                links['target'] = i[1]
                links['value'] = 1
                links_list.append(links)

    # triwulan IV 2018
    mycursor.execute("""SELECT `nama_tokoh` FROM `output` WHERE `indikator` LIKE '%""" + indikator + """%' 
        AND `tanggal` BETWEEN '""" + tahun + """/10/1' AND '""" + tahun + """/12/31' ORDER BY `tanggal` ASC""")
    records1 = mycursor.fetchall()
    for row in records1:
        nama = row[0]
        x = ast.literal_eval(nama)
        x = [n.strip() for n in x]
        for r in x:
            nodes = OrderedDict()
            nodes['id'] = r
            nodes['group'] = 4
            if nodes not in nodes_list:
                nodes_list.append(nodes)

    for row1 in records1:
        tokoh_list = []
        tokoh = row1[0]
        x = ast.literal_eval(tokoh)
        x = [n.strip() for n in x]
        for t in x:
            if t not in tokoh_list:
                tokoh_list.append(t)

        if len(tokoh_list) > 1:
            comb = combinations(tokoh_list, 2)
            for i in list(comb):
                links = OrderedDict()
                links['source'] = i[0]
                links['target'] = i[1]
                links['value'] = 1
                links_list.append(links)

    # List menggabungkan dictionaries
    graph_list = []
    graph = OrderedDict()
    graph['nodes'] = nodes_list
    graph['links'] = links_list
    graph_list.append(graph)

    # Mengubah list dict ke JSON
    j = js.dumps(graph_list[0])

    # Menyimpan file ke format .json
    with open("C:/xampp/htdocs/SKRIPSI/assets/json/graph_sna.json", 'w') as f:
        f.write(j)

    return j, 200, {'Access-Control-Allow-Origin': 'http://localhost',
                                   'Access-Control-Allow-Methods': '*'}


if __name__ == '__main__':
    app.run(debug=True)