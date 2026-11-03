import requests
from rich.table import Table
from rich.console import Console

URL = "https://api.openf1.org/v1"


def get_results(driver, active_drivers):
        driver_number = active_drivers[driver]['driver_number']
        params = {"driver_number": driver_number}
        response = requests.get(f"{URL}/session_result", params=params)

        if response.ok:
                all_races = response.json()
                return all_races
        else:
                print(f"Fout: {response.status_code} - {response.text}")
                return None
#
def session_key_to_race_name(race_data, all_races):
        params = {"session_key": race_data}
        response = requests.get(f"{URL}/session_key", params=params)

        if response.ok:
                race_names = response.json()
                print(race_names)
        else:
                print(f"Fout: {response.status_code} - {response.text}")
                return None
