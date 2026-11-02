import requests
from rich.table import Table
from rich.console import Console

URL = "https://api.openf1.org/v1"

print(f"Welkom bij deze F1 app.\nHier kan je statistieken bekijken, vergelijken en opslaan.\n")

def main():
    year = input("Van welk jaar wil je statistieken bekijken? Je kan kiezen uit 2023 t/m 2025. ")
    while year not in ("2023", "2024", "2025"):
        year = input("Ongeldige invoer, ja kan keizen uit 2023 t/m 2025 ")

    found_keys = get_session_key(year)
    active_drivers = get_drivers(found_keys, year)

    driver = input(f"\nVan welke coureur wil je informatie bekijken? Gebruik de afkorting (bijvoorbeeld VER) ").upper()
    while driver not in active_drivers:
        driver = input("Coureur niet gevonden, probeer opnieuw ").upper()

    print(type(active_drivers))


def get_session_key(chosen_year):
    params = {'session_name': "Race", "year": chosen_year}
    response = requests.get(f"{URL}/sessions",params=params)

    if response.ok:
        data = response.json()
        keys = [session["session_key"] for session in data]
        return keys
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
                acronym = driver_entry["name_acronym"]
                name = driver_entry["full_name"]
                if acronym and name not in driver_dict:
                    driver_dict[acronym] = name

        table = Table(title=f"\nCourers die in {year} hebben gereden:", show_lines=True)
        table.add_column("Naam", justify="center")
        table.add_column("Afkorting", justify="center")
        for acronym, name in sorted(driver_dict.items()):
            table.add_row(name, acronym)
        console = Console()
        console.print(table)

        return driver_dict
    else:
        print(f"Fout: {response.status_code} - {response.text}")
        return None


main()