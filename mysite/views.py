from django.http import request
from django.shortcuts import render
from connection import UserDBConnection
from insert.save_to_database import save_all_data
import math
from collections import Counter
import numpy as np
from sklearn.tree import DecisionTreeClassifier


def dashboard(request):

    if request.POST.get("save-data"):
        save_all_data()
        result = "COMPLETE NIH PROSESNYA"
    else:
        result = ""

    context = {"result": result}

    return render(request, "dashboard.html", context)


def datakotor(request):
    conn = UserDBConnection(dictionary = True)

    querry = "SELECT * FROM data_kotor"
    conn.cursor.execute(querry)
    datakotor = [i for i in conn.cursor]

    context = {
        'datakotor':datakotor,
    }

    return render(request, "datakotor.html", context)


def cleansingResult(request):
    conn = UserDBConnection(dictionary = True)

    querry = "SELECT * FROM data_bersih"
    conn.cursor.execute(querry)
    databersih = [i for i in conn.cursor]

    context = {
        'databersih':databersih,
    }

    return render(request, "cleansing-result.html", context)

def nilai_to_kategori(nilai):
    if nilai >= 91:
        return 1
    elif nilai >= 81:
        return 2
    elif nilai >= 71:
        return 3
    else:
        return 4

def get_category_id( table, value):
    conn = UserDBConnection(dictionary=True)
    conn.cursor.execute(f"SELECT id FROM {table} WHERE category = %s", [value])
    result = conn.cursor.fetchone()
    return result['id'] if result else None

def transformasi(request):
    conn = UserDBConnection(dictionary=True)

    if request.method == "POST":
        # Ambil data dari data_bersih
        query = "SELECT * FROM data_bersih"
        conn.cursor.execute(query)
        data_bersih = [row for row in conn.cursor]

        for row in data_bersih:
            nomor = row['nomor']  # pastikan kolom ini ada di data_bersih

            # Transform nilai pelajaran
            agama = nilai_to_kategori(row['agama'])
            pkn = nilai_to_kategori(row['pkn'])
            bahasa_indo = nilai_to_kategori(row['bahasa_indo'])
            matematika = nilai_to_kategori(row['matematika'])
            inggris = nilai_to_kategori(row['inggris'])
            jasmani = nilai_to_kategori(row['jasmani'])
            tik = nilai_to_kategori(row['tik'])
            prakarya = nilai_to_kategori(row['prakarya'])

            # Ambil ID kategori
            jenis_iq = get_category_id('iq_categories', row['jenis_iq'])
            gaya_belajar = get_category_id('gaya_belajar_categories', row['gaya_belajar'])
            personality = get_category_id('personality_categories', row['personality'])
            rekomendasi_1 = get_category_id('recomendation_categories', row['rekomendasi_1'])
            rekomendasi_2 = get_category_id('recomendation_categories', row['rekomendasi_2'])
            rekomendasi_3 = get_category_id('recomendation_categories', row['rekomendasi_3'])

            # Simpan ke tabel transformasi
            insert_query = """
                INSERT INTO transformasi (
                    nomor, agama, pkn, bahasa_indo, matematika, inggris, jasmani, tik, prakarya,
                    jenis_iq, gaya_belajar, personality,
                    rekomendasi_1, rekomendasi_2, rekomendasi_3
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            conn.cursor.execute(insert_query, (
                nomor, agama, pkn, bahasa_indo, matematika, inggris, jasmani, tik, prakarya,
                jenis_iq, gaya_belajar, personality,
                rekomendasi_1, rekomendasi_2, rekomendasi_3
            ))

        conn.mydb.commit()

    # Ambil hasil transformasi
    conn.cursor.execute("""
        SELECT * from TRANSFORMASI
    """)
    hasil_transformasi = [row for row in conn.cursor]
    columns = hasil_transformasi[0].keys() if hasil_transformasi else []

    return render(request, "transformasi.html", {
        'hasil_transformasi': hasil_transformasi,
        'columns': columns
    })

def transform_data_uji(data_uji_raw):
    transformed = []

    for row in data_uji_raw:
        try:
            transformed.append({
                'agama': nilai_to_kategori(row['agama']),
                'pkn': nilai_to_kategori(row['pkn']),
                'bahasa_indo': nilai_to_kategori(row['bahasa_indo']),
                'matematika': nilai_to_kategori(row['matematika']),
                'inggris': nilai_to_kategori(row['inggris']),
                'jasmani': nilai_to_kategori(row['jasmani']),
                'tik': nilai_to_kategori(row['tik']),
                'prakarya': nilai_to_kategori(row['prakarya']),
                'jenis_iq': get_category_id('iq_categories', row['jenis_iq']),
                'gaya_belajar': get_category_id('gaya_belajar_categories', row['gaya_belajar']),
                'personality': get_category_id('personality_categories', row['personality']),
            })
        except Exception as e:
            print("Transformasi gagal untuk row:", row, "karena", e)
            continue
        

    return transformed

def safe_cast(val, default=0):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def get_category_id(table, value):
    conn = UserDBConnection(dictionary=True)

    conn.cursor.execute(f"SELECT id FROM {table} WHERE category = %s", (value,))
    result = conn.cursor.fetchone()
    return result['id'] if result else 0

def hitung_akurasi(data_uji_raw, hasil_prediksi):
    total = 0
    benar = 0
    akurasi_per_record = []

    for data, pred in zip(data_uji_raw, hasil_prediksi):
        match = 0
        if data['rekomendasi_1'] == pred['rekomendasi_1']:
            match += 1
        if data['rekomendasi_2'] == pred['rekomendasi_2']:
            match += 1
        if data['rekomendasi_3'] == pred['rekomendasi_3']:
            match += 1

        akurasi = (match / 3) * 100
        akurasi_per_record.append(akurasi)

        benar += match
        total += 3  # karena setiap record ada 3 prediksi

    akurasi_total = (benar / total) * 100 if total > 0 else 0
    return akurasi_per_record, akurasi_total


def klasifikasi(request):
    conn = UserDBConnection(dictionary=True)

    if request.method == 'POST':
        # Ambil semua data uji
        conn.cursor.execute("SELECT * FROM data_uji")
        data_uji_raw = [row for row in conn.cursor]

        data_uji = transform_data_uji(data_uji_raw)

        if 'knn_button' in request.POST:
            knn_results = knn_predict_raw(data_uji)
            akurasi_per_record, akurasi_total = hitung_akurasi(data_uji_raw, knn_results)
            context = {
                'rows': zip(data_uji_raw, knn_results, akurasi_per_record),
                'method': 'KNN',
                'akurasi_total': akurasi_total,
            }
            return render(request, "klasifikasi.html", context)

        elif 'c45_button' in request.POST:
            c45_results = c45_predict_raw(data_uji)
            akurasi_per_record, akurasi_total = hitung_akurasi(data_uji_raw, c45_results)
            context = {
                'rows': zip(data_uji_raw, c45_results, akurasi_per_record),
                'method': 'C4.5',
                'akurasi_total': akurasi_total,
            }
            return render(request, "klasifikasi.html", context)

    return render(request, "klasifikasi.html")

def knn_predict_raw(data_uji_list, k=3):
    conn = UserDBConnection(dictionary=True)
    # Ambil data latih (transformasi)
    conn.cursor.execute("""
        SELECT 
            agama, pkn, bahasa_indo, matematika, inggris, 
            jasmani, tik, prakarya, jenis_iq, gaya_belajar, 
            personality, rekomendasi_1, rekomendasi_2, rekomendasi_3
        FROM transformasi
    """)
    data_latih = [row for row in conn.cursor]

    # Mapping rekomendasi
    conn.cursor.execute("SELECT * FROM recomendation_categories")
    rekomendasi_map = {row['category']: row['id'] for row in conn.cursor}
    rekomendasi_inv_map = {v: k for k, v in rekomendasi_map.items()}

    results = []

    for data_uji in data_uji_list:
        # Hitung jarak untuk setiap data latih
        distances = []
        for data in data_latih:
            try:
                numerical_distance = math.sqrt(
                    (data['agama'] - data_uji['agama'])**2 +
                    (data['pkn'] - data_uji['pkn'])**2 +
                    (data['bahasa_indo'] - data_uji['bahasa_indo'])**2 +
                    (data['matematika'] - data_uji['matematika'])**2 +
                    (data['inggris'] - data_uji['inggris'])**2 +
                    (data['jasmani'] - data_uji['jasmani'])**2 +
                    (data['tik'] - data_uji['tik'])**2 +
                    (data['prakarya'] - data_uji['prakarya'])**2 +
                    (data['jenis_iq'] - data_uji['jenis_iq'])**2 +
                    (data['gaya_belajar'] - data_uji['gaya_belajar'])**2 +
                    (data['personality'] - data_uji['personality'])**2
                )

                total_distance = numerical_distance
                distances.append((total_distance, data))
            except Exception as e:
                print("Error menghitung jarak:", e)
                continue

        # Ambil k tetangga terdekat
        distances.sort(key=lambda x: x[0])
        neighbors = distances[:k]

        def most_common(lst):
            return Counter(lst).most_common(1)[0][0] if lst else 'Tidak diketahui'

        try:
            # Ambil rekomendasi mayoritas dari tetangga
            rek1 = [rekomendasi_inv_map[neighbor[1]['rekomendasi_1']] for neighbor in neighbors]
            rek2 = [rekomendasi_inv_map[neighbor[1]['rekomendasi_2']] for neighbor in neighbors]
            rek3 = [rekomendasi_inv_map[neighbor[1]['rekomendasi_3']] for neighbor in neighbors]

            hasil = {
                'rekomendasi_1': most_common(rek1),
                'rekomendasi_2': most_common(rek2),
                'rekomendasi_3': most_common(rek3),
            }
        except Exception as e:
            print("Error mengambil rekomendasi mayoritas:", e)
            hasil = {
                'rekomendasi_1': 'Tidak diketahui',
                'rekomendasi_2': 'Tidak diketahui',
                'rekomendasi_3': 'Tidak diketahui',
            }
        results.append(hasil)

    return results

def c45_predict_raw(data_uji_list):
    conn = UserDBConnection(dictionary=True)
    cursor = conn.cursor

    # Ambil data latih
    cursor.execute("""
        SELECT 
            agama, pkn, bahasa_indo, matematika, inggris, 
            jasmani, tik, prakarya, jenis_iq, gaya_belajar, 
            personality, rekomendasi_1, rekomendasi_2, rekomendasi_3
        FROM transformasi
    """)
    data_latih = [row for row in cursor]

    # Mapping rekomendasi
    cursor.execute("SELECT * FROM recomendation_categories")
    rekomendasi_map = {row['category']: row['id'] for row in cursor}
    rekomendasi_inv_map = {v: k for k, v in rekomendasi_map.items()}

    # Data training
    X = []
    y_rek1, y_rek2, y_rek3 = [], [], []
    for d in data_latih:
        X.append([
            d['agama'], d['pkn'], d['bahasa_indo'], d['matematika'], d['inggris'],
            d['jasmani'], d['tik'], d['prakarya'],
            d['jenis_iq'], d['gaya_belajar'], d['personality']
        ])
        y_rek1.append(d['rekomendasi_1'])
        y_rek2.append(d['rekomendasi_2'])
        y_rek3.append(d['rekomendasi_3'])

    # Train model
    clf1 = DecisionTreeClassifier(criterion='entropy').fit(X, y_rek1)
    clf2 = DecisionTreeClassifier(criterion='entropy').fit(X, y_rek2)
    clf3 = DecisionTreeClassifier(criterion='entropy').fit(X, y_rek3)

    results = []
    for data in data_uji_list:
        xuji = [[
            data['agama'], data['pkn'], data['bahasa_indo'], data['matematika'], data['inggris'],
            data['jasmani'], data['tik'], data['prakarya'],
            data['jenis_iq'], data['gaya_belajar'], data['personality']
        ]]

        pred1 = clf1.predict(xuji)[0]
        pred2 = clf2.predict(xuji)[0]
        pred3 = clf3.predict(xuji)[0]

        hasil = {
            'rekomendasi_1': rekomendasi_inv_map.get(pred1, 'Tidak diketahui'),
            'rekomendasi_2': rekomendasi_inv_map.get(pred2, 'Tidak diketahui'),
            'rekomendasi_3': rekomendasi_inv_map.get(pred3, 'Tidak diketahui'),
        }
        results.append(hasil)

    return results
