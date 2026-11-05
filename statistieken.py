import requests
from rich import print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

URL = "https://api.openf1.org/v1"


def get_race_results(driver, race_data, active_drivers):
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
                return race_results_dict
        else:
                print(f"Fout: {response.status_code} - {response.text}")
                return None

def show_race_results(driver, driver_full_name, race_data, active_drivers):
        race_results_dict = get_race_results(driver, race_data, active_drivers)

        table = Table(title=f"\nEindstand per race van {driver_full_name}:", show_lines=True)
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

def get_average_position(driver, driver_full_name, race_data, active_drivers):
    race_results_dict = get_race_results(driver, race_data, active_drivers)
    total_positions = 0
    races_completed = 0

    for race in race_results_dict:
        position = race["position"]
        if isinstance(position, int):
                total_positions += position
                races_completed += 1

    average_position = total_positions / races_completed
    print(f"\nDe gemiddelde positie van {driver_full_name} was {average_position:.2f}.")

    return average_position

def get_fastest_lap(driver, driver_full_name, race_data, active_drivers):
    driver_number = active_drivers[driver]['driver_number']

    params = {"driver_number": driver_number}
    response = requests.get(f"{URL}/laps", params=params)

    if response.ok:
        lap_data = response.json()
        fastest_lap_per_session = {}

        for lap in lap_data:
            session_key = lap["session_key"]
            lap_duration = lap["lap_duration"]

            if session_key in race_data and lap_duration is not None:
                if lap_duration not in fastest_lap_per_session:
                    fastest_lap_per_session[session_key] = lap_duration
                else:
                    if lap_duration < fastest_lap_per_session[session_key]:
                        fastest_lap_per_session = lap_duration

        fastest_lap = min(fastest_lap_per_session.values())
        fastest_session_key = min(fastest_lap_per_session, key=fastest_lap_per_session.get)
        country = race_data[fastest_session_key]["country_name"]
        circuit = race_data[fastest_session_key]["location"]
        print(Panel.fit(f"De snelste ronde van {driver_full_name} is {fastest_lap} in {country} - {circuit}"))

    else:
        print(f"Fout: {response.status_code} - {response.text}")
        return None
