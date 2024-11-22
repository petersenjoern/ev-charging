import argparse
from datetime import timedelta

import pytest

from main import (compute_charging_details, compute_remaining_values,
                  compute_schedule, get_finish_at, km_to_percentage,
                  percentage_to_km)


def _assert_time_equal(t1, t2):
    assert (
        t1.year == t2.year
        and t1.month == t2.month
        and t1.day == t2.day
        and t1.hour == t2.hour
        and t1.minute == t2.minute
    ), f"Times not equal: {t1} != {t2}"


@pytest.mark.parametrize(
    "remaining_km, remaining_percentage, max_range_km, expected",
    [
        (None, 50.0, 400, (200, 50.0)),
        (100, None, 400, (100, 25.0)),
        (100, 50.0, 400, (100, 50.0)),  # Both provided
    ],
)
def test_compute_remaining_values(
    remaining_km, remaining_percentage, max_range_km, expected
):
    args = argparse.Namespace(
        remaining_km=remaining_km,
        remaining_percentage=remaining_percentage,
        max_battery_capacity_kwh=50.0,
        max_charging_rate_kwh=10.0,
        max_range_km=max_range_km,
    )
    assert compute_remaining_values(args) == expected


@pytest.mark.parametrize(
    "remaining_perc, max_battery_capacity_kwh, expected",
    [
        (50.0, 50.0, (50.0, 25.0, timedelta(hours=2.5))),
        (30.0, 70.0, (70.0, 49.0, timedelta(hours=4.9))),
    ],
)
def test_compute_charging_details(remaining_perc, max_battery_capacity_kwh, expected):
    args = argparse.Namespace(
        remaining_km=None,
        remaining_percentage=None,
        max_battery_capacity_kwh=max_battery_capacity_kwh,
        max_charging_rate_kwh=10.0,
        max_range_km=400,
    )
    assert compute_charging_details(remaining_perc, args) == expected


@pytest.mark.parametrize(
    "charging_time_str, finish_at_str, expected_start_str",
    [
        ("2.5", "6:00", "15:30"),
        (
            "4.9",
            "6:00",
            "21:10",
        ),  # This example assumes a precise timedelta of 4 hours and 54 minutes
    ],
)
def test_compute_schedule(charging_time_str, finish_at_str, expected_start_str):
    charging_time = timedelta(hours=float(charging_time_str))
    finish_at = get_finish_at(finish_at_str)
    start_at, _ = compute_schedule(charging_time, finish_at_str)
    _assert_time_equal(
        start_at.replace(second=0, microsecond=0), finish_at - charging_time
    )


@pytest.mark.parametrize(
    "km, max_range_km, expected",
    [
        (200, 400, 50.0),
        (100, 400, 25.0),
    ],
)
def test_km_to_percentage(km, max_range_km, expected):
    assert km_to_percentage(km, max_range_km) == expected


@pytest.mark.parametrize(
    "percentage, max_range_km, expected",
    [
        (50.0, 400, 200),
        (25.0, 400, 100),
    ],
)
def test_percentage_to_km(percentage, max_range_km, expected):
    assert percentage_to_km(percentage, max_range_km) == expected


def test_compute_charging_details_zero_remaining():
    args = argparse.Namespace(
        remaining_km=None,
        remaining_percentage=0.0,
        max_battery_capacity_kwh=50.0,
        max_charging_rate_kwh=10.0,
        max_range_km=400,
    )
    assert compute_charging_details(0.0, args) == (100.0, 50.0, timedelta(hours=5.0))


def test_compute_charging_details_full_remaining():
    args = argparse.Namespace(
        remaining_km=None,
        remaining_percentage=100.0,
        max_battery_capacity_kwh=50.0,
        max_charging_rate_kwh=10.0,
        max_range_km=400,
    )
    assert compute_charging_details(100.0, args) == (0.0, 0.0, timedelta(hours=0))


# Run the tests
if __name__ == "__main__":
    import sys 
    pytest.main(sys.argv)
