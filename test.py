#Autor: Marcelina Brygier nr 231293
#Progra słuzy do pracy na zdaniu podanym przez użytkownika
#wykonuje kolejne czynnosci
#Program z wykorzystaniem funkcji usuwa znaki interpunkcyjne
def usuwanie_znakow_interpunkcyjnych(zdanie): #tworzymy funkcje z argumentem zdanie
    znaki = [",", ".", ":", ";", "!", "?","\""]   #do zmiennej znaki zapisujemy w liscie znaki ktore program bedzie usuwal
    for i in zdanie:  # dla kazdej litery w zdaniu
        if i in znaki: #sprawdzamy czy litera w zdaniu znajduje sie w liscie znaki
            zdanie = zdanie.replace(i,"") #jezeli tak, to litere zastepujemy pustym polem
    zdanie_bez = ''
    for word in zdanie.split():
        if word != ' ' or word != '':
            zdanie_bez += word + ' '
    zdanie_bez = zdanie_bez.rstrip()
    return zdanie_bez # i zwracamy zmienione zdanie
#Program przy pomocy funkcji sprawdz czy istnieją wyrazy rozpoczynające się wielka literą.
def wielka_mala_litera(zdanie): #tworzymy funkcje z argumentem zdanie
    if zdanie == "":
        return 'Brak wyrazow, ktore zaczynaja sie wielka litera'
    noweZdanie = zdanie.split(" ")  #tworzymy nowa zmienna noweZdanie, dzieki metodzie split, kazde slowo w zdaniu bedzie osobnym elementem w liscie
    zbior = [] #tworzymy pusty zbior
    for letter in noweZdanie: #dla kazdej litery w zmiennej noweZdanie

        if letter[0].isupper(): # sprawdza warunek czy pierwsza litera elementu jest z wielkiej litery
            zbior.append(letter) #jesli tak dodaje do zbioru
    if len(zbior) > 0: #jesli dlugosc zbioru jest wieksza od 0
        return 'Slowa zaczynajace sie z wielkiej litery',zbior  #zwraca slowa ze zbioru, ktore sa napisane wielka litera
    else:  #w innym wypadku
        return 'Brak wyrazow, ktore zaczynaja sie wielka litera'  #zwraca, ze takich wyrazow nie ma
#program przy uzyciu funkcji sortuje wyrazy alfabetycznie i wyswietla je w zmienionej kolejnosci.
def sortowanie_wyrazow(zdanie):
    if zdanie == "":
        return ""
    #za pomocą split dostajemy listę elementów(kazde slowo oddzielone przecinkiem)
    noweZdanie=zdanie.split(" ")
    #sortuje je
    noweZdanie.sort(key=lambda x:x.split()[0].lower())
    return noweZdanie

zdanie = input("Wypisz dowolne zdanie:"'\n') #zmienna zdanie przechwouje zdanie, ktore wypisze uzytkownik
#Wyświetla kolejne wyniki wykonanych zadań na zdaniu
print("Potwierdzam przyjęcie danych:", zdanie) # powtarza przyjecie danych
zdanie_bez = usuwanie_znakow_interpunkcyjnych(zdanie)
print("usuwam znaki interpunkcyjne: ", zdanie_bez)#dzieki funkcji usuwa znami interpunkcyjne
print("Podaje wyrazy rozpoczynające się z wielkiej litery: ", wielka_mala_litera(zdanie_bez)) #drukuje wyrazy, ktore sa z wielkiej litery
print("Sortuje wyrazy alfabetycznie w zdaniu:", sortowanie_wyrazow(zdanie_bez)) #sortuje wyrazy w kolejnosci alfabetycznej



