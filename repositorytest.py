# -*- coding: utf-8 -*-

import myrepository
import sqlite3
import unittest

db_path = 'mybankbase.db'

class RepositoryTest(unittest.TestCase):

    def setUp(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('DELETE FROM Klient')
        c.execute('DELETE FROM Kredyt')
	c.execute('DELETE FROM Konto')
	c.execute('DELETE FROM Klient_Konto')
        c.execute('''INSERT INTO Klient VALUES(1, 'Jan', 'Kowalski', 'Smitha', '5', '99-999', 'Gdansk','17')''')
        c.execute('''INSERT INTO Kredyt VALUES(23,1,5,'0025-01-01 00:00:00',156900)''')
        c.execute('''INSERT INTO Kredyt VALUES (24,2,8,'0020-01-01 00:00:00',177000)''')
	c.execute('''INSERT INTO Klient_Konto VALUES(1,'235456256445646',1)''')
	c.execute('''INSERT INTO Konto VALUES('235456256445646',1,2500,'1999-01-01')''')
        conn.commit()
        conn.close()

    def tearDown(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('DELETE FROM Kredyt')
        c.execute('DELETE FROM Klient')
        conn.commit()
        conn.close()

    #Test sprawdzający czy w repozytorium istnieje klient o id = 1
    def testGetByIdInstance(self):
        klient = myrepository.KlientRepository().getById(1)
        self.assertIsInstance(klient, myrepository.Klient, "Objekt nie jest klasy Klient")

    #Test sprawdzający czy klient o id = 2 jest None
    def testGetByIdNotFound(self):
        self.assertEqual(myrepository.KlientRepository().getById(2),
                None, "Powinno wyjść None")

    #Test sprawdzający czy klient ma dokładnie dwa kredyty
    def testGetByIdInvitemsLen(self):
        self.assertEqual(len(myrepository.KlientRepository().getById(1).kredyty),
                2, "Powinno wyjść 2")

    #Test sprawdzający czy operacja delete z repozytorium klienta wywoluje RepositoryException
    def testDeleteNotFound(self):
        self.assertRaises(myrepository.RepositoryException,
                myrepository.KlientRepository().delete, 22)

    #Test sprawdzajacy czy klient o id = 1 ma na nazwisko Kowalski
    def testContainsKowalski(self):
	self.assertEqual(myrepository.KlientRepository().getById(1).nazwisko,"Kowalski")

    #Test sprawdzajacy czy suma do splacenia w kredytach klienta jest wieksza niz 500000
    def testSumaKredytowWieksza(self):
	sumakredytow = 0
	for kredyt in myrepository.KlientRepository().getById(1).kredyty:
	    sumakredytow += kredyt.do_splacenia
	self.assertTrue(sumakredytow > 500000)

    #Test sprawdzajacy czy klient o id = 1 ma zalozone konto
    def testKlientKonto(self):
	konto = myrepository.KontoRepository().getByKlientId(1)
	self.assertIsInstance(konto, myrepository.Konto,"Takie konto nie istnieje")

if __name__ == "__main__":
    unittest.main()
