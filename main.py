import fdb
import time
import configparser

print("Generator adresów do korespondencji. Wersja 0.1")
print("Copyright (C) 2021 Filip Napierała")
print("Data kompilacji 08.07.2021r.")
print("--------------------------------------------------------------------------------------------------------")
print("Niniejszy program jest wolnym oprogramowaniem - możesz go rozpowszechniać dalej i/lub modyfikować ")
print("na warunkach Powszechnej Licencji Publicznej GNU")
print("wydanej przez Fundację Wolnego Oprogramowania, według wersji 3 tej Licencji lub dowolnej z późniejszych wersji.")
print("Niniejszy program rozpowszechniany jest z nadzieją, iż będzie on użyteczny - jednak BEZ ŻADNEJ GWARANCJI,")
print("nawet domyślnej gwarancji PRZYDATNOŚCI HANDLOWEJ,")
print("albo PRZYDATNOŚCI DO OKREŚLONYCH ZASTOSOWAŃ. Bliższe informacje na ten temat można uzyskać z")
print("Powszechnej Licencji Publicznej GNU.")
print("Powszechna Licencja Publiczna GNU powinna zostać ci dostarczona razem z tym programem")
print("--------------------------------------------------------------------------------------------------------")
print("Program powinien być uruchamiany na serwerze")
print("Proszę sprawdzić plik config.txt pod kątem zgodności danych domyślnych z tymi na Państwa Ogrodzie")
#print("Potencjalne aktualizacje programu będą dostępne pod adresem: www.github.com/filnap/RODNaliczenia")

config = "config.txt"
parser = configparser.ConfigParser()
parser.read('config.txt')

filepath = parser['BASIC']['filepath']
database = parser['BASIC']['database']
user = parser['BASIC']['user']
password = parser['BASIC']['password']

print("Zapis do pliku '%s'. Upewnij się, że jest pusty!" % filepath)

con = fdb.connect(database=database, user=user, password=password, charset='utf8')
cur = con.cursor()
# Main loop
print("Wszystkie dane wpisane prawidłowo")

cur.execute("SELECT NUMERDZIALKI FROM \"@PZD_DZIALKI\" ")
listadzialek = cur.fetchall()
# Creating list in file
L = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
potwierdzenie = input("Gotowość? [T/n]")
if potwierdzenie == "T" or potwierdzenie == "t":

    for h in range(len(listadzialek)):
        L = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        nrdz = listadzialek[h][0]
        print("Obsługuję działkę nr: " + nrdz)


        cur.execute("SELECT IDDZIALKI FROM \"@PZD_DZIALKI\" WHERE NUMERDZIALKI='%s' " % nrdz)
        iddzialkilist = cur.fetchall()
        iddzialki = iddzialkilist[0][0]
        # print("id dzialki:")
        # print(iddzialki)

        cur.execute("SELECT IDSIKONTRWLA FROM \"@PZD_RELDZIALKISIKONTR\" WHERE IDDZIALKI='%s' AND DATADO IS NULL" % iddzialki)
        idkontrwlaraw = cur.fetchall()
        idkontrwla=idkontrwlaraw[0][0]
        print(idkontrwla)

        cur.execute("SELECT IDSIKONTRMALZ FROM \"@PZD_RELDZIALKISIKONTR\" WHERE IDDZIALKI='%s' AND DATADO IS NULL" % iddzialki)
        idkontrmalzraw = cur.fetchall()
        idkontrmalz=idkontrmalzraw[0][0]
        print(idkontrmalz)

        #WLAS

        cur.execute("SELECT IMIE, NAZWISKO, ULICAKOR, KODMIASTAKOR, MIASTOKOR FROM \"@PZD_DZIALKOWIEC\" WHERE IDSIKONTR='%s' " % idkontrwla)
        danewlaraw1 = cur.fetchall()
        print(danewlaraw1)

        cur.execute("SELECT NIPKONTR, TELEFON, EMAIL FROM SIKONTR WHERE IDSIKONTR='%s' " % idkontrwla)
        danewlaraw2 = cur.fetchall()
        print(danewlaraw2)

        L[1] = danewlaraw1[0][0]
        L[2] = danewlaraw1[0][1]
        L[3] = danewlaraw1[0][2]
        L[4] = danewlaraw1[0][3]
        L[5] = danewlaraw1[0][4]

        L[6] = danewlaraw2[0][0]
        L[7] = danewlaraw2[0][1]
        L[8] = danewlaraw2[0][2]

        #MALZ
        if (idkontrmalz != None):
            cur.execute("SELECT IMIE, NAZWISKO, ULICAKOR, KODMIASTAKOR, MIASTOKOR FROM \"@PZD_DZIALKOWIEC\" WHERE IDSIKONTR='%s' " % idkontrmalz)
            danemalzraw1 = cur.fetchall()
            print(danemalzraw1)

            cur.execute("SELECT NIPKONTR, TELEFON, EMAIL FROM SIKONTR WHERE IDSIKONTR='%s' " % idkontrmalz)
            danemalzraw2 = cur.fetchall()
            print(danemalzraw2)

            L[9] = danemalzraw1[0][0]
            L[10] = danemalzraw1[0][1]
            L[11] = danemalzraw1[0][2]
            L[12] = danemalzraw1[0][3]
            L[13] = danemalzraw1[0][4]

            L[14] = danemalzraw2[0][0]
            L[15] = danemalzraw2[0][1]
            L[16] = danemalzraw2[0][2]

        f = open(filepath, "a")

        L[0] = nrdz
        print(L)

        f.write("\n")
        for g in range(len(L)):
            f.write(str(L[g]))
            f.write(";")
            g = g + 1
        f.close()
        h = h + 1
        print("Wiersz zapisano")
    print("Program zakończył pracę sukcesem. Wyłączam za 3 sekundy")
    time.sleep(3)
else:
    print("Nie wpisano 'T'. Program zakończony przez użytkownika. Wyłączam za 3 sekundy")
    time.sleep(3)
con.close()
