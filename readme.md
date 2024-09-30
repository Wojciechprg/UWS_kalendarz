Kalendarz Wydarzeń - Aplikacja Flask
====================================
Jak sklonować repozytorium i uruchomić aplikację
-----------------------------------------------
1. Sklonuj repozytorium:
```bash
git clone https://github.com/Wojciechprg/UWS_kalendarz
```
2. Przejdź do katalogu z projektem:
```bash
cd UWS_kalendarz
```
Uruchomienie aplikacji lokalnie (Flask)
---------------------------------------
1. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```
2. Uruchom aplikację:
```bash
python3 -m flask run
```
Aplikacja będzie dostępna pod adresem http://localhost:5000/

Uruchomienie aplikacji w Dockerze
--------------------------------
1. Zbuduj obraz Dockera:
```bash
docker build -t kalendarz_wydarzen .
```
2. Uruchom kontener Dockera:
```bash
docker run -p 5000:5000 kalendarz_wydarzen
```
Aplikacja będzie dostępna pod adresem http://localhost:5000/

Jak uruchomić testy jednostkowe
-------------------------------
1. Aby uruchomić testy wykonaj:
```bash
python3 -m unittest discover
```
Uwagi
====
Jeśli korzystasz z Dockera, upewnij się, że Docker jest poprawnie zainstalowany i skonfigurowany w twoim systemie
---------------------------------------------------------------------------------------------------------------