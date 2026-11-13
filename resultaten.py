import logging
from pathlib import Path

RESULTS_DIR = Path("resultaten")

def get_saved_files():
    if not RESULTS_DIR.exists():
        return
    return sorted(path.name for path in RESULTS_DIR.glob("*.txt"))

def open_file(file_name):
    try:
        file_path = (RESULTS_DIR / file_name).read_text(encoding="utf-8")
        print(f"\nInhoud van {file_name}:\n")
        print(f"{file_path}\n")
    except OSError as error:
        logging.error("Bestand lezen mislukt: '%s'", error)
        print("Bestand kon niet worden geopend")

def delete_file(file_name):
    try:
        (RESULTS_DIR / file_name).unlink()
        print(f"{file_name} is verwijderd")
    except OSError as error:
        logging.error("Bestand verwijjderen mislukt: '%s'", error)
        print("Bestand kon niet worden verwijderd")


def add_note(file_name):
    file_path = RESULTS_DIR / file_name

    if not file_path.exists():
        logging.error("Bestand niet gevonden: '%s'", file_path)
        print("Bestand bestaat niet")
        return

    added_content = input(f"Welke notitie wil je aan {file_name} toevoegen? ").strip()
    if not added_content:
        print("Geen notitie ingevoerd, bestand is niet aangepast")
        return

    try:
        text = file_path.read_text(encoding="utf-8")
        text = text.split("\n\nNotitie:\n")[0]
        file_path.write_text(f"{text}\n\nNotitie:\n{added_content}\n", encoding="utf-8")
        print(f'{file_name} is aangepast, "{added_content}" is toegevoegd')
    except OSError as error:
        logging.error("Bestand aanpassen mislukt: '%s'", error)
        print("Bestand kon niet worden aangepast")


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
            logging.warning("Ongeldig bestandsnummer ingevoerd: '%s'", choice)
            choice = input("Ongeldige invoer, probeer opnieuw").strip()

        choice = int(choice)
        if choice == 0:
            return
        file_name = files[choice-1]

        action = input(f"Welke actie wil je uitvoeren? \n"
                       f"1. Openen\n"
                       f"2. Notitie toevoegen\n"
                       f"3. Verwijderen\n"
                       f"4. Ander bestand selecteren\n"
                       f"0. Stop\n"
                       f"Kies het nummer van je optie: ").strip()
        while action not in ("1", "2", "3", "4", "0"):
            logging.warning("Ongeldige invoer bij openen/verwijderen: '%s'", action)
            action = input("Ongeldige invoer, kies 1, 2, 3, 4 of 0 ").strip()

        if action == "1":
            open_file(file_name)
        if action == "2":
            add_note(file_name)
            open_file(file_name)
        if action == "3":
            confirm = input(f"Weet je zeker dat je '{file_name}' wilt verwijderen? (Ja/Nee): ").capitalize().strip()
            while confirm not in ("Ja", "Nee"):
                logging.warning("Ongeldige invoer bij verwijderen confirmatie: '%s'", confirm)
                confirm = input("Onjuiste invoer, kies Ja of Nee: ").capitalize().strip()
            if confirm == "Ja":
                delete_file(file_name)
            else:
                print("Verwijderen geannuleerd.")
        if action == "4":
            continue
        if action == "0":
            return
        keep_on_going = input("Wil je nog een actie doen met de opgeslagen resultaten? Ja/nee ").capitalize().strip()
        while keep_on_going not in ("Ja", "Nee"):
            logging.warning("Ongeldige invoer bij saved results: '%s'", keep_on_going)
            keep_on_going = input("Ongeldige invoer, kies ja/nee ").capitalize().strip()

        if keep_on_going == "Nee":
            return