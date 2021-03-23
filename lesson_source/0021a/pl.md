PyLove 1.0 Powtórka
=====================

CRUD
----

* C – Create - Stwórz
* R – Read - Odczytaj
* U – Update - Zmodyfikuj
* D – Delete - Usuń

Typy liczbowe
-------------

```python
# int:
1 2 123123

# float:
1.23     3.22   3.0   123.12311

1.23     3.22   3.0   123.12311

```

Na liczbach możemy wykonywać znane nam operacje matematyczne:
+ - * / ** // %
Np. 

```python
23 + 7 // 2 * 5 % 3
(2 + 2) * 2 ** 2 + (3 -1) * 2

(2 + 2) * 2 ** 2 + (3 -1) * 2

```

Typ tekstowy
------------

	```python
'Ala ma kota'
'Ala ma kota'
```

	'Kot ma ale'
	'''Nie Kot	Ma
	Nie Ale'''

Można z nimi robić wiele rzeczy!

```python
'Ala' + 'Ma' + 'kota'
'{} ma {}'.format('Pies', 'wilka')

'{} ma {}'.format('Pies', 'wilka')

```

zmienna
-------

C:

```python
dane = 'kot'
dane = 'kot'
```

R:

```python
dane
dane
```

U:

```python
dane = 'pies'
dane = 'pies'
```

D: nie ma potrzeby Python zrobi to za nas.

```python
moja_lista = ['x', 'y', 'ciecz']
moj_string = 'PyLove'
moja_liczba = 1.23

moja_liczba = 1.23

```

lista
-----

Przykłady:

```python
```

	['piotr', 20, 185]
	[1, 3, 6]
C:

```python
moja_lista = [['magda', 22], ['zosia', 23]]
moja_lista = [['magda', 22], ['zosia', 23]]
```

R:

```python
moja_lista[0]
moja_lista[0][1]

moja_lista[0][1]

```

U:

```python
moja_lista[1] = ['cecylia', 55]
moja_lista[1][0] = 'weronika'
moja_lista[1][0] = 'weronika'
```

D:

```python
moja_lista.pop()
moja_lista[0].remove('magda')

moja_lista[0].remove('magda')

```

slice - kawałek
---------------

```python
moja_torebka = ['szminka', 'pomadka', 'portfel', 'okulary']
moj_string = 'PyLove'
moja_torebka[0:2]
moja_torebka[::2]
moj_string[2:4]
moj_string[::3]

moj_string[::3]

```

slownik
-------

Przykłady:

```python
```

	{'klucz': 'wartosc', 'klucz_2': 'wartosc'}
	{1: 'jeden', 2: 'dwa', 3: 'trzy'}

C:

```python
moj_slownik = {'imie': 'piotr', 'wiek': 99}
moj_slownik = {'imie': 'piotr', 'wiek': 99}
```

	moj_slownik['plec'] = 'M'
R:

```python
moj_slownik['imie']	moj_slownik.get('imie')
moj_slownik['imie']	moj_slownik.get('imie')
```

	moj_slownik['wiek']
U:

```python
moj_slownik['imie'] = 'cecylia'
moj_slownik['imie'] = 'cecylia'
```

	moj_slownik['wiek'] = 22

D:

```python
del moj_slownik['wiek']

del moj_slownik['wiek']

```

funkcje wbudowane
-----------------

Ogólne:

	```python
print()
input()
abs()
len()
round()

round()

```

Pomocnicze:

```python
type()
dir()
help()

help()

```

Funkcje do zmiany typu:

```python
```

	str()
	int()
	float()
	list()

Przykłady:

```python
str(int(float('123123.123123')))
list('ala ma kota')

list('ala ma kota')

```

typ bool i if
-------------

Bool może przyjąć jedną z dwóch wartości:
* True 
* False

Składnia funkcji warunkej if:

```python
if 3 > 5:	
    print('alternatywna matematyka')
elif 3 == 5:
    print('chyba zmienilismy wszechswiat')
elif 1 <= 0 or 1 >= 5 and True:
    print('ehhh...')
else:
    print('wszystko jest ok')

    print('wszystko jest ok')

```

pętla for
---------

```python
for letter in in 'Ala ma Kota':
    print(letter)

moja_lista = ['x', 'y', 'ciecz']
for rzecz in moja_lista:
    print(rzecz)

# petla o okreslonej liczbie wykonań
for i in range(10)
    print(i)

    print(i)

```

pętla while
-----------

```python
czy_zakonczyc_program = False
while not czy_zakonczyc_program:
    odp = input('czy zakonczyc program T/N')
    if odp == 'T':
        czy_zakonczyc_program = True

        czy_zakonczyc_program = True

```

funkcje - def
-------------

```python
def moja_funkcja():
    print('To jest moja funkcja')

moja_funkcja()
moja_funkcja()

def moje_dodawanie(a, b):
    c = a + b
    print('Twoim wynikiem jest liczba: ' + str(c))

moje_dodawanie(2, 3)

def moje_potegowanie(a, b=2):
    c = a ** b
    print('Liczba' + str(a) + ' do ' + str(b) +' jest liczba: ' + str(c))

moje_potegowanie(2)
moje_potegowanie(2, b=10)

moje_potegowanie(2, b=10)

```

łapanie wyjatkow - try/except
-----------------------------

```python
def test_try(alist):
    try:
        return alist[1]
    except IndexError:
        print('Obiekt nie ma tylu elementow')

        print('Obiekt nie ma tylu elementow')

```

Przygotowanie do zadań
----------------------

Pobierz plik zawierający bazę krajów z:
[http://dyba.it/countries.py](http://dyba.it/countries.py)

