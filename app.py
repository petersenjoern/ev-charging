from typing import Optional

from fasthtml.common import *

from main import (STRFTIME, compute_charging_details, compute_remaining_values,
                  compute_schedule)

app = FastHTML()

TITLE = "EV Charging Tool"
DESCRIPTION = "The tool calculates how long it will take to charge your vehicle and when you need to start charging to be fully charged by a specified time."

count = 0
@app.get("/")
def home():
        input_remaining_km = Input(id="remaining_km", name="remaining_km", type=int, placeholder="Enter remaining km", hx_validate="false")
        input_remaining_percentage = Input(id="remaining_percentage", name="remaining_percentage", type=int, placeholder="Enter remaining battery in %", hx_validate="false")
        input_max_range_km = Input(id="max_range_km", name="max_range_km", type=int, placeholder="Enter max. range (km)")
        input_max_battery_capacity_kwh = Input(id="max_battery_capacity", name="max_battery_capacity_kwh", type=float, placeholder="Enter max. battery (kWh)")
        input_max_charging_rate_kwh = Input(id="max_charging_rate_kwh", name="max_charging_rate_kwh", type=float, placeholder="Enter max. charging rate (kWh)")
        input_finished_at = Input(id="finish_at_str", name="finish_at_str", type=str, placeholder="Enter finish time (6:00)")
        ev_form = Form(method="post", action='/calculate')(
              Fieldset(Label('Remaining km', input_remaining_km)),
              Fieldset(Label('Remaining Battery %', input_remaining_percentage)),
              Fieldset(Label('Range (km)', input_max_range_km)),
              Fieldset(Label('Battery Capacity (kWh)', input_max_battery_capacity_kwh)),
              Fieldset(Label('Charging Rate (kWh)', input_max_charging_rate_kwh)),
              Fieldset(Label('Charging finish by', input_finished_at)),
              Button("Calculate")
        )
        input_finished_at = ()
        return Title(TITLE), Main(
        H1(TITLE),
        H2(DESCRIPTION), ev_form,  cls="container"
    )

@app.post('/calculate')
def calculate(
      remaining_km: None | int = None,
      remaining_percentage: None | int = None,
      max_range_km: int= 310,
      max_battery_capacity_kwh: float = 38.0,
      max_charging_rate_kwh: float = 3.75,
      finish_at_str: str = "6:00"
):
    remaining_km, remaining_perc = compute_remaining_values(remaining_km, remaining_percentage, max_range_km)
    charge_needed, charge_amount, charging_time = compute_charging_details(
        remaining_perc, max_battery_capacity_kwh, max_charging_rate_kwh
    )
    start_at, finish_at = compute_schedule(charging_time, finish_at_str)



    return Main(
    Div(f"Remaining KM: {remaining_km}"),
    Div(f"Remaining Percentage: {remaining_perc}%"),
    Div(f"Charge Needed to Reach 100%: {charge_needed}%"),
    Div(f"Amount of Charge Needed (kWh): {charge_amount} kWh"),
    Div(f"Charging Time Required: {charging_time}"),
    Div(f"Finish Charging At: {finish_at.strftime(STRFTIME)}"),
    Div(f"Start Charging At: {start_at.strftime(STRFTIME)}"),
    )


serve()