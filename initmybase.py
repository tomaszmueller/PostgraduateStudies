# -*- coding: utf-8 -*-

import sqlite3


db_path = 'mybankbase.db'
conn = sqlite3.connect(db_path)

c = conn.cursor()
#
# Tabele
#

c.execute('''
          CREATE TABLE konto (
    nr_rachunku character varying PRIMARY KEY,
    rodzaj_konta_id_rodzaj_konta integer,
    stan double precision,
    data_otwarcia date,
    CONSTRAINT konto_fkindex1 FOREIGN KEY (rodzaj_konta_id_rodzaj_konta) REFERENCES rodzaj_konta(id_rodzaj_konta)
);
          ''')
c.execute('''
          CREATE TABLE klient (
    id_klient integer PRIMARY KEY,
    imie character varying,
    nazwisko character varying,
    ulica character varying,
    nr_domu character varying,
    kod_pocztowy character varying,
    miejscowosc character varying,
    nr_lokalu character varying,
    CONSTRAINT klient_fkindex1 CHECK(kod_pocztowy LIKE '%%-%%%')
);
          ''')
c.execute('''
          CREATE TABLE klient_konto (
    id_klient_konto integer PRIMARY KEY,
    konto_nr_rachunku character varying,
    klient_id_klient integer,
    CONSTRAINT klient_konto_fkindex1 FOREIGN KEY (klient_id_klient) REFERENCES klient(id_klient),
    CONSTRAINT klient_konto_fkindex2 FOREIGN KEY (konto_nr_rachunku) REFERENCES konto(nr_rachunku)
);
          ''')
c.execute('''
          CREATE TABLE kredyt (
    id_kredytu integer PRIMARY KEY,
    rodzaj_kredytu_id_rodzaj_kredytu integer,
    klient_id_klient integer,
    okres timestamp without time zone,
    do_splacenia double precision,
    CONSTRAINT kredyt_fkindex1 FOREIGN KEY (klient_id_klient) REFERENCES klient(id_klient),
    CONSTRAINT kredyt_fkindex2 FOREIGN KEY (rodzaj_kredytu_id_rodzaj_kredytu) REFERENCES rodzaj_kredytu(id_rodzaj_kredytu)
);
          ''')
c.execute('''INSERT INTO klient VALUES (1, 'Jan', 'Kowalski', 'Smitha', '5', '99-999', 'Gdansk','17'),
         (2, 'Adam', 'Freund', 'Legionow', '7', '80-800', 'Gdynia', '15'),
         (3, 'Seweryn', 'Wierzchowski', 'Prosta', '6', '71-771', 'Warszawa', '2'),
         (4, 'Ahmed', 'Ben Abubekr', 'Kwiatowa', '9', '01-700', 'Mragowo', '12'),
         (5, 'Li', 'Peng', 'Zlota', '11', '55-556', 'Gizycko', '10'),
         (6, 'Michal', 'Wrona', 'Grunwaldzka', '599', '63-207', 'Bialowieza', '1'),
         (7, 'Jacek', 'Kwasniewski', 'Lipowa', '23', '20-200', 'Swiebodzin', '2'),
         (8, 'Jurij', 'Kolejow', 'Dworcowa', '5', '23-391', 'Krakow', '8'),
         (9, 'Przemyslaw', 'Ustupski', 'Biala', '37', '44-555', 'Lebork', '23'),
         (10, 'Stanislaw', 'Baca', 'Zakopianska', '67', '34-589', 'Zabnica', '31');
''')
c.execute('''INSERT INTO konto VALUES('235456256445646',3,2500,'1999-01-01'),
('222200007777167',2,1500,'1989-01-20'),
('124566588768779',1,1000,'2001-01-03');
''')
c.execute('''INSERT INTO kredyt VALUES(23,1,5,'0025-01-01 00:00:00',156900),
(24,2,8,'0020-01-01 00:00:00',177000),
(25,3,10,'0001-05-01 00:00:00',10000);
''')

