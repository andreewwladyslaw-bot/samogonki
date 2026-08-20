# Ten plik odpowiada tylko za tabelę najlepszych wyników.
# Wczytuje dane z JSON-a i zapisuje nowe wyniki po zakończeniu gry.

import json
from pathlib import Path

from constants import MAX_HIGH_SCORES


# Folder, w którym znajduje się storage.py
PROJECT_DIR = Path(__file__).resolve().parent

# Ścieżka do folderu data i pliku JSON
DATA_DIR = PROJECT_DIR / "data"
HIGHSCORES_FILE = DATA_DIR / "highscores.json"


def load_highscores():
    """Wczytuje najlepsze wyniki z pliku JSON."""
    try:
        # Plik jeszcze nie istnieje
        if not HIGHSCORES_FILE.exists():
            return []

        file_content = HIGHSCORES_FILE.read_text(
            encoding="utf-8",
        )

        # Plik jest pusty
        if not file_content.strip():
            return []

        # Zamieniamy tekst z pliku JSON na dane Pythona.
        data = json.loads(file_content)

        # JSON powinien zawierać listę
        if not isinstance(data, list):
            return []

        # Do tej listy trafią tylko poprawne wyniki.
        valid_results = []

        # Sprawdzamy po kolei każdy zapisany wynik.
        for result in data:
            if not isinstance(result, dict):
                continue

            name = result.get("name")
            score = result.get("score")
            distance = result.get("distance")

            if (
                isinstance(name, str)
                and isinstance(score, int)
                and isinstance(distance, int)
                and score >= 0
                and distance >= 0
            ):
                valid_results.append(
                    {
                        "name": name,
                        "score": score,
                        "distance": distance,
                    }
                )

        # Najlepszy wynik ma być na początku listy.
        valid_results.sort(
            key=lambda result: (
                result["score"],
                result["distance"],
            ),
            reverse=True,
        )

        return valid_results[:MAX_HIGH_SCORES]

    except (
        OSError,
        json.JSONDecodeError,
        UnicodeDecodeError,
    ):
        # Uszkodzony lub niemożliwy do odczytania plik
        return []


def save_highscore(player_name, score, distance):
    """Dodaje wynik, sortuje tabelę i zapisuje pięć najlepszych."""
    # Najpierw pobieramy wyniki, które już były zapisane.
    highscores = load_highscores()

    new_result = {
        "name": player_name,
        "score": score,
        "distance": distance,
    }

    # Dodajemy aktualny wynik gracza do listy.
    highscores.append(new_result)

    # Sortujemy od największej liczby punktów do najmniejszej.
    highscores.sort(
        key=lambda result: (
            result["score"],
            result["distance"],
        ),
        reverse=True,
    )

    # Zostawiamy tylko ustaloną liczbę najlepszych wyników.
    highscores = highscores[:MAX_HIGH_SCORES]

    try:
        # Utworzenie folderu data, jeśli go nie ma
        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        HIGHSCORES_FILE.write_text(
            json.dumps(
                highscores,
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )

    except OSError:
        # Błąd zapisu nie powinien wyłączyć całej gry
        pass

    return highscores


def get_best_score(highscores):
    """Zwraca najlepszy wynik albo zero."""
    if not highscores:
        return 0

    return highscores[0]["score"]