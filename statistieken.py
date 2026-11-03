import requests
from rich.table import Table
from rich.console import Console

URL = "https://api.openf1.org/v1"


def get_results(driver, race_data, active_drivers):
        driver_number = active_drivers[driver]['driver_number']
        params = {"driver_number": driver_number}
        response = requests.get(f"{URL}/session_result", params=params)

        if response.ok:
                all_races = response.json()
                race_results_dict = []

                for race in all_races:
                        if race["session_key"] in race_data:
                                country = race_data[race["session_key"]]["country_name"]
                                location = race_data[race["session_key"]]["location"]
                                position = race["position"]
                                new_entry = {
                                        "Race name": country,
                                        "Location": location,
                                        "position": position
                                }
                                race_results_dict.append(new_entry)

                print(race_results_dict)

                table = Table(title=f"\nEindstand per race van {driver}:", show_lines=True)

                table.add_column("Race naam", justify="left")
                table.add_column("End position", justify="center")

                for races in race_results_dict:
                        race_name_combined = f"{races['Race name']} - {races['Location']}"
                        table.add_row(
                                race_name_combined,
                                str(races["position"])
                        )
                console = Console()
                console.print(table)

        else:
                print(f"Fout: {response.status_code} - {response.text}")
                return None
