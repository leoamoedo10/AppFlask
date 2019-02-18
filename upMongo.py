import csv
from flask import render_template
from pymongo import MongoClient
from datetime import date

data_atual = date.today()

def upload_to_mongo(filemane):
        input_fd = open('uploads/dados.csv', 'r')
        output_fd = open('uploads/dados(edit).csv', 'w')
        for line in input_fd.readlines():
                line = line.replace(',', '.')
                line = line.replace(';', ',')
                output_fd.write(line)
        input_fd.close()
        output_fd.close()

        csvfile = open('uploads/dados(edit).csv', 'r')
        reader = csv.DictReader(csvfile)
        mongo_client = MongoClient() 
        db = mongo_client.archiveCSV
        db.dados.drop()
        keys = ["Tensao1(V)", "Tensao2(V)", "Tensao3(V)", "Corrente1(A)", "Corrente2(A)", "Corrente3(A)",
                "FP1", "FP2", "FP3", "THDV1(%)", "THDV2(%)", "THDV3(%)", "THDI1(%)", "THDI2(%)" ,"THDI3(%)",
                "P Aparente1(VA)", "P Aparente2(VA)", "P Aparente3(VA)", "P Ativa1(W)", "P Ativa2(W)", "P Ativa3(W)",
                "P Reativa1(VAr)", "P Reativa2(VAr)", "P Reativa3(VAr)", "Freq(Hz)", "Energ Ativa(Wh)",
                "Energ Reat Indutiva (VARh)", "Energ Reat Capacitiva (VArh)", "Energ Ativ Reversa (Wh)", "Energ Aparente (VAh)"]

        for each in reader:
                row={}
                for field in keys:
                        row[field] = each[field]
                db.dados.insert(row)

        return render_template('index.html')