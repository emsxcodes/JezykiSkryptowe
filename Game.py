# Projekt zaliczeniowy - Języki skryptowe - Python - 08.12.22r.

# Wtyczka rozszerzająca mozliwosci funkcji input()
import pyinputplus as pyip

# W programie będą używane losowe wartości dlatego należy zaimportować random
import random

import pytest as pytest


# Klasa Dictionary czyli miejsce w którym dzieje się wszystko co jest związane z naszym słownikiem, od wczytania pliku dictionary.txt,
# przez losowanie słów w zależności od poziomu trudnosci (5 poziomów trudności: poczatkujacy,latwy, sredni, trudny, ekstremalny)

class Dictionary:
    def __init__(self, slownik="dictionary.txt"):
        try:
            with open("dictionary.txt", "r") as file:
                self.slownik = list(file.read().split())
                if len(self.slownik) < 10:
                    print("Baza danych musi zawierać co najmniej 10 słów")
                    exit(1)
        except:
            print("Nie można otworzyć pliku")
            exit(1)

# Funkcja odpowiadajaca za losowanie slowa, ustawilem kilka mozliwych poziomow trudnosci które zależą po prostu od dlugosci slowa,
# w zaleznosci od poziomu jaki wybierzemy zalezy dlugosc slowa ktore musimy zgadnac. Nastepnie funkcja analizuje nasza liste
# i wybiera slowa w okreslonej dlugosci po czym losuje jedno z nich.

    def losuj_slowo(self, poziom_trudnosci) -> str:
        if poziom_trudnosci == 1:
            poczatkujacy_slownik = [word for word in self.slownik if len(word)==3]
            return random.choice(poczatkujacy_slownik)
        elif poziom_trudnosci == 2:
            latwy_slownik = [word for word in self.slownik if len(word)==4]
            return random.choice(latwy_slownik)
        elif poziom_trudnosci == 3:
            sredni_slownik = [word for word in self.slownik if len(word)==6]
            return random.choice(sredni_slownik)
        elif poziom_trudnosci == 4:
            trudny_slownik = [word for word in self.slownik if len(word)==8]
            return random.choice(trudny_slownik)
        elif poziom_trudnosci == 5:
            ekstremalny_slownik = [word for word in self.slownik if len(word)>8]
            return random.choice(ekstremalny_slownik)

class Validator:
    @staticmethod
    def sprawdz_slowo(slowo="")->bool:
        return len(set(slowo.lower())) == len(slowo.lower())

# Klasa Stats zgodnie z założeniami projektu będzie przechowywać informacje o Bullsach i Cowsach oraz liczbie prob

class Stats:
    proby = 0
    cows = 0
    bulls = 0
# Odpowiada za eksport wynikow do pliku tekstowego (otwieramy plik w trybie do nadpisu i
    # nasze wyniki z kazda nastepna gra beda dopisywane)
    def eksportuj_wynik(self):
        with open("highscore.txt", "a") as file:
            file.write(f"Liczba prob: {self.proby} bulls:{self.bulls} cows:{self.cows} \n")
        print("Twoje wyniki zostaly wyeksportowane do pliku highscore.txt")
        wyswietl_menu()

class Engine:
    # Obiekt typu Dictionary zawierający slowa
    slowa = Dictionary()
    # Obiekt typu Stats przechowujacy statystyki w czasie gry
    statystyki = Stats()
    # Obiekt typu Validator odpowiedzialny za testowanie czyli sprawdzanie czy jest izogramem(rzeczownikiem)
    tester = Validator()
    # Domyslna liczba prob wg. zalozen projektu ma wynosic 10
    domyslna_liczba_prob = 10

    # Ponizej znajduja sie funkcje odpowiedzialne za poszczegolne opcje gry

    # 1 - Rozpocznij nową grę
    def nowa_gra(self):
        print("Rozpoczynam losowanie słowa")
        # Losujemy slowo z klasy Dictionary ktora pobiera z pliku dictionary.txt
        slowo = self.slowa.losuj_slowo(poziom_trudnosci=self.poziom_trudnosci)
        print("Drogi graczu, skup się, losowanie zostało zakończone!\n")
        # W zaleznosci od wyboru poziomu trudnosci otrzymamy slowo o danej dlugosci
        print(f"Zostało wylosowane slowo o długości {len(slowo)}")
        # Program wykonuje sie do momentu gdy zejdziemy z liczba prob do zera
        while self.liczba_prob > 0:
            self.statystyki.bulls = 0
            self.statystyki.cows = 0
            twoja_proba = pyip.inputStr("Podaj swoją propozycje: ")
            if self.tester.sprawdz_slowo(twoja_proba):
                for(znak_uzytkownika, znak_komputera) in zip (twoja_proba, slowo):
                    if znak_uzytkownika in slowo:
                        if znak_komputera == znak_uzytkownika:
                            self.statystyki.bulls += 1
                        else:
                            self.statystyki.cows += 1
                if self.statystyki.bulls == len(slowo):
                    print(f"Gratulacje! Zgadles slowo prawidlowo za {self.liczba_prob} razem")
                    self.statystyki.liczba_prob = self.liczba_prob
                    wyswietl_menu()
                else:
                    self.liczba_prob = self.liczba_prob - 1
                    self.statystyki.proby += 1
                    print("Niestety! Nie udało Ci się zgadnąć \n"
                          f"Twoje statystyki na ten moment: \n"
                          f"Liczba prób:{self.liczba_prob} \n"
                          f"Bulls{self.statystyki.bulls} & Cows{self.statystyki.cows}")
        print("Drogi uzytkowniku - niestety ale przegrales! \n"
              f"Gra zostala zakonczona \n")
        print("Twoje statystyki na koniec gry: \n"
              f"Liczba prób:{self.liczba_prob} \n"
              f"Bulls{self.statystyki.bulls} & Cows{self.statystyki.cows}")
        self.liczba_prob = self.domyslna_liczba_prob
        wyswietl_menu()

    # 2 - Wyswietl zasady gry
    def wyswietl_zasady_gry(self):
        print("Tekstowa gra w której komputer (Host) losuje słowo, które jest izogramem (izogram jest to wyraz w którym nie powtarzajq się żadne litery) \n"
              "i informuje użytkownika (Guesser) o ilości liter w słowie. \n"
              "Użytkownik (Guesser) stara się zgadnqć co to za słowo. Komputer (Host) po każdej próbie zwraca liczbe Cows & Bulls. \n"
              "Liczba przy słowie Cows oznacza literę występujqcq w słowie lecz na złej pozycji, \n"
              "liczba przy słowie Bulls oznacza poprawnq literę na poprawnej pozycji. \n"
              "Gra kończy się kiedy liczba przy Bulls będzie taka sama jak długość słowa wylosowanego przez komputer. ")
        wyswietl_menu()

    # 3 - Wyeksportuj wyniki do pliku tekstowego

    # Ta funkcja znadjuje sie bezposrednio w klasie Stats poniewaz tam znajduja sie te wartosci

    # 4 - Zmien poziom trudnosci

    # W tym miejscu znajduja się opcje umozliwiajace zmiane poziomu trudnosci na jeden z 5 dostepnych (jako standardowy ustawiłem "Łatwy")

    poziomy_trudnosci = {"Początkujący" : 1, "Łatwy" : 2, "Średni": 3, "Trudny": 4, "Ekstremalny": 5}

    poziom_trudnosci = poziomy_trudnosci["Łatwy"]

    def zmien_poziom_trudnosci(self, poziom_trudnosci):
        self.poziom_trudnosci = poziom_trudnosci
        wyswietl_menu()

    # 5 - Zmien liczbe prób
    # Mozliwosc zmiany liczby prob
    liczba_prob = domyslna_liczba_prob
    def zmien_liczbe_prob(self, liczba_prob):
        if liczba_prob <= 0:
            print("Liczba prob nie moze byc mniejsza badz rowna 0")
            wyswietl_menu()
        else:
            self.liczba_prob = liczba_prob
            wyswietl_menu()

    # 6 - Wyjdz z gry
    # Prosta instrukcja ktora konczy nasza gre
    def wyjdz_z_gry(self):
        print(f"Dziekuje za wspolna gre! \n"
              "Do zobaczenia!")
        exit(1)

silnik = Engine()

def wyswietl_menu():
    print("\n Witaj w grze Bulls&Cows \n Jeśli chcesz zagrać lub zmienić zasady wybierz jedną z poniższych opcji\n"
          "1 - Rozpocznij nową grę\n"
          "2 - Wyswietl zasady gry\n"
          "3 - Wyeksportuj wyniki do pliku tekstowego\n"
          "4 - Zmien poziom trudnosci\n"
          "5 - Zmien liczbe prób\n"
          "6 - Wyjdz z gry\n")
    menu_wyboru()

def menu_wyboru():
        wybor_uzytkownika = pyip.inputNum()
        while wybor_uzytkownika not in range (1,7):
            print(f"Aby wybrac jedną z opcji wybierz liczbę z zakresu 1-6")
            wybor_uzytkownika = pyip.inputNum()
        else:
            if wybor_uzytkownika ==1:
                silnik.nowa_gra()
            elif wybor_uzytkownika ==2:
                silnik.wyswietl_zasady_gry()
            elif wybor_uzytkownika ==3:
                silnik.statystyki.eksportuj_wynik()
            elif wybor_uzytkownika ==4:
                print(f"Twoj aktualny poziom trudnosci to: {silnik.poziom_trudnosci}")
                print("Wybierz poziom trudnosci \n"
                      "1 - Poczatkujacy [3 znaki]\n"
                      "2 - Łatwy [4 znaki]\n"
                      "3 - Średni [6 znakow]\n"
                      "4 - Trudny [8 znakow]\n"
                      "5 - Ekstremalny [Wiecej niz 8 znakow]\n")
                silnik.poziom_trudnosci = pyip.inputNum(prompt="Podaj poziom trudności: ")
                silnik.zmien_poziom_trudnosci(silnik.poziom_trudnosci)
            elif wybor_uzytkownika ==5:
                print(f"Twoja aktualna liczba prob to: {silnik.liczba_prob}")
                silnik.liczba_prob = pyip.inputNum(prompt="Podaj liczbe prob:")
                silnik.zmien_liczbe_prob(silnik.liczba_prob)
                wyswietl_menu()
            elif wybor_uzytkownika ==6:
                silnik.wyjdz_z_gry()
# TESTY

# Sprawdzenie poprawnosci dzialania validatora - jest kluczowe przed rozpoczeciem naszej gry

@pytest.mark.parametrize("slowo", [("armia"),("ser"),("kareta"),("klasa"),("kraj")])
def test_sprawdzenie_czy_jest_izogramem(slowo):
    assert Validator.sprawdz_slowo(slowo) == True

# Nasza gra rozpoczyna sie w tym miejscu od prostej instrukcji wyswietl menu ktora zawiera w sobie odnosnik

wyswietl_menu()
