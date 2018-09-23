Logika Pythona
==============

Sprawdzanie warunków
--------------------

Porównanie: prawda, czy fałsz?
------------------------------

Porozmawiajmy o porównaniach. Spójrzmy, jak się one zachowują podczas
krótkiej lekcji matematyki:

```python
>>>  2 > 1 
True 
>>> 1 == 2 
False 
>>> 1 == 1.0 
True 
>>> 10 >= 10 
True 
13 <= 1 + 3
False 
>>> -1 != 0 
True
```

Rezultatem porównania jest zawsze `True` lub `False`. Porównania mogą
być włączone w bardziej złożone wyrażenia przy użyciu słów and i or:

```python
>>>  x = 5 
>>>  x < 10 
True 
>>>  2*x > x 
True 
>>>  (x < 10) and (2*x > x) 
True 
>>>  (x != 5) and (x != 4)
False 
>>>  (x != 5) and (x != 4) or (x == 5) 
True
```

Python Love - ćwiczenie
-----------------------

Porozmawiajmy o miłości z naszym cudownym wężem. Napiszcie to w swoim 
interpreterze:

```python
>>>  import this 
>>>  love = this 
>>>  love is this 
>>>  love is not True or False 
>>>  love is love
```

W Pythonie możemy porównywać, używając kilku różnych operatorów:

-   ==
-   is
-   !=
-   not
-   \>=
-   <=
-   in

i łączyć wyrażenia za pomocą:

-   and
-   or

Czy is to to samo co == ?
-------------------------

Przeprowadźmy kilka testów, by sprawdzić, czy 'is' to to samo co '==':

```python
>>> 1000 is 10**3 
>>> 1000 == 10**3
>>> "a" is "a" 
>>> "aa" is "a" * 2 
>>> x = "a" 
>>> "aa" is x * 2 
>>> "aa" == x * 2
>>> [1, 2] == [1, 2]
>>> [1, 2] is [1, 2]

>>> [1, 2] is [1, 2]
```

Wniosek: 'is' zwróci True, jeśli dwie zmienne wskazują na ten sam obiekt,
a '==' zwróci True jeśli obiekty, do których odnoszą się zmienne są równe.

BMI: Gruby, czy nie? Niechaj Python zadecyduje za Ciebie
--------------------------------------------------------

Przejdźmy do naszego kolejnego problemu. Chcemy, aby program wydrukował
właściwą klasyfikację dla obliczonego BMI, przy użyciu poniższej tabeli:

  	BMI              Klasyfikacja
  	-------------- ----------------
  	< 18,5         niedowaga
  	18,5 – 24,99   prawidłowa waga
  	25,0 – 29,99   nadwaga
  	≥ 30,0         otyłość

Musimy użyć "komendy warunkowej' if. Wykona ona dalszy ciąg programu
zależnie od podanego warunku:

Ćwiczenie - prosty pythonowy kalkulator
---------------------------------------

Napiszcie skrypt stanowiący prosty kalkulator, który pobierze dwie
liczby oraz znak operacji matematycznej (+, -, \*, /) i wyświetli
przyjemny string, który pokaże całe równanie oraz rozwiązanie. 
Pamiętajcie: string + string = nowy string :-)
Przykład:

```python
>>>  'Wprowadź pierwszą liczbę' 
10 
>>>  "Wprowadź znak operacji matematycznej (+, -, \*, /)" 
+ 
>>> 'Wprowadź drugą liczbę'
5
'10 + 5 = 15'
```
