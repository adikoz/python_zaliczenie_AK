# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime

db_path = 'zadanie_AK.db'

class RepositoryException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors


class Klient():

    def __init__(self, id_klient, nazwa, imie, nazwisko, pesel, miasto, produkt_kredytowy=[]):
        self.id_klient = id_klient
        self.nazwa = nazwa
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.miasto = miasto
        self.produkt_kredytowy = produkt_kredytowy

    def __repr__(self):
        return "<klient('%s', '%s', '%s', '%s','%s','%s','%s', )>" % (
                    self.id_klient, self.nazwa, self.imie, self.nazwisko, str(self.pesel), self.miasto, self.produkt_kredytowy
                )


class Produkt_kredytowy():

    def __init__(self, id_klient, nr_wniosku, kwota_kredytu, oprocentowanie):
        self.id_klient = id_klient
        self.nr_wniosku = nr_wniosku
        self.kwota_kredytu = kwota_kredytu
        self.oprocentowanie = oprocentowanie

    def __repr__(self):
        return "<( nr_wniosku='%s', kwota='%s', oprocentowanie='%s','%s' )>" % (
                   str(self.nr_wniosku), str(self.kwota_kredytu), str(self.oprocentowanie), self.id_klient
                )


#
# Klasa bazowa repozytorium
#
class Repository():
    def __init__(self):
        try:
            self.conn = self.get_connection()
        except Exception as e:
            raise RepositoryException('GET CONNECTION:', *e.args)
        self._complete = False

    # wejście do with ... as ...
    def __enter__(self):
        return self

    # wyjście z with ... as ...
    def __exit__(self, type_, value, traceback):
        self.close()

    def complete(self):
        self._complete = True

    def get_connection(self):
        return sqlite3.connect(db_path)

    def close(self):
        if self.conn:
            try:
                if self._complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                raise RepositoryException(*e.args)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    raise RepositoryException(*e.args)

#
# repozytorium obiektow
#
class KlRepository(Repository):

    def add(self, klient):
       
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO klient ( id_klient, nazwa, imie, nazwisko, pesel, miasto) VALUES(?, ?, ?, ?, ?, ?)',
                        (klient.id_klient, klient.nazwa, klient.imie, klient.nazwisko, klient.pesel, klient.miasto)
                    )

            if klient.produkt_kredytowy:
                for produkt_kredytowy in klient.produkt_kredytowy:
                    try:
                        c.execute('INSERT INTO produkt_kredytowy (nr_wniosku, kwota_kredytu, oprocentowanie,id_klient) VALUES(?,?,?,?)',
                                        (produkt_kredytowy.nr_wniosku, produkt_kredytowy.kwota_kredytu, produkt_kredytowy.oprocentowanie, klient.id_klient)
                                )

                    except Exception as e:
                        raise RepositoryException('error adding: %s, to komunikat bledu: %s' %
                                                    (str(klient), e)
                                                )

        except Exception as e:
             raise RepositoryException('error adding klient %s' % str(e))


    def delete(self, id_klient):
       
        try:
            c = self.conn.cursor()
            # usuń klienta
            c.execute('DELETE FROM klient WHERE id_klient=?', (id_klient,))
            # usuń kredyt
            c.execute('DELETE FROM produkt_kredytowy WHERE id_klient=?', (id_klient,))

        except Exception as e:
            raise RepositoryException('error deleting %s' % str(e))

    def getById(self, id):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM klient WHERE id_klient=?", (id,))
            row = c.fetchone()
            pk=[]
            if row == None:
                klient = None
            else:
                klient = Klient(id_klient=id, nazwa=row[1], imie=row[2], nazwisko=row[3], pesel=row[4], miasto=row[5], produkt_kredytowy=[])
                c.execute("SELECT * FROM produkt_kredytowy WHERE id_klient=? ", (id,))
                produkt_kredytowy_rows = c.fetchall()
                for i_rows in  produkt_kredytowy_rows:
                    pk = Produkt_kredytowy(id_klient=id, nr_wniosku=i_rows[1], kwota_kredytu=i_rows[2], oprocentowanie=i_rows[3])   
                    klient.produkt_kredytowy.append(pk)
        except Exception as e:
            raise RepositoryException('error getting by id klient: %s' % str(e))
        return klient

    def update(self, klient):
        """Metoda uaktualnia pojedynczego klienta z przypisanymi kredytami,
         """
        try:
            K_oryg = self.getById(klient.id_klient)
            if K_oryg != None:
                self.delete(klient.id_klient)
            self.add(klient)

        except Exception as e:
            raise RepositoryException('error updating %s' % str(e))

    def sumaKredytowKlienta(self, id):

         try:
            c = self.conn.cursor()
            c.execute("SELECT sum(kwota_kredytu) FROM produkt_kredytowy  where id_klient = ?", (id,))
            row = c.fetchone()
            if row == None:
                suma_kredytow_klienta=None
            else:
                suma_kredytow_klienta=row[0]
         except Exception as e:
            raise RepositoryException('error getting suma: %s' % str(e))
         return suma_kredytow_klienta

    def sumaKredytowWszystkich(self):

         try:
            c = self.conn.cursor()
            c.execute("SELECT sum(kwota_kredytu) FROM produkt_kredytowy")
            row = c.fetchone()
            if row == None:
                suma_kredytow_klienta=None
            else:
                suma_kredytow_klienta=row[0]
         except Exception as e:
            raise RepositoryException('error getting suma: %s' % str(e))
         return suma_kredytow_klienta


    def sredniaKredytowKlienta(self, id):

         try:
            c = self.conn.cursor()
            c.execute("SELECT avg(kwota_kredytu) FROM produkt_kredytowy where id_klient = ?", (id,))
            row = c.fetchone()
            if row == None:
                suma_kredytow_klienta=None
            else:
                suma_kredytow_klienta=row[0]
         except Exception as e:
            raise RepositoryException('error getting srednia: %s' % str(e))
         return suma_kredytow_klienta

        
if __name__ == '__main__':
    try:
        with KlRepository() as kl_repository:
            kl_repository.delete(1)
            kl_repository.delete(2)
            kl_repository.delete(3)
            kl_repository.complete()
            kl_repository.add(
              Klient(1, "Kokos", "Alojzy", "Madry", 81023132123, "Gdansk",
                     produkt_kredytowy = [
                         Produkt_kredytowy(1, 39281, 100000, 5.32),
                         Produkt_kredytowy(1, 45342, 3400, 9.33),
                         ]
               ))
            kl_repository.add(
                Klient(2, "Doradca smaku", "Miloglost", "Smaczny", 41123023456, "Koniecpol",
                    produkt_kredytowy = [
                         Produkt_kredytowy(2, 747292, 847780, 3.62),
                         Produkt_kredytowy(2, 173745, 1000, 12.2),
                         Produkt_kredytowy(2, 884883, 948400, 2.87),
                         ]
               ))
            kl_repository.add(
                Klient(3, "Szwagropol", "Absalon", "Radosny", 65101183643, "Pacanowo",
                     produkt_kredytowy = [
                         Produkt_kredytowy(3, 12321, 2321, 44.12),
                         Produkt_kredytowy(3, 23452, 77654, 2.25),
                         Produkt_kredytowy(3, 25431, 65433, 3.87),
                         ]
               ))
          
            kl_repository.complete()


            print("Klient o podanym id wraz z kredytami:")
            print(kl_repository.getById(id=1))
            print("*******************")
            print("Zaktualizowanie danych klienta o podanym numerze id")
            kl_repository.update(Klient(1,"KOS", "Alojzy", "NieZbytMadry", 81023132123, "Gdansk",
                     produkt_kredytowy = [
                         Produkt_kredytowy(1, 39281, 100000, 0.32),
                         Produkt_kredytowy(1, 45342, 3400, 9.33),
                         ]
               ))
            print("Suma kredytow dla klienta o podanym id:")
            print(kl_repository.sumaKredytowKlienta(id=2))
            print("Srednia kredytow dla klienta o podanym id:")
            print(kl_repository.sredniaKredytowKlienta(id=2))
            print("Suma kredytow wszystkich klientow:")
            print(kl_repository.sumaKredytowWszystkich())

    except RepositoryException as e:
        print(e)

   
