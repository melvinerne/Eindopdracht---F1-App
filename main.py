import requests
URL = "https://api.openf1.org/v1"

print(f"Welkom bij deze F1 app.\nHier kan je statistieken bekijken, vergelijken en opslaan.\n")
year = input("Van welk jaar wil je statistieken bekijken? Je kan kiezen uit 2023 t/m 2025. ")

while year not in ("2023", "2024", "2025"):
    year = input("Ongeldige invoer, ja kan keizen uit 2023 t/m 2025 ")

driver = input("Van welke coureur wil je informatie bekijken? ")
    # while driver not in get_drivers(chosen_driver):
    #     driver = input("Coureur niet gevonden, probeer opnieuw")

def choose_year(chosen_year):
    params = {'year': chosen_year}
    response = requests.get(f"{URL}/sessions",params=params)

    if response.ok:
        data = response.json()
        print(data)
        return response.json()
    else:
        print(f"Fout: {response.status_code} - {response.text}")
        return None

def get_drivers(driver):
    params = {'name_acronym': driver}
    response = requests.get(f"{URL}/drivers", params=params)

    if response.ok:
        data = response.json()
        print(data)
    else:
        print(f"Fout: {response.status_code} - {response.text}")
        return None

get_drivers(driver)
