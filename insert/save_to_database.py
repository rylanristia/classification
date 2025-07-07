import csv
from connection import UserDBConnection
import pandas as pd
import re


def symbol_remover(text):
    return re.sub(r"[^a-z0-9\s]", " ", text)


def has_content(table):
    conn = UserDBConnection()

    conn.cursor.execute("SELECT * FROM {};".format(table))

    x = [i for i in conn.cursor]

    if len(x) == 0:
        return False

    return True


def save_kategori():
    conn = UserDBConnection()

    try:
        # Data untuk iq_categories
        iq_categories = [
            "Diatas Rata-rata",
            "Dibawah Rata-rata",
            "Rata-rata",
            "Rendah",
            "Tinggi",
            "Sangat Tinggi",
        ]

        # Data untuk gaya_belajar_categories
        gaya_belajar = ["Visual", "Auditori", "Kinestetik"]

        # Data untuk personality_categories
        personalities = [
            "ENFJ",
            "ENFP",
            "ENTJ",
            "ENTP",
            "ESFJ",
            "ESFP",
            "ESTJ",
            "ESTP",
            "INFJ",
            "INFP",
            "INTJ",
            "INTP",
            "ISFJ",
            "ISFP",
            "ISTJ",
            "ISTP",
        ]

        # Data untuk recomendation_categories
        recommendations = [
            "Antropologi",
            "Bahasa Asing",
            "Biologi",
            "Ekonomi",
            "Fisika",
            "Geografi",
            "Informatika",
            "Kimia",
            "Matematika",
            "Sejarah",
            "Sosiologi",
        ]

        # Insert ke iq_categories
        for category in iq_categories:
            conn.cursor.execute(
                "INSERT INTO iq_categories (category) VALUES (%s)", (category,)
            )

        # Insert ke gaya_belajar_categories
        for category in gaya_belajar:
            conn.cursor.execute(
                "INSERT INTO gaya_belajar_categories (category) VALUES (%s)",
                (category,),
            )

        # Insert ke personality_categories
        for category in personalities:
            conn.cursor.execute(
                "INSERT INTO personality_categories (category) VALUES (%s)", (category,)
            )

        # Insert ke recomendation_categories
        for category in recommendations:
            conn.cursor.execute(
                "INSERT INTO recomendation_categories (category) VALUES (%s)",
                (category,),
            )

        conn.mydb.commit()
        print("Data berhasil dimasukkan ke semua tabel!")

    finally:
        if hasattr(conn, "cursor") and conn.cursor:
            conn.cursor.close()
        if hasattr(conn, "close") and callable(getattr(conn, "close")):
            conn.mydb.close()


def save_data_kotor():
    conn = UserDBConnection()

    xls = pd.ExcelFile("xlsx/datasets.xlsx")
    sheetx = xls.parse(0)
    sheetx = sheetx.where(
        pd.notnull(sheetx), None
    )  # Use None instead of "null" for NULL values

    for i in range(len(sheetx)):
        # Convert numpy types to native Python types
        nomor = (
            int(sheetx["nomor"].iloc[i])
            if pd.notnull(sheetx["nomor"].iloc[i])
            else None
        )
        kelas = (
            str(sheetx["kelas"].iloc[i])
            if pd.notnull(sheetx["kelas"].iloc[i])
            else None
        )
        nama = (
            str(sheetx["nama"].iloc[i]) if pd.notnull(sheetx["nama"].iloc[i]) else None
        )
        agama = (
            int(sheetx["agama"].iloc[i])
            if pd.notnull(sheetx["agama"].iloc[i])
            else None
        )
        pkn = int(sheetx["pkn"].iloc[i]) if pd.notnull(sheetx["pkn"].iloc[i]) else None
        bahasa_indo = (
            int(sheetx["bahasa_indo"].iloc[i])
            if pd.notnull(sheetx["bahasa_indo"].iloc[i])
            else None
        )
        matematika = (
            int(sheetx["matematika"].iloc[i])
            if pd.notnull(sheetx["matematika"].iloc[i])
            else None
        )
        inggris = (
            int(sheetx["inggris"].iloc[i])
            if pd.notnull(sheetx["inggris"].iloc[i])
            else None
        )
        jasmani = (
            int(sheetx["jasmani"].iloc[i])
            if pd.notnull(sheetx["jasmani"].iloc[i])
            else None
        )
        tik = int(sheetx["tik"].iloc[i]) if pd.notnull(sheetx["tik"].iloc[i]) else None
        prakarya = (
            int(sheetx["prakarya"].iloc[i])
            if pd.notnull(sheetx["prakarya"].iloc[i])
            else None
        )
        iq = int(sheetx["iq"].iloc[i]) if pd.notnull(sheetx["iq"].iloc[i]) else None
        jenis_iq = (
            str(sheetx["jenis_iq"].iloc[i])
            if pd.notnull(sheetx["jenis_iq"].iloc[i])
            else None
        )
        gaya_belajar = (
            str(sheetx["gaya_belajar"].iloc[i])
            if pd.notnull(sheetx["gaya_belajar"].iloc[i])
            else None
        )
        personality = (
            str(sheetx["personality"].iloc[i])
            if pd.notnull(sheetx["personality"].iloc[i])
            else None
        )
        rekomendasi_1 = (
            str(sheetx["rekomendasi_1"].iloc[i])
            if pd.notnull(sheetx["rekomendasi_1"].iloc[i])
            else None
        )
        rekomendasi_2 = (
            str(sheetx["rekomendasi_2"].iloc[i])
            if pd.notnull(sheetx["rekomendasi_2"].iloc[i])
            else None
        )
        rekomendasi_3 = (
            str(sheetx["rekomendasi_3"].iloc[i])
            if pd.notnull(sheetx["rekomendasi_3"].iloc[i])
            else None
        )

        # Use %s for all placeholders (MySQL connector will handle type conversion)
        query = """
        INSERT INTO data_kotor(
            nomor, kelas, nama, agama, pkn, bahasa_indo, matematika, inggris,
            jasmani, tik, prakarya, iq, jenis_iq, gaya_belajar, personality,
            rekomendasi_1, rekomendasi_2, rekomendasi_3
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            nomor,
            kelas,
            nama,
            agama,
            pkn,
            bahasa_indo,
            matematika,
            inggris,
            jasmani,
            tik,
            prakarya,
            iq,
            jenis_iq,
            gaya_belajar,
            personality,
            rekomendasi_1,
            rekomendasi_2,
            rekomendasi_3,
        )

        conn.cursor.execute(query, values)

    conn.mydb.commit()


def save_data_bersih():
    conn = UserDBConnection()

    xls = pd.ExcelFile("xlsx/datasets.xlsx")
    sheetx = xls.parse(0)
    sheetx = sheetx.where(
        pd.notnull(sheetx), None
    )  # Use None instead of "null" for NULL values

    for i in range(len(sheetx)):
        # Convert numpy types to native Python types
        nomor = (
            int(sheetx["nomor"].iloc[i])
            if pd.notnull(sheetx["nomor"].iloc[i])
            else None
        )
        agama = (
            int(sheetx["agama"].iloc[i])
            if pd.notnull(sheetx["agama"].iloc[i])
            else None
        )
        pkn = int(sheetx["pkn"].iloc[i]) if pd.notnull(sheetx["pkn"].iloc[i]) else None
        bahasa_indo = (
            int(sheetx["bahasa_indo"].iloc[i])
            if pd.notnull(sheetx["bahasa_indo"].iloc[i])
            else None
        )
        matematika = (
            int(sheetx["matematika"].iloc[i])
            if pd.notnull(sheetx["matematika"].iloc[i])
            else None
        )
        inggris = (
            int(sheetx["inggris"].iloc[i])
            if pd.notnull(sheetx["inggris"].iloc[i])
            else None
        )
        jasmani = (
            int(sheetx["jasmani"].iloc[i])
            if pd.notnull(sheetx["jasmani"].iloc[i])
            else None
        )
        tik = int(sheetx["tik"].iloc[i]) if pd.notnull(sheetx["tik"].iloc[i]) else None
        prakarya = (
            int(sheetx["prakarya"].iloc[i])
            if pd.notnull(sheetx["prakarya"].iloc[i])
            else None
        )
        jenis_iq = (
            str(sheetx["jenis_iq"].iloc[i])
            if pd.notnull(sheetx["jenis_iq"].iloc[i])
            else None
        )
        gaya_belajar = (
            str(sheetx["gaya_belajar"].iloc[i])
            if pd.notnull(sheetx["gaya_belajar"].iloc[i])
            else None
        )
        personality = (
            str(sheetx["personality"].iloc[i])
            if pd.notnull(sheetx["personality"].iloc[i])
            else None
        )
        rekomendasi_1 = (
            str(sheetx["rekomendasi_1"].iloc[i])
            if pd.notnull(sheetx["rekomendasi_1"].iloc[i])
            else None
        )
        rekomendasi_2 = (
            str(sheetx["rekomendasi_2"].iloc[i])
            if pd.notnull(sheetx["rekomendasi_2"].iloc[i])
            else None
        )
        rekomendasi_3 = (
            str(sheetx["rekomendasi_3"].iloc[i])
            if pd.notnull(sheetx["rekomendasi_3"].iloc[i])
            else None
        )

        # Use %s for all placeholders
        query = """
        INSERT INTO data_bersih(
            nomor, agama, pkn, bahasa_indo, matematika, inggris,
            jasmani, tik, prakarya, jenis_iq, gaya_belajar, personality,
            rekomendasi_1, rekomendasi_2, rekomendasi_3
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            nomor,
            agama,
            pkn,
            bahasa_indo,
            matematika,
            inggris,
            jasmani,
            tik,
            prakarya,
            jenis_iq,
            gaya_belajar,
            personality,
            rekomendasi_1,
            rekomendasi_2,
            rekomendasi_3,
        )

        conn.cursor.execute(query, values)

    conn.mydb.commit()

def save_data_uji():
    conn = UserDBConnection()
    cursor = conn.cursor

    data_uji = [
        (1, 62, 79, 98, 95, 51, 70, 79, 69, "Rata-rata", "Kinestetik", "ISTP", "Ekonomi", "Sosiologi", "Sejarah"),
        (2, 99, 66, 61, 69, 87, 57, 85, 63, "Rendah", "Visual", "INFP", "Sosiologi", "Sejarah", "Antropologi"),
        (3, 58, 60, 79, 64, 50, 80, 97, 51, "Rendah", "Auditori", "ESTP", "Antropologi", "Ekonomi", "Sosiologi"),
        (4, 96, 72, 93, 93, 66, 59, 73, 92, "Rendah", "Auditori", "ISFP", "Antropologi", "Sosiologi", "Ekonomi"),
        (5, 51, 64, 99, 62, 69, 65, 88, 91, "Dibawah Rata-rata", "Visual", "ESTJ", "Ekonomi", "Sosiologi", "Geografi"),
        (6, 89, 59, 76, 82, 73, 64, 92, 76, "Rata-rata", "Visual", "ESTJ", "Ekonomi", "Sosiologi", "Geografi"),
        (7, 76, 52, 75, 53, 92, 52, 88, 52, "Diatas Rata-rata", "Visual", "ESFJ", "Biologi", "Kimia", "Geografi"),
        (8, 51, 51, 64, 93, 90, 67, 95, 56, "Rata-rata", "Visual", "ISTJ", "Biologi", "Kimia", "Informatika"),
        (9, 93, 81, 83, 61, 97, 58, 58, 84, "Rendah", "Visual", "ENTJ", "Antropologi", "Sosiologi", "Geografi"),
        (10, 71, 88, 86, 94, 62, 61, 95, 98, "Dibawah Rata-rata", "Auditori", "ENTP", "Geografi", "Ekonomi", "Sosiologi"),
        (11, 78, 77, 71, 52, 56, 53, 60, 87, "Dibawah Rata-rata", "Visual", "ESFP", "Geografi", "Sosiologi", "Sejarah"),
        (12, 66, 83, 95, 57, 100, 50, 98, 95, "Dibawah Rata-rata", "Visual", "ISTJ", "Ekonomi", "Sosiologi", "Sejarah"),
        (13, 96, 72, 73, 89, 75, 96, 79, 72, "Rata-rata", "Kinestetik", "ESFJ", "Biologi", "Kimia", "Sosiologi"),
        (14, 68, 65, 96, 84, 71, 80, 66, 92, "Rata-rata", "Auditori", "ESTJ", "Ekonomi", "Sosiologi", "Matematika"),
        (15, 77, 97, 69, 94, 96, 66, 58, 63, "Sangat Rendah", "Kinestetik", "ENFJ", "Biologi", "Bahasa Asing", "Informatika"),
        (16, 97, 72, 67, 82, 100, 81, 63, 93, "Dibawah Rata-rata", "Visual", "ESTP", "Antropologi", "Sosiologi", "Ekonomi"),
        (17, 75, 97, 71, 58, 84, 78, 89, 75, "Rata-rata", "Kinestetik", "ESFP", "Ekonomi", "Sosiologi", "Geografi"),
        (18, 69, 50, 89, 65, 81, 95, 51, 65, "Rata-rata", "Visual", "ENFJ", "Antropologi", "Ekonomi", "Geografi"),
        (19, 60, 85, 68, 69, 70, 58, 70, 64, "Diatas Rata-rata", "Visual", "ISTJ", "Antropologi", "Sosiologi", "Biologi"),
        (20, 92, 82, 60, 60, 65, 87, 61, 54, "Rata-rata", "Visual", "ENTJ", "Ekonomi", "Sosiologi", "Geografi")
    ]

    query = """
        INSERT INTO data_uji (
            nomor, agama, pkn, bahasa_indo, matematika, inggris, jasmani, tik, prakarya,
            jenis_iq, gaya_belajar, personality,
            rekomendasi_1, rekomendasi_2, rekomendasi_3
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for row in data_uji:
        cursor.execute(query, row)

    conn.mydb.commit()

def remove_all_data():
    conn = UserDBConnection()

    conn.cursor.execute(
        """
        DELETE FROM iq_categories
        """
    )

    conn.cursor.execute(
        """
        DELETE FROM gaya_belajar_categories
        """
    )

    conn.cursor.execute(
        """
        DELETE FROM personality_categories
        """
    )

    conn.cursor.execute(
        """
        DELETE FROM recomendation_categories
        """
    )

    conn.cursor.execute(
        """
        DELETE FROM data_kotor
        """
    )

    conn.cursor.execute(
        """
        DELETE FROM data_bersih
        """
    )

    conn.cursor.execute(
        """
        DELETE FROM data_uji
        """
    )

    conn.cursor.execute(
        """
        DELETE FROM transformasi
        """
    )

    conn.mydb.commit()

def save_all_data():

    remove_all_data()

    save_kategori()
    print("Berhasil menyimpan data kategori")

    if not has_content("data_bersih"):
        save_data_bersih()
        print("Berhasil menyimpan data bersih")

    if not has_content("data_kotor"):
        save_data_kotor()
        print("Berhasil menyimpan data kotor")

    save_data_uji()
    print("Berhasil menyimpan data uji")
    

