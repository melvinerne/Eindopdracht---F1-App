import requests
import logging
from rich.table import Table
from rich.console import Console
from statistieken import get_average_position, show_race_results, get_fastest_lap, get_total_podiums, compare_race_results, compare_average_positions, compare_fastest_laps, compare_total_podiums
from resultaten import show_saved_results

logging.basicConfig(
    filename="f1_app.log",
    filemode="a",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

URL = "https://api.openf1.org/v1"

print(f"Welkom bij deze F1 app.\nHier kan je statistieken bekijken, vergelijken en opslaan.\n")

def main():
    while True:
        print(f"1. Statistieken ophalen en vergelijken\n"
              f"2. Opgeslagen data bekijken\n"
              f"0. Stop")
        choice = input("Maak je keuze: ")
        while choice not in ("0", "1", "2"):
            logging.warning("Ongeldige invoer bij initialisatie: '%s'", choice)
            choice = input("Ongeldige invoer, kies 1, 2 of 0 ").strip()

        if choice == "1":
            active_drivers, driver, race_data, year = initialize()
            show_main_menu(driver, active_drivers, race_data, year)
        if choice == "2":
            show_saved_results()
        if choice == "0":
            print("Bedankt voor het gebruiken van de F1 app!")
            exit(1)


def initialize():
    year = input("Van welk jaar wil je statistieken bekijken? Je kan kiezen uit 2023 t/m 2025. ")
    while year not in ("2023", "2024", "2025"):
        logging.warning("Ongeldig jaar ingevoerd: '%s'", year)
        year = input("Ongeldige invoer, ja kan kiezen uit 2023 t/m 2025 ")

    race_data = get_race_data(year)
    active_drivers = get_drivers(race_data, year) if race_data else None
    if not active_drivers:
        logging.critical("Race data ophalen (initialisatie) mislukt")
        print("Kan de gegevens nu niet ophalen. Probeer het later opnieuw.")
        exit(1)

    driver = input(f"\nVan welke coureur wil je informatie bekijken? Gebruik de afkorting (bijvoorbeeld VER) ").upper().strip()
    while driver not in active_drivers:
        logging.warning("Ongeldige coureur ingevoerd: '%s'", driver)
        driver = input("Coureur niet gevonden, probeer opnieuw ").upper().strip()
    return active_drivers, driver, race_data, year

def get_race_data(chosen_year):
    params = {'session_name': "Race", "year": chosen_year}
    try:
        response = requests.get(f"{URL}/sessions",params=params, timeout=10)

        if response.ok:
            data = response.json()
            race_data_dict = {session["session_key"]: {
                "country_name": session["country_name"], "location": session['location']}
                for session in data}

            return race_data_dict
        else:
            logging.error("API-fout bij race data: '%s %s'", response.status_code, response.text)
            print(f"Fout: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as error:
        logging.error("Verbindingsfout bij race results voor race data '%s'", error)
        print("De OpenF1 API is momenteel niet bereikbaar.")
        return None

def get_drivers(active_session_keys, year):
    try:
        response = requests.get(f"{URL}/drivers")

        if response.ok:
            data = response.json()
            driver_dict = {}

            for driver_entry in data:
                if driver_entry.get("session_key") in active_session_keys:
                    driver_acronym = driver_entry.get("name_acronym")
                    driver_full_name = driver_entry.get("full_name")
                    driver_number = str(driver_entry.get("driver_number"))

                    if driver_acronym and driver_full_name and driver_number not in driver_dict:
                        driver_dict[driver_acronym] = {
                            "full_name": driver_full_name,
                            "driver_number": driver_number
                        }
        else:
            logging.error("API-fout bij race data: '%s %s'", response.status_code, response.text)
            print(f"Fout: {response.status_code} - {response.text}")
            return None

        table = Table(title=f"\nCoureurs die in {year} hebben gereden:")
        table.add_column("Naam", justify="center")
        table.add_column("Afkorting", justify="center")
        table.add_column("Nummer", justify="center")

        for driver_acronym, values in sorted(driver_dict.items()):
            table.add_row(values["full_name"], driver_acronym, values["driver_number"])

        console = Console()
        console.print(table)

        return driver_dict

    except requests.exceptions.RequestException as error:
        logging.error("Verbindingsfout bij race results voor get drivers '%s'", error)
        print("De OpenF1 API is momenteel niet bereikbaar.")
        return None

def show_main_menu(driver, active_drivers, race_data, year):
    driver_full_name = active_drivers[driver]["full_name"]

    print(f"\nJe hebt gekozen voor {driver_full_name} in het jaar {year}.\n"
          f"Welke statistieken wil je bekijken?")

    table = Table()
    table.add_column("Keuze", justify="center")
    table.add_column("Actie", justify="center")
    table.add_row("1", "Eindstand van alle races")
    table.add_row("2", "Gemiddelde positie")
    table.add_row("3", "Snelste ronde van het seizoen")
    table.add_row("4", "Aantal podia's (top 3)")
    table.add_row("5", "Vergelijken met andere coureur")
    table.add_row("6", "Opgeslagen resultaten")
    table.add_row("0", "Terug")

    console = Console()
    console.print(table)

    menu_choice = input(f"Kies een optie: Kies uit 0 t/m 6 ")
    while menu_choice not in ("0", "1", "2", "3", "4", "5", "6"):
        logging.warning("Ongeldige menukeuze ingevoerd: '%s'", menu_choice)
        menu_choice = input(f"Ongeldige invoer. Kies 0 t/m 6. ")

    match menu_choice:
        case "1":
            show_race_results(driver, driver_full_name, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "2":
            get_average_position(driver, driver_full_name, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "3":
            get_fastest_lap(driver, driver_full_name, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "4":
            get_total_podiums(driver, driver_full_name, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "5":
            compare_drivers(driver, driver_full_name, race_data, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "6":
            show_saved_results()
            show_main_menu(driver, active_drivers, race_data, year)
        case "0":
            return

    return driver_full_name

def keep_on_going(driver, driver_full_name, active_drivers, race_data, year):
    choice = input(f"Wil je meer statistieken bekijken? Ja/nee ").capitalize().strip()
    while choice not in ("Ja", "Nee"):
        logging.warning("Ongeldige invoer bij vraag om door te gaan ingevoerd: '%s'", choice)
        choice = input("Onjuiste invoer, kies ja/nee ").capitalize().strip()
    if choice == "Ja":
        second_choice = input(f"Je bekijkt nu statistieken van {driver_full_name} uit {year}. Wil je verder met dezelfde gegevens? Ja/nee ").capitalize().strip()
        while second_choice not in ("Ja", "Nee"):
            second_choice = input("Onjuiste invoer, kies ja/nee ").capitalize().strip()
        if second_choice == "Ja":
            show_main_menu(driver, active_drivers, race_data, year)
        elif second_choice == "Nee":
            active_drivers, driver, race_data, year = initialize()
            show_main_menu(driver, active_drivers, race_data, year)
    if choice == "Nee":
        return

def compare_drivers(driver, driver_full_name, race_data, year):
    active_drivers = get_drivers(race_data, year)

    driver_to_compare = input(f"Met welke coureur wil je {driver_full_name} vergelijken? Gebruik de afkorting (bijvoorbeeld VER) ").upper().strip()
    while driver_to_compare == driver or driver_to_compare not in active_drivers:
        logging.warning("Ongeldige coureur om te vergelijken ingevoerd: '%s'", driver_to_compare)
        driver_to_compare = input(f"{driver} is al geselecteerd of bestaat niet. Kies een andere coureur ").upper().strip()

    driver_to_compare_full_name =  active_drivers[driver_to_compare]["full_name"]

    print(f"\nJe hebt gekozen om {driver_full_name} te vergelijken met {driver_to_compare_full_name} in het jaar {year}.\n"
          f"Welke statistieken wil je vergelijken?\n")

    table = Table()
    table.add_column("Keuze", justify="center")
    table.add_column("Actie", justify="center")
    table.add_row("1", "Eindstand van alle races")
    table.add_row("2", "Gemiddelde positie")
    table.add_row("3", "Snelste ronde van het seizoen")
    table.add_row("4", "Aantal podia's (top 3)")
    table.add_row("0", "Terug")

    console = Console()
    console.print(table)

    menu_choice = input("Kies een optie: Kies uit 0 t/m 4 ")
    while menu_choice not in ("0", "1", "2", "3", "4"):
        logging.warning("Ongeldige menukeuze om te vergelijken ingevoerd: '%s'", menu_choice)
        menu_choice = input("Ongeldige invoer. Kies 0 t/m 4. ")

    match menu_choice:
        case "1":
            compare_race_results(driver, driver_full_name, driver_to_compare, driver_to_compare_full_name, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "2":
            compare_average_positions(driver, driver_to_compare, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "3":
            compare_fastest_laps(driver, driver_full_name, driver_to_compare, driver_to_compare_full_name, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "4":
            compare_total_podiums(driver, driver_full_name, driver_to_compare, driver_to_compare_full_name, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "0":
            return

main()