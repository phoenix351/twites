from tqdm import tqdm
import csv
import json
import ast
from sentistrength_id.sentistrength_id import sentistrength
from sentistrength_id_negasi.sentistrength_id_negasi import sentistrength_negasi
from collections import OrderedDict
from koneksi_database import connectDB, set_var

# Untuk mengelompokkan sentimen berita dan sentimen kutipan
def sentiment():
    mydb, mycursor = connectDB()

    # config
    config = dict()
    config["negation"] = True
    config["booster"] = True
    config["ungkapan"] = True
    config["consecutive"] = True
    config["repeated"] = True
    config["emoticon"] = True
    config["question"] = True
    config["exclamation"] = True
    config["punctuation"] = True
    senti = sentistrength(config)
    senti_negasi = sentistrength_negasi(config)
    skor = 0

    # select konten berita hasil prediksi dari database
    sql_berita = """SELECT `id`, `konten_berita`, `kutipan`, `sub_indikator` FROM `temp_output`"""
    mycursor.execute(sql_berita)
    berita = mycursor.fetchall()

    for row in tqdm(berita):
        id = row[0]
        konten = row[1]
        kutipan = row[2]
        indikator = row[3]

        # mendefinisikan indikator negasi
        negasi = [line.replace('\n','') for line in open("indikator_negasi.txt").read().splitlines()]
        x = ast.literal_eval(indikator)
        x = [n.strip() for n in x]

        if len(x) > 0:
            for r in x:
                # jika indikator merupakan indikator negasi
                if r in negasi:
                    senti_konten = senti_negasi.main(konten)
                    sk = senti_konten['kelas']
                    senti_quote = senti_negasi.main(kutipan)
                    sq = senti_quote['kelas']
                    # input to db
                    set_var('sentimen_berita', sk, id)
                    set_var('sentimen_kutipan', sq, id)
                # jika bukan indikator negasi
                else:
                    senti_konten = senti.main(konten)
                    sk = senti_konten['kelas']
                    senti_quote = senti.main(kutipan)
                    sq = senti_quote['kelas']
                    # input to db
                    set_var('sentimen_berita', sk, id)
                    set_var('sentimen_kutipan', sq, id)
        else:
            senti_konten = senti.main(konten)
            sk = senti_konten['kelas']
            senti_quote = senti.main(kutipan)
            sq = senti_quote['kelas']
            # input to db
            set_var('sentimen_berita', sk, id)
            set_var('sentimen_kutipan', sq, id)

# Visualisasi sentimen menggunakan donut chart
def donutchart():
    mydb, mycursor = connectDB()

    # select indicator dari database
    mycursor.execute("SELECT `indicator` FROM `indicator`")
    result = mycursor.fetchall()
    sentimen_list = []
    for row in result:
        ind = row[0]
        sql_pos = mycursor.execute("""SELECT count(*) FROM `output` WHERE `indikator` LIKE '%"""+ind+"""%' AND `sentimen_berita` = 'Positif'""")
        positif = mycursor.fetchone()
        sql_neg = mycursor.execute("""SELECT count(*) FROM `output` WHERE `indikator` LIKE '%"""+ind+"""%' AND `sentimen_berita` = 'Negatif'""")
        negatif = mycursor.fetchone()
        sql_net = mycursor.execute("""SELECT count(*) FROM `output` WHERE `indikator` LIKE '%"""+ind+"""%' AND `sentimen_berita` = 'Netral'""")
        netral = mycursor.fetchone()

        sentimen = OrderedDict()
        sentimen['id'] = ind
        sentimen['Negatif'] = negatif[0]
        sentimen['Netral'] = netral[0]
        sentimen['Positif'] = positif[0]
        sentimen_list.append(sentimen)

        # menyimpan file dengan format .csv
        with open('C:/xampp/htdocs/SKRIPSI/assets/data/data.csv', mode='w', newline='') as f:
            fieldnames = ['id', 'Negatif', 'Netral', 'Positif']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in sentimen_list:
                j = json.dumps(r)
                j = json.loads(j)
                writer.writerow(j)

# Visualisasi zoomable sunburst untuk melihat jumlah indikator secara bertingkat
def zoomable_sunburst():
    mydb, mycursor = connectDB()

    #main_indicator
    mind_list = []
    data1 = mycursor.execute("SELECT * FROM `main_indicator`")
    records1 = mycursor.fetchall()

    for row1 in records1:
        id1 = tuple([row1[0]])

        #indicator
        ind_list = []
        data2 = mycursor.execute("SELECT * FROM `indicator` WHERE `mind_id` = (%s)", id1)
        records2 = mycursor.fetchall()

        for row2 in records2:
            id2 = tuple([row2[0]])

            #sub indicator
            sind_list = []
            data3 = mycursor.execute("SELECT * FROM `sub_indicator` WHERE `ind_id` = (%s)", id2)
            records3 = mycursor.fetchall()

            for row3 in records3:
                sind = OrderedDict()
                sind['name'] = row3[1]
                sind['size'] = row3[4]
                sind_list.append(sind)

            ind = OrderedDict()
            ind['name'] = row2[1]
            ind['children'] = sind_list
            ind_list.append(ind)

        mind = OrderedDict()
        mind['name'] = row1[1]
        mind['children'] = ind_list
        mind_list.append(mind)

    # List menggabungkan semua dictionaries
    indikator_list = []
    indikator = OrderedDict()
    indikator['name'] = 'indikator'
    indikator['children'] = mind_list
    indikator_list.append(indikator)

    # Mengubah list dari dict menjadi JSON
    j = json.dumps(indikator_list[0])

    # Menyimpan file dengan format .json
    with open('C:/xampp/htdocs/SKRIPSI/assets/json/indikator.json', 'w') as f:
        f.write(j)
