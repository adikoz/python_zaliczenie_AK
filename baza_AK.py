# -*- coding: utf-8 -*-

import sqlite3


db_path = 'zadanie_AK.db'
conn = sqlite3.connect(db_path)

c = conn.cursor()
#
# Tabele
#



c.execute('''
create table klient(
id_klient integer Primary Key,
nazwa varchar(45) not null,
imie varchar(30) not null,
nazwisko varchar(30)not null,
PESEL varchar(11) not null,
miasto varchar(30) not null
)
''')

c.execute('''
create table produkt_kredytowy(
id_produkt_kredytowy integer Primary Key,
nr_wniosku varchar(20) not null,
kwota_kredytu integer,
oprocentowanie float,
id_klient INTEGER,
FOREIGN KEY(id_klient) references klient(id_klient)
)
''')
