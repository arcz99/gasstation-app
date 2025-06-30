# Aplikacja Zarządzania Stacją Paliw

Aplikacja webowa do zarządzania stacją paliw: sprzedaż, fakturowanie, magazyn, pracownicy, role i raporty.

---

## Funkcjonalności

- Zarządzanie pracownikami i rolami (admin/manager/pracownik)
- Obsługa klientów indywidualnych i firm (wystawianie faktur)
- Magazyn produktów i stanów (widok magazynowy)
- Sprzedaż paliw i innych produktów (paragony i faktury)
- Metody płatności: gotówka, karta, przelew (z automatycznym liczeniem reszty)
- Logowanie użytkowników i zmiana hasła
- Filtrowanie i wyszukiwanie transakcji
- Gotowa do uruchomienia w Dockerze (Dockerfile)

---

## Jak uruchomić lokalnie

1. **Zainstaluj Pythona 3.10+ oraz pip**
2. (Zalecane) Utwórz i aktywuj wirtualne środowisko:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate      # Linux/Mac
    .\.venv\Scripts\activate       # Windows
    ```
3. **Zainstaluj zależności:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Uruchom aplikację:**
    ```bash
    python3 app.py
    ```
5. **Aplikacja będzie dostępna pod adresem:**  
   [http://localhost:5000](http://localhost:5000)

---

## Jak uruchomić w Dockerze

1. **Zbuduj obraz Dockera:**
    ```bash
    docker build -t gasstation-app .
    ```
2. **Uruchom aplikację w kontenerze:**
    ```bash
    docker run -p 5000:5000 gasstation-app
    ```
3. **Otwórz w przeglądarce:**  
   [http://localhost:5000](http://localhost:5000)  
   lub na maszynie wirtualnej: [http://IP_UBUNTU:5000](http://IP_UBUNTU:5000)

## Testy automatyczne

Aby uruchomić testy jednostkowe:

```bash
pytest