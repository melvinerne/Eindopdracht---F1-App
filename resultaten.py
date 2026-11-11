import logging
from pathlib import Path

RESULTS_DIR = Path("resultaten")

def get_saved_files():
    if not RESULTS_DIR.exists():
        return
    return sorted(path.name for path in RESULTS_DIR.glob("*.txt"))

def open_file(file_name):
    try:
        text = (RESULTS_DIR / file_name).read_text(encoding="utf-8")
        print(f"\nInhoud van {file_name}:\n")
        print(f"{text}\n")
    except:
        logging.error("Bestand lezen mislukt")
        print("Bestand kon niet worden geopend")

def delete_file(file_name):
    try:
        (RESULTS_DIR / file_name).unlink()
        print(f"{file_name} is verwijderd")
    except:
        logging.error("Bestand verwijjderen mislukt")
        print("Bestand kon niet worden verwijderd")

def show_saved_results():
    while True:
        files = get_saved_files()
        if not files:
            print(f"Er zijn geen opgeslagen bestanden\n")
            return

        print("Opgeslagen resultaten:")
        for number, file_name in enumerate(files, start=1):
            print(f"{number} - {file_name}")

        choice = input(f"Kies het nummer van het bestand die je wilt selecteren.\n"
                       f"Kies 0 om te stoppen. ").strip()
        while not choice.isdigit() or int(choice) > len(files):
            logging.warning("Ongeldig bestandsnummer ingevoerd")
            choice = input("Ongeldige invoer, probeer opnieuw").strip()

        choice = int(choice)
        if choice == 0:
            return
        file_name = files[choice-1]

        action = input(f"Welke actie wil je uitvoeren? \n"
                       f"1. Openen\n"
                       f"2. Verwijderen\n"
                       f"3. Ander bestand selecteren\n"
                       f"0. Stop\n"
                       f"Kies het nummer van je optie: ").strip()
        while action not in ("1", "2", "3", "0"):
            logging.warning("Ongeldige invoer bij openen/verwijderen")
            action = input("Ongeldige invoer, kies 1 of 2 ").strip()

        if action == "1":
            open_file(file_name)
        if action == "2":
            confirm = input(f"Weet je zeker dat je '{file_name}' wilt verwijderen? (Ja/Nee): ").capitalize().strip()
            while confirm not in ("Ja", "Nee"):
                logging.warning("Ongeldige invoer bij verwijderen confirmatie")
                confirm = input("Onjuiste invoer, kies Ja of Nee: ").capitalize().strip()
            if confirm == "Ja":
                delete_file(file_name)
            else:
                print("Verwijderen geannuleerd.")
        if action == "3":
            continue
        if action == "0":
            return
        keep_on_going = input("Wil je nog een actie doen met de opgeslagen resultaten? Ja/nee ").capitalize().strip()
        while keep_on_going not in ("Ja", "Nee"):
            logging.warning("Ongeldige invoer bij saved results")
            keep_on_going = input("Ongeldige invoer, kies ja/nee ").capitalize().strip()

        if keep_on_going == "Nee":
            return