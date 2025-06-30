# Gas Station Management App

## Jak uruchomić lokalnie

1. Zainstaluj Python 3.10+ i pip
2. (Opcjonalnie) Utwórz środowisko wirtualne:

    ```bash
    python -m venv .venv
    source .venv/bin/activate    # Linux/Mac
    .\.venv\Scripts\activate     # Windows
    ```

3. Zainstaluj zależności:

    ```bash
    pip install -r requirements.txt
    ```

4. Uruchom aplikację:

    ```bash
    python app.py
    ```

5. Przeglądaj na: [http://localhost:5000](http://localhost:5000)

---

## Jak zbudować i uruchomić obraz Dockera

1. Zbuduj obraz:

    ```bash
    docker build -t gasstation-app .
    ```

2. Uruchom kontener:

    ```bash
    docker run -p 5000:5000 gasstation-app
    ```

3. Wejdź na [http://localhost:5000](http://localhost:5000)