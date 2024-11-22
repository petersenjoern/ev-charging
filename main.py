import argparse
from datetime import timedelta, datetime


MAX_BATTERY_CAPACITY_KWH=38.0
MAX_CHARGING_KWH=3.8
MAX_RANGE_KM=310
STRFTIME="%Y-%m-%d %H:%M"

def main() -> None:
    parser = argparse.ArgumentParser(description="A CLI to calculate EV charging schedules")
    parser.add_argument("-km","--remaining_km", type=int, help="Remaining number of Kilometers, until battery is empty")
    parser.add_argument("-p", "--remaining_percentage", type=int, help="Remaining battery percentage, until battery is empty")
    parser.add_argument("-f", "--finish_at", type=str, default="6am", help="Time at when the charge is expected to be finished")
    args = parser.parse_args()

    if not args.remaining_km and not args.remaining_percentage:
        raise Exception("You have to at least provide remaining kilometers (-km) or remaining percentage (-p)!")

    remaining_km = args.remaining_km if args.remaining_km else percentage_to_km(args.remaining_percentage)
    remaining_perc = args.remaining_percentage if args.remaining_percentage else km_to_percentage(args.remaining_km)
    charge_needed = percentage_to_max(remaining_perc)
    charge_amount = current_perc_as_missing_kwh(charge_needed)
    charging_time = get_charging_time(charge_amount)

    finish_at = get_finish_at()
    start_at = get_start_time(charging_time, finish_at)

    finish_at_str = finish_at.strftime(STRFTIME)
    start_at_str = start_at.strftime(STRFTIME)
        

    print(f"Remaining number of kilometers: {remaining_km}") 
    print(f"Remaining battery: {remaining_perc}%")
    print(f"Percentage missing until max {charge_needed}%")
    print(f"There are {charge_amount} KWh missing until your capacity of {MAX_BATTERY_CAPACITY_KWH} KWh is reached")
    print(f"Total time to charge: {charging_time}")
    print(f"""Assuming you want to be finished charging at {finish_at_str} with a battery
capacity of almost 100%, you need to start charging by: {start_at_str}""")

def current_km_to_max(current: int, _max: int = MAX_RANGE_KM) -> int:
    return _max - current

def km_to_percentage(km: int, max_range: int = MAX_RANGE_KM) -> int:
    perc = (km / max_range) * 100
    return round(perc,1)

def percentage_to_km(percentage: float, max_range: int = MAX_RANGE_KM) -> int:
    km = (max_range * percentage) / 100
    return round(km, 0)

def percentage_to_max(percentage: float, max_percentage: float = 100.0) -> float:
    return max_percentage - percentage

def current_perc_as_missing_kwh(percentage: float, max_kwh: float = MAX_BATTERY_CAPACITY_KWH) -> float:
    return (percentage / 100) * max_kwh

def get_charging_time(kwh: float, charging_rate_kwh: float = MAX_CHARGING_KWH) -> timedelta:
    charging_time_hours = kwh / charging_rate_kwh
    return timedelta(hours=charging_time_hours)

def get_finish_at() -> datetime:
    tomorrow = datetime.today() + timedelta(days=1)
    tomorrow_at_6am = tomorrow.replace(hour=6, minute=10, second=0)
    return tomorrow_at_6am

def get_start_time(charge_time: timedelta, finish_at: datetime) -> datetime:
    return finish_at - charge_time


def current_percentage_to_max(current: float, _max: float = 100) -> float:
    return _max - current

if __name__ == "__main__":
    main()