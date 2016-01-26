# -*- coding: utf-8 -*-

import repository1 
import sqlite3
import unittest

db_path = 'zadanie_AK.db'

class RepositoryTest(unittest.TestCase):

    def setUp(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('DELETE FROM produkt_kredytowy')
        c.execute('DELETE FROM klient')
        c.execute('''INSERT INTO klient (id_klient, nazwa, imie, nazwisko, pesel, miasto ) VALUES(1, "BOM", "Kamil","Nowak",83111223432,"Warszawa")''')
        c.execute('''INSERT INTO produkt_kredytowy (id_klient, nr_wniosku, kwota_kredytu, oprocentowanie) VALUES(1,23456,53456,4.1)''')
        c.execute('''INSERT INTO produkt_kredytowy (id_klient, nr_wniosku, kwota_kredytu, oprocentowanie) VALUES(1,34567,52222,2.1)''')
        c.execute('''INSERT INTO produkt_kredytowy (id_klient, nr_wniosku, kwota_kredytu, oprocentowanie) VALUES(1,31567,52222,2.1)''')
        conn.commit()
        conn.close()

    def tearDown(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('DELETE FROM produkt_kredytowy')
        c.execute('DELETE FROM klient')
        conn.commit()
        conn.close()

    def testGetById(self):
        klient = repository1.KlRepository().getById(1)
        self.assertIsInstance(klient, repository1.Klient, "Objekt nie jest klasy Klient")

    def testGetByIdNotFound(self):
        self.assertEqual(repository1.KlRepository().getById(2),
                None, "Powinno wyjsc None")

    def testGetByIdLen(self):
        self.assertEqual(len(repository1.KlRepository().getById(1).produkt_kredytowy),
                3, "Powinno wyjsc 3")

    def testDeleteNotFound(self):
        self.assertRaises(repository1.RepositoryException,
                repository1.KlRepository().delete(55), 1)



if __name__ == "__main__":
    unittest.main()
