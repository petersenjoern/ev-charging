import argparse
from datetime import datetime, timedelta

STRFTIME = "%Y-%m-%d %H:%M"


def main():
    args = parse_arguments()
    remaining_km, remaining_perc = compute_remaining_values(args.remaining_km, args.remaining_percentage, args.max_range_km)
    charge_needed, charge_amount, charging_time = compute_charging_details(
        remaining_perc, args.max_battery_capacity_kwh, args.max_charging_rate_kwh
    )
    start_at, finish_at = compute_schedule(charging_time, args.finish_at)
    print_results(
        remaining_km,
        remaining_perc,
        charge_needed,
        charge_amount,
        charging_time,
        finish_at,
        start_at,
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="A CLI to calculate EV charging schedules"
    )
    parser.add_argument(
        "-km",
        "--remaining_km",
        type=int,
        help="Remaining number of Kilometers, until battery is empty",
    )
    parser.add_argument(
        "-p",
        "--remaining_percentage",
        type=float,
        help="Remaining battery percentage, until battery is empty",
    )
    parser.add_argument(
        "-f",
        "--finish_at",
        type=str,
        default="6:00",
        help="Time at when the charge is expected to be finished",
    )
    parser.add_argument(
        "--max_battery_capacity_kwh",
        type=float,
        required=True,
        help="Maximum battery capacity in KWh",
    )
    parser.add_argument(
        "--max_charging_rate_kwh",
        type=float,
        required=True,
        help="Max charging rate in KWh per hour",
    )
    parser.add_argument(
        "--max_range_km",
        type=int,
        required=True,
        help="Maximum range of the vehicle in kilometers",
    )
    return parser.parse_args()


def compute_remaining_values(remaining_km, remaining_percentage, max_range_km) -> tuple[int, float]:
    if not remaining_km and not remaining_percentage:
        raise ValueError(
            "You have to at least provide remaining kilometers (-km) or remaining percentage (-p)!"
        )

    remaining_km = (
        remaining_km
        if remaining_km
        else percentage_to_km(remaining_percentage, max_range_km)
    )
    remaining_perc = (
        remaining_percentage
        if remaining_percentage
        else km_to_percentage(remaining_km, max_range_km)
    )
    return remaining_km, remaining_perc


def compute_charging_details(remaining_perc: float, max_battery_capacity_kwh, max_charging_rate_kwh) -> tuple[float, float, timedelta]:
    charge_needed = percentage_to_max(remaining_perc)
    charge_amount = current_perc_as_missing_kwh(
        charge_needed, max_battery_capacity_kwh
    )
    charging_time = get_charging_time(charge_amount, max_charging_rate_kwh)
    return charge_needed, charge_amount, charging_time


def compute_schedule(
    charging_time: timedelta, finish_at_str: str
) -> tuple[datetime, datetime]:
    finish_at = get_finish_at(finish_at_str)
    start_at = get_start_time(charging_time, finish_at)
    return start_at, finish_at


def print_results(
    remaining_km,
    remaining_perc,
    charge_needed,
    charge_amount,
    charging_time,
    finish_at,
    start_at,
):
    print(f"Remaining KM: {remaining_km}")
    print(f"Remaining Percentage: {remaining_perc}%")
    print(f"Charge Needed to Reach 100%: {charge_needed}%")
    print(f"Amount of Charge Needed (kWh): {charge_amount} kWh")
    print(f"Charging Time Required: {charging_time}")
    print(f"Finish Charging At: {finish_at.strftime(STRFTIME)}")
    print(f"Start Charging At: {start_at.strftime(STRFTIME)}")


def km_to_percentage(km: int, max_range: int) -> float:
    return round((km / max_range) * 100, 1)


def percentage_to_km(percentage: float, max_range: int) -> int:
    return round((max_range * percentage) / 100, 0)


def percentage_to_max(percentage: float) -> float:
    return 100 - percentage


def current_perc_as_missing_kwh(percentage: float, max_kwh: float) -> float:
    return (percentage / 100) * max_kwh


def get_charging_time(kwh: float, charging_rate_kwh: float) -> timedelta:
    return timedelta(hours=kwh / charging_rate_kwh)


def get_finish_at(finish_time_str: str) -> datetime:
    tomorrow = datetime.today() + timedelta(days=1)
    hour, minute = map(int, finish_time_str.split(":"))
    return tomorrow.replace(hour=hour, minute=minute, second=0)


def get_start_time(charge_time: timedelta, finish_at: datetime) -> datetime:
    return finish_at - charge_time


if __name__ == "__main__":
    main()
