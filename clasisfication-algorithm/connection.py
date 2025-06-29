import mysql.connector
from constant import DB
from constant import Program
from typing import Union


def connect():
    mydb = mysql.connector.connect(
        host=DB.DB_HOST, user=DB.DB_USER, password=DB.DB_PASSWORD
    )

    return mydb


def get_cursor(mydb, dictionary: bool = False):
    cursor = mydb.cursor(dictionary=dictionary)

    cursor.execute("CREATE DATABASE IF NOT EXISTS {};".format(DB.DB_NAME))

    cursor.execute("USE {};".format(DB.DB_NAME))

    return cursor


class UserDBConnection:
    def __init__(self, dictionary: bool = False) -> None:
        self.mydb = connect()
        self.cursor = get_cursor(self.mydb, dictionary)
        self.create_table()

    def create_table(self):
        if not Program.run:
            Program.run = True

            # Create iq_categories table
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS iq_categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(50) NOT NULL
            )
            """
            )

            # Create gaya_belajar_categories table
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS gaya_belajar_categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(50) NOT NULL
            )
            """
            )

            # Create personality_categories table
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS personality_categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(50) NOT NULL
            )
            """
            )

            # Create recomendation_categories table
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS recomendation_categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(50) NOT NULL
            )
            """
            )

            # Create data_kotor
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS data_kotor (
                nomor INT PRIMARY KEY,
                kelas VARCHAR(255),
                nama VARCHAR(100),
                agama INT,
                pkn INT,
                bahasa_indo INT,
                matematika INT,
                inggris INT,
                jasmani INT,
                tik INT,
                prakarya INT,
                iq INT,
                jenis_iq VARCHAR(255),
                gaya_belajar VARCHAR(255),
                personality VARCHAR(255),
                rekomendasi_1 VARCHAR(255),
                rekomendasi_2 VARCHAR(255),
                rekomendasi_3 VARCHAR(255)
            )
            """
            )

            # Create data_bersih
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS data_bersih (
                nomor INT PRIMARY KEY,
                agama INT,
                pkn INT,
                bahasa_indo INT,
                matematika INT,
                inggris INT,
                jasmani INT,
                tik INT,
                prakarya INT,
                jenis_iq VARCHAR(255),
                gaya_belajar VARCHAR(255),
                personality VARCHAR(255),
                rekomendasi_1 VARCHAR(255),
                rekomendasi_2 VARCHAR(255),
                rekomendasi_3 VARCHAR(255)
            )
            """
            )

            # Create data_bersih
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS data_uji (
                nomor INT PRIMARY KEY,
                agama INT,
                pkn INT,
                bahasa_indo INT,
                matematika INT,
                inggris INT,
                jasmani INT,
                tik INT,
                prakarya INT,
                jenis_iq VARCHAR(255),
                gaya_belajar VARCHAR(255),
                personality VARCHAR(255),
                rekomendasi_1 VARCHAR(255),
                rekomendasi_2 VARCHAR(255),
                rekomendasi_3 VARCHAR(255)
            )
            """
            )

            # Create transformasi
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS transformasi (
                nomor INT PRIMARY KEY,
                agama INT,
                pkn INT,
                bahasa_indo INT,
                matematika INT,
                inggris INT,
                jasmani INT,
                tik INT,
                prakarya INT,
                jenis_iq INT,
                gaya_belajar INT,
                personality INT,
                rekomendasi_1 INT,
                rekomendasi_2 INT,
                rekomendasi_3 INT
            )
            """
            )

            print("All tables created successfully!")

            self.mydb.commit()
