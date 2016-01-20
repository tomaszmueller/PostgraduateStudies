# -*- coding: utf-8 -*-
import numpy as np
import sqlite3
from datetime import datetime

#
# Ścieżka połączenia z bazą danych
#
db_path = 'mybankbase.db'

#
# Wyjątek używany w repozytorium
#
class RepositoryException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors


class Konto():
    def __init__(self, nr_rachunku, rodzaj_konta_id_rodzaj_konta, stan, data_otwarcia):
        self.nr_rachunku = nr_rachunku
        self.rodzaj_konta_id_rodzaj_konta = rodzaj_konta_id_rodzaj_konta
	self.stan = stan
        self.data_otwarcia = data_otwarcia

    def __repr__(self):
        return "<Konto(nr_rachunku='%s', rodzaj_konta_id_rodzaj_konta='%s', stan='%s', data_otwarcia='%s')>" % (
                    str(self.nr_rachunku), str(self.rodzaj_konta_id_rodzaj_konta), str(self.stan), str(self.data_otwarcia)
                )

class Klient():
    def __init__(self, id_klient, imie, nazwisko, ulica, nr_domu, kod_pocztowy, miejscowosc, nr_lokalu, kredyty):
        self.id_klient = id_klient
        self.imie = imie
	self.nazwisko = nazwisko
        self.ulica = ulica
	self.nr_domu = nr_domu
	self.kod_pocztowy = kod_pocztowy
	self.miejscowosc = miejscowosc
	self.nr_lokalu = nr_lokalu
	self.kredyty = kredyty
	
    def __repr__(self):
        return "<Klient(id_klient='%s', imie='%s', nazwisko='%s', ulica='%s', nr_domu='%s', kod_pocztowy='%s', miejscowosc='%s', nr_lokalu='%s', kredyty='%s')>" % (
                    str(self.id_klient), self.imie, self.nazwisko, self.ulica, self.nr_domu, self.kod_pocztowy, self.miejscowosc, self.nr_lokalu, str(self.kredyty)
                )

class Klient_Konto():
    def __init__(self, id_klient_konto, konto_nr_rachunku, klient_id_klient):
        self.id_klient_konto = id_klient_konto
        self.konto_nr_rachunku = konto_nr_rachunku
	self.klient_id_klient = klient_id_klient

    def __repr__(self):
        return "<Klient_Konto(id_klient_konto='%s', konto_nr_rachunku='%s', klient_id_klient='%s')>" % (
                    str(self.id_klient_konto), str(self.konto_nr_rachunku), str(self.klient_id_klient)
                )

class Kredyt():
    def __init__(self, id_kredytu, rodzaj_kredytu_id_rodzaj_kredytu, klient_id_klient, okres, do_splacenia):
        self.id_kredytu = id_kredytu
        self.rodzaj_kredytu_id_rodzaj_kredytu = rodzaj_kredytu_id_rodzaj_kredytu
	self.klient_id_klient = klient_id_klient
	self.okres = okres
	self.do_splacenia = do_splacenia
    def __repr__(self):
        return "<Kredyt(id_kredytu='%s', rodzaj_kredytu_id_rodzaj_kredytu='%s', klient_id_klient='%s', okres='%s', do_splacenia='%s')>" % (
                    self.id_kredytu, self.rodzaj_kredytu_id_rodzaj_kredytu, self.klient_id_klient, self.okres, self.do_splacenia)


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
# repozytorium obiektow typu Klient
#
class KlientRepository(Repository):

    def add(self, klient):
        
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO Klient VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
                        (klient.id_klient, klient.imie, klient.nazwisko, klient.ulica, klient.nr_domu, klient.kod_pocztowy, klient.miejscowosc, klient.nr_lokalu)
                    )
        except Exception as e:
            #print "klient add error:", e
            raise RepositoryException('error adding klient %s' % str(klient))
	    if klient.kredyty:
                for kredyt in klient.kredyty:
                    try:
			print "add kredyt"
                        c.execute('INSERT INTO Kredyt VALUES(?,?,?,?,?)',
                                        (kredyt.id_kredytu, kredyt.rodzaj_kredytu_id_rodzaj_kredytu, klient.id_klient, kredyt.okres, kredyt.do_splacenia)
                                )
                    except Exception as e:
                        #print "kredyt add error:", e
                        raise RepositoryException('error adding kredyt item: %s, to klient: %s' %
                                                    (str(kredyt), str(kredyt.id_kredytu))
                                                )

    def delete(self, klient):
        
        try:
            c = self.conn.cursor()

            c.execute('DELETE FROM klient WHERE id_klient=?', (klient.id_klient,))

            c.execute('DELETE FROM kredyt WHERE klient_id_klient=?', (klient.id_klient,))

        except Exception as e:
            raise RepositoryException('error deleting klient %s' % str(klient))

    def getById(self, id_klient):
        try:
	    c = self.conn.cursor()
            c.execute("SELECT * FROM Klient WHERE id_klient=?", (id_klient,))
            klient_row = c.fetchone()
            if klient_row == None:
                klient=None
            else:
                c.execute("SELECT * FROM kredyt WHERE klient_id_klient=?", (id_klient,))
		kredyty_rows = c.fetchall()
                kredyty_klient = []
                for kredyt_row in kredyty_rows:
                    kredyt = Kredyt(id_kredytu=kredyt_row[1],rodzaj_kredytu_id_rodzaj_kredytu=kredyt_row[2],klient_id_klient=kredyt_row[3],okres=kredyt_row[4],do_splacenia=kredyt_row[5])
                    kredyty_klient.append(kredyt)
		klient=Klient(id_klient,klient_row[1],klient_row[2],klient_row[3],klient_row[4],klient_row[5],klient_row[6],klient_row[7],kredyty_klient)
		
	except Exception as e:
            raise RepositoryException('error getting by id klient_id_klient: %s' % str(id_klient))

        return klient

    def update(self, klient):
       
        try:
            klient_oryg = self.getById(klient.id_klient)
	    if klient_oryg != None:
                klient_oryg.imie = "Bartek"
		klient_oryg.nazwisko = "Kazmierski"
		klient_oryg.miejscowosc = "Nowy Targ"
                self.delete(klient)
            self.add(klient_oryg)

        except Exception as e:
            
            raise RepositoryException('error updating klient %s' % str(klient))

    def Statistics(self, klient):
	
	try:
	    kredyty_do_splacenia = []
	    for kredyt_row in klient.kredyty:
		kredyty_do_splacenia.append(kredyt_row.do_splacenia)
	    print "Srednia wartosc kredytu do splacenia: ", np.mean(kredyty_do_splacenia)
	    print "Odchylenie standardowe z wartosci kredytu do splacenia:  ", np.std(kredyty_do_splacenia, ddof=1)

	    
	except Exception as e:
            
            raise RepositoryException('Statistics error ')

#
# repozytorium obiektow typu Konto
#
class KontoRepository(Repository):

    def add(self, konto):
        
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO Konto VALUES(?, ?, ?, ?)',
                        (konto.nr_rachunku, konto.rodzaj_konta_id_rodzaj_konta, konto.stan, konto.data_otwarcia)
                    )
        except Exception as e:
            
            raise RepositoryException('error adding konto ')

    def delete(self, konto):
        
        try:
            c = self.conn.cursor()

            c.execute('DELETE FROM konto WHERE nr_rachunku=?', (konto.nr_rachunku,))

        except Exception as e:
            #print "klient delete error:", e
            raise RepositoryException('error deleting konto %s' % str(konto))

    def update(self, konto):
        
        try:
            konto_oryg = self.getById(konto.nr_rachunku)
            if konto_oryg != None:
                konto_oryg.stan = -252
                self.delete(konto)
            self.add(konto_oryg)

        except Exception as e:
            
            raise RepositoryException('error updating klient %s' % str(klient))

    def getByKlientId(self, id_klient):

	try:
	    c = self.conn.cursor()
	    c.execute("SELECT K.* FROM Konto K INNER JOIN Klient_konto KK ON K.nr_rachunku=KK.konto_nr_rachunku WHERE KK.klient_id_klient=?", (id_klient,))
	    konto_row = c.fetchone()
	    konto = None
            if konto_row != None:
                konto=Konto(konto_row[0], konto_row[1], konto_row[2], konto_row[3])
	except Exception as e:
            raise RepositoryException('error getting konto by id_klient: %s' % str(id_klient))

        return konto

    def getById(self, nr_rachunku):

	try:
	    c = self.conn.cursor()
            c.execute("SELECT * FROM Konto WHERE nr_rachunku=?", (nr_rachunku,))
            konto_row = c.fetchone()
            if konto_row == None:
                konto=None
            else:
                konto=Konto(nr_rachunku, konto_row[1], konto_row[2], konto_row[3])
		
	except Exception as e:
            raise RepositoryException('error getting konto by Id: %s' % str(nr_rachunku))

        return konto

if __name__ == '__main__':
    try:
        with KlientRepository() as klient_repository:
	    klient_kredyty = [
                            Kredyt(id_kredytu=3498659,rodzaj_kredytu_id_rodzaj_kredytu=2,klient_id_klient=1,okres="0025-01-01 00:00:00",do_splacenia=300000),
			    Kredyt(id_kredytu=3498700,rodzaj_kredytu_id_rodzaj_kredytu=2,klient_id_klient=1,okres="0020-01-01 00:00:00",do_splacenia=500000),
			    Kredyt(id_kredytu=3498701,rodzaj_kredytu_id_rodzaj_kredytu=2,klient_id_klient=1,okres="0030-01-01 00:00:00",do_splacenia=250000),
			    Kredyt(id_kredytu=3498759,rodzaj_kredytu_id_rodzaj_kredytu=2,klient_id_klient=1,okres="0015-01-01 00:00:00",do_splacenia=100000)
                        ]
	    klient_to_add = Klient(1, "Adam", "Slodowy", "Ziemska", "1", "57-891", "Gdynia", "3", klient_kredyty)
	    klient_repository.add(klient_to_add)
	    klient_repository.Statistics(klient_to_add)
    	    klient_repository.complete()
	    
            print klient_repository.getById(1)
    except RepositoryException as e:
        print(e)

    try:
        with KlientRepository() as klient_repository:
            klient_repository.update(
                Klient(1, "Adam", "Slodowy", "Ziemska", "1", "57-891", "Gdynia", "3",
                        kredyty = [
                            Kredyt(id_kredytu=3498659,rodzaj_kredytu_id_rodzaj_kredytu=2,klient_id_klient=1,okres="0025-01-01 00:00:00",do_splacenia=300000)
                        ]
                    )
                )
            klient_repository.complete()
	    print klient_repository.getById(1)
    except RepositoryException as e:
        print(e)

    

    
    try:
        with KlientRepository() as klient_repository:
            klient_repository.delete( Klient(1, "Adam", "Slodowy", "Ziemska", "1", "57-891", "Gdynia", "3",
                        kredyty = [
                            Kredyt(id_kredytu=3498659,rodzaj_kredytu_id_rodzaj_kredytu=2,klient_id_klient=1,okres="0025-01-01 00:00:00",do_splacenia=300000)
                        ]
                    ) )
    	    klient_repository.complete()
    except RepositoryException as e:
        print(e)
