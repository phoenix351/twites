from __future__ import unicode_literals, print_function, division

import re
import spacy
from tqdm import tqdm
import ast
from koneksi_database import connectDB, set_var
from analysis import sentiment, donutchart, zoomable_sunburst

# Memprediksi berita dengan model NER
def predict_NER():
    mydb, mycursor = connectDB()
    sql_insert1 = "INSERT INTO `berita_crawling` SELECT * FROM `temp`"
    mycursor.execute(sql_insert1)
    mydb.commit()
    sql_query = """SELECT * FROM `temp`"""
    mycursor.execute(sql_query)
    berita = mycursor.fetchall()

    #Load model NER masing-masing entitas
    nlp1 = spacy.load('Person')
    nlp2 = spacy.load('Position')
    nlp3 = spacy.load('Organization')
    nlp4 = spacy.load('Location')
    nlp5 = spacy.load('Indicator')
    nlp6 = spacy.load('Quote')

    for row in berita:
        id = row[0]
        sumber = row[1]
        tanggal = row[6]
        judul = row[4]
        konten = row[7]
        konten = re.sub(r"[#/?]", "", konten)

        doc1 = nlp1(konten)
        doc2 = nlp2(konten)
        doc3 = nlp3(konten)
        doc4 = nlp4(konten)
        doc5 = nlp5(konten)
        doc6 = nlp6(konten)

        # mengambil teks hasil prediksi dari label
        person_temp = [(e.text) for e in doc1.ents if e.label_ == 'person']
        position_temp = [(e.text) for e in doc2.ents if e.label_ == 'position']
        organization_temp = [(e.text) for e in doc3.ents if e.label_ == 'organization']
        location_temp = [(e.text) for e in doc4.ents if e.label_ == 'location']
        indicator_temp = [(e.text) for e in doc5.ents if e.label_ == 'indicator']
        quote_temp = [(e.text) for e in doc6.ents if e.label_ == 'quote']

        # memasukkkan hasil prediksi kedalam list
        person=[]
        position=[]
        organization=[]
        location=[]
        indicator=[]
        quote=[]

        for row in person_temp:
            if row not in person:
                person.append(row)

        for row in position_temp:
            if row not in position:
                position.append(row)

        for row in organization_temp:
            if row not in organization:
                organization.append(row)

        for row in location_temp:
            if row not in location:
                location.append(row)

        for row in indicator_temp:
            if row not in indicator:
                indicator.append(row)

        for row in quote_temp:
            if row not in quote:
                quote.append(row)

        # konversi list to str
        person = str(person)
        position = str(position)
        organization = str(organization)
        location = str(location)
        indicator = str(indicator)
        quote = str(quote)

        # insert ke DB
        mydb, mycursor = connectDB()
        sql_insert_query = """INSERT INTO `temp_output`(`id`, `sumber`, `tanggal`, `judul_berita`, `konten_berita`,
                                    `nama_tokoh`, `jabatan`, `organisasi`, `lokasi`, `alias`, `kutipan`)
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        insert_tuple = (id, sumber, tanggal, judul, konten, person, position, organization, location, indicator, quote)
        mycursor.execute(sql_insert_query, insert_tuple)
        # menghapus DB sementara
        mycursor.execute("DELETE FROM `temp` WHERE 1")
        mydb.commit()

        # memanggil fungsi lainnya
        print("Mengklasifikasi alias ke indikator BPS")
        klasifikasi_indikator()  # mengklasifikasikan alias ke indikator BPS
        print("Mengelompokkan Sentimen")
        sentiment()  # mengelompokkan sentimen berita dan sentimen kutipan
        mycursor.execute("INSERT INTO `output` SELECT * FROM `temp_output`")
        mycursor.execute("DELETE FROM `temp_output` WHERE 1")
        mydb.commit()
        print("Menghitung ulang sub_indikator")
        hitung_sub_indikator() # menghitung value dari setiap sub indikator BPS untuk zoomable sunburst
        zoomable_sunburst() # membangun data JSON untuk zoomable sunburst
        donutchart() # membangun data csv untuk donut chart
        
        # print("Update db tokoh_indikator dan org_indikator")
        # sen = ['Negatif', 'Netral', 'Positif']
        # for sentimen in sen:
        #     tokoh(sentimen) # update db tokoh_indikator
        # for sentimen in sen:
        #     organisasi(sentimen) # update db org_indikator

def klasifikasi_indikator():
    mydb, mycursor = connectDB()

    sql_alias_id = """SELECT `alias`, `id` FROM `temp_output`"""
    mycursor.execute(sql_alias_id)
    rows = mycursor.fetchall()

    sql = "SELECT `sub_indicator`, `ind_id` FROM `sub_indicator` WHERE `alias` LIKE lower(%s)"
    sql2 = "SELECT `indicator` FROM `indicator` WHERE `ind_id` = (%s)"
    for row in tqdm(rows):
        sub_ind = []
        ind_id = []
        ind = []
        alias = row[0]
        id = row[1]

        x = ast.literal_eval(alias)
        x = [n.strip() for n in x]
        for r in x:
            var = "%'" + r + "'%"
            mycursor.execute(sql, (var,))
            y = mycursor.fetchone()
            if y is not None:
                if y[0] not in sub_ind:
                    sub_ind.append(y[0])
                if y[1] not in ind_id:
                    ind_id.append(y[1])
        sub_ind = str(sub_ind)
        set_var('sub_indikator', sub_ind, id)

        for id1 in ind_id:
            mycursor.execute(sql2, (id1,))
            y = mycursor.fetchone()
            if y is not None:
                if y[0] not in ind:
                    ind.append(y[0])
        ind = str(ind)
        set_var('indikator', ind, id)

def hitung_sub_indikator():
    mydb, mycursor = connectDB()

    sql = "SELECT `sub_indicator` FROM `sub_indicator`"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in tqdm(result):
        sind = row[0]
        mycursor.execute("""SELECT COUNT(*) FROM `output` WHERE `sub_indikator` LIKE '%"""+sind+"""%'""")
        result = mycursor.fetchall()

        for row in result:
            value= row[0]
            sql_update = """UPDATE `sub_indicator` SET `value` = (%s) WHERE `sub_indicator` LIKE '%"""+sind+"""%'"""
            mycursor.execute(sql_update, (value,))
            mydb.commit()

# Untuk mengetahui Top 5 Tokoh
def tokoh(sen):
    mydb, mycursor = connectDB()
    mycursor.execute("DELETE FROM `tokoh_indikator` WHERE 1")
    mydb.commit()
    sql = "SELECT `indicator` FROM `indicator`"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in tqdm(result):
        ind = row[0]
        mycursor.execute("""SELECT `nama_tokoh` FROM `output` WHERE `indikator` LIKE '%""" + ind + """%' AND `sentimen_kutipan` = '"""+ sen + """'""")
        result = mycursor.fetchall()

        if ind == 'PDB/PDRB':
            ind = 'PDB'

        total_tokoh = []
        list_tokoh = []

        for row in result:
            tokoh = row[0]
            x = ast.literal_eval(tokoh)
            x = [n.strip() for n in x]

            for y in x:
                list_tokoh.append(y)
                if y not in total_tokoh:
                    total_tokoh.append(y)

        for row in total_tokoh:
            jumlah = list_tokoh.count(row)

            sql = """INSERT INTO `tokoh_indikator`(`indikator`, `sentimen`, `nama_tokoh`, `jumlah`) VALUES (%s,%s,%s,%s)"""

            insert_tuple = (ind, sen, row, jumlah)
            mycursor.execute(sql, insert_tuple)
            # menghilangkan tokoh BPS
            del_tokoh = ['Suhariyanto', 'Suharyanto', 'Kecuk', 'Suryamin','Sasmito']
            for r in del_tokoh:
                mycursor.execute("""DELETE FROM `tokoh_indikator` WHERE `nama_tokoh` LIKE '%"""+r+"""%'""")
                mydb.commit()

# Untuk mengetahui Top 5 Organisasi
def organisasi(sen):
    mydb, mycursor = connectDB()
    mycursor.execute("DELETE FROM `org_indikator` WHERE 1")
    mydb.commit()
    sql = "SELECT `indicator` FROM `indicator`"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in tqdm(result):
        ind = row[0]
        mycursor.execute("""SELECT `organisasi` FROM `output` WHERE `indikator` LIKE '%""" + ind + """%' AND `sentimen_kutipan` = '"""+ sen + """'""")
        result = mycursor.fetchall()

        if ind == 'PDB/PDRB':
            ind = 'PDB'

        total_org = []
        list_org = []

        for row in result:
            org = row[0]
            x = ast.literal_eval(org)
            x = [n.strip() for n in x]
            for y in x:
                list_org.append(y)
                if y not in total_org:
                    total_org.append(y)

        for row in total_org:
            jumlah = list_org.count(row)

            sql = """INSERT INTO `org_indikator`(`indikator`, `sentimen`, `organisasi`, `jumlah`) VALUES (%s,%s,%s,%s)"""

            insert_tuple = (ind, sen, row, jumlah)
            mycursor.execute(sql, insert_tuple)
            # menghilangkan organisasi BPS
            del_org = ['BPS', 'Badan Pusat Statistik']
            for r in del_org:
                mycursor.execute("""DELETE FROM `org_indikator` WHERE `organisasi` LIKE '%""" + r + """%'""")
                mydb.commit()
