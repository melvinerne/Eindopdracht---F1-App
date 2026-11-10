import requests
from rich.table import Table
from rich.console import Console
from statistieken import get_average_position, show_race_results, get_fastest_lap, get_total_podiums, compare_race_results

URL = "https://api.openf1.org/v1"

print(f"Welkom bij deze F1 app.\nHier kan je statistieken bekijken, vergelijken en opslaan.\n")

def main():
    active_drivers, driver, race_data, year = initialize()

    show_main_menu(driver, active_drivers, race_data, year)

    return active_drivers


def initialize():
    year = input("Van welk jaar wil je statistieken bekijken? Je kan kiezen uit 2023 t/m 2025. ")
    while year not in ("2023", "2024", "2025"):
        year = input("Ongeldige invoer, ja kan keizen uit 2023 t/m 2025 ")

    race_data = get_race_data(year)
    active_drivers = get_drivers(race_data, year)

    driver = input(
        f"\nVan welke coureur wil je informatie bekijken? Gebruik de afkorting (bijvoorbeeld VER) ").upper().strip()
    while driver not in active_drivers:
        driver = input("Coureur niet gevonden, probeer opnieuw ").upper().strip()
    return active_drivers, driver, race_data, year


def get_race_data(chosen_year):
    params = {'session_name': "Race", "year": chosen_year}
    response = requests.get(f"{URL}/sessions",params=params)

    if response.ok:
        data = response.json()
        race_data_dict = {session["session_key"]: {
            "country_name": session["country_name"], "location": session['location']}
            for session in data}

        return race_data_dict
    else:
        print(f"Fout: {response.status_code} - {response.text}")
        return None

def get_drivers(active_session_keys, year):
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

        table = Table(title=f"\nCoureurs die in {year} hebben gereden:")
        table.add_column("Naam", justify="center")
        table.add_column("Afkorting", justify="center")
        table.add_column("Nummer", justify="center")

        for driver_acronym, values in sorted(driver_dict.items()):
            table.add_row(values["full_name"], driver_acronym, values["driver_number"])

        console = Console()
        console.print(table)

        return driver_dict
    else:
        print(f"Fout: {response.status_code} - {response.text}")
        return None

def show_main_menu(driver, active_drivers, race_data, year):
    driver_full_name = active_drivers[driver]["full_name"]

    print(f"\nJe hebt gekozen voor {driver_full_name} in het jaar {year}.\n"
          f"Welke statistieken wil je bekijken?\n")

    table = Table()
    table.add_column("Keuze", justify="center")
    table.add_column("Actie", justify="center")
    table.add_row("1", "Eindstand van alle races")
    table.add_row("2", "Gemiddelde positie")
    table.add_row("3", "Snelste ronde van het seizoen")
    table.add_row("4", "Aantal podia's (top 3)")
    table.add_row("5", "Vergelijken met andere coureur")
    table.add_row("0", "Terug")

    console = Console()
    console.print(table)

    menu_choice = input("Kies een optie: Kies uit 0 t/m 5 ")
    while menu_choice not in ("0", "1", "2", "3", "4", "5"):
        menu_choice = input("Ongeldige invoer. Kies 0 t/m 5. ")

    match menu_choice:
        case "1":
            show_race_results(driver, driver_full_name, race_data, active_drivers)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "2":
            get_average_position(driver, driver_full_name, race_data, active_drivers)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "3":
            get_fastest_lap(driver, driver_full_name, race_data, active_drivers)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "4":
            get_total_podiums(driver, driver_full_name, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "5":
            compare_drivers(driver, driver_full_name, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "0":
            return

    return driver_full_name

def keep_on_going(driver, driver_full_name, active_drivers, race_data, year):
    choice = input(f"\nWil je meer statistieken bekijken? Ja/nee ").capitalize().strip()
    while choice not in ("Ja", "Nee"):
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
    else:
        print("Bedankt voor het gebruiken van de F1 app!")
        exit(1)

def compare_drivers(driver, driver_full_name, race_data, active_drivers, year):
    active_drivers = get_drivers(race_data, year)

    driver_to_compare = input(f"Met welke coureur wil je {driver_full_name} vergelijken? Gebruik de afkorting (bijvoorbeeld VER) ").upper().strip()
    while driver_to_compare == driver:
        driver_to_compare = input(f"{driver} is al geselecteerd. Kies een andere couruer ").upper().strip()
    while driver_to_compare not in active_drivers:
        driver_to_compare = input("Coureur niet gevonden, probeer opnieuw ").upper().strip()

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
        menu_choice = input("Ongeldige invoer. Kies 0 t/m 4. ")

    match menu_choice:
        case "1":
            compare_race_results(driver, driver_full_name, driver_to_compare, driver_to_compare_full_name, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "2":
            get_average_position(driver, driver_full_name, race_data, active_drivers)
            get_average_position(driver_to_compare, driver_to_compare_full_name, race_data, active_drivers)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "3":
            get_fastest_lap(driver, driver_full_name, race_data, active_drivers)
            get_fastest_lap(driver_to_compare, driver_to_compare_full_name, race_data, active_drivers)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "4":
            get_total_podiums(driver, driver_full_name, race_data, active_drivers, year)
            get_total_podiums(driver_to_compare, driver_to_compare_full_name, race_data, active_drivers, year)
            keep_on_going(driver, driver_full_name, active_drivers, race_data, year)
        case "0":
            return




main()