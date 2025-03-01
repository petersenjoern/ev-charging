import modal

from main import (
    STRFTIME,
    compute_charging_details,
    compute_remaining_values,
    compute_schedule,
)

TITLE = "EV Charging Tool"
DESCRIPTION = """The tool calculates how long it will
take to charge your vehicle and when you need to start charging to be fully
charged by a specified time."""

app = modal.App("ev-charging")
image = modal.Image.debian_slim(python_version="3.12").pip_install(
    "python-fasthtml==0.10.0"
)


@app.function(image=image)
@modal.asgi_app()
def serve():
    import fasthtml.common as fh

    app = fh.FastHTML()

    count = 0

    @app.get("/")
    def home():
        input_remaining_km = fh.Input(
            id="remaining_km",
            name="remaining_km",
            type=int,
            placeholder="Enter remaining km",
            hx_validate="false",
        )
        input_remaining_percentage = fh.Input(
            id="remaining_percentage",
            name="remaining_percentage",
            type=int,
            placeholder="Enter remaining battery in %",
            hx_validate="false",
        )
        input_max_range_km = fh.Input(
            id="max_range_km",
            name="max_range_km",
            type=int,
            placeholder="Enter max. range (km)",
            hx_validate="false",
            value=300,
        )
        input_max_battery_capacity_kwh = fh.Input(
            id="max_battery_capacity",
            name="max_battery_capacity_kwh",
            type=float,
            placeholder="Enter max. battery (kWh)",
            hx_validate="false",
            value=38.0,
        )
        input_max_charging_rate_kwh = fh.Input(
            id="max_charging_rate_kwh",
            name="max_charging_rate_kwh",
            type=float,
            placeholder="Enter max. charging rate (kWh)",
            hx_validate="false",
            value=3.65,
        )
        input_finished_at = fh.Input(
            id="finish_at_str",
            name="finish_at_str",
            type="time",
            placeholder="Enter finish time (6:00)",
            hx_validate="true",
            value="06:00",
        )
        ev_form = fh.Form(method="post", action="/calculate")(
            fh.Fieldset(fh.Label("Remaining km", input_remaining_km)),
            fh.Fieldset(fh.Label("Remaining Battery %", input_remaining_percentage)),
            fh.Fieldset(fh.Label("Range (km)", input_max_range_km)),
            fh.Fieldset(
                fh.Label("Battery Capacity (kWh)", input_max_battery_capacity_kwh)
            ),
            fh.Fieldset(fh.Label("Charging Rate (kWh)", input_max_charging_rate_kwh)),
            fh.Fieldset(fh.Label("Charging finish by", input_finished_at)),
            fh.Button("Calculate"),
        )
        input_finished_at = ()
        return fh.Title(TITLE), fh.Main(
            fh.H1(TITLE), fh.H2(DESCRIPTION), ev_form, cls="container"
        )

    @app.post("/calculate")
    def calculate(
        remaining_km: None | int = None,
        remaining_percentage: None | int = None,
        max_range_km: int = 310,
        max_battery_capacity_kwh: float = 38.0,
        max_charging_rate_kwh: float = 3.75,
        finish_at_str: str = "6:00",
    ):
        remaining_km, remaining_perc = compute_remaining_values(
            remaining_km, remaining_percentage, max_range_km
        )
        charge_needed, charge_amount, charging_time = compute_charging_details(
            remaining_perc, max_battery_capacity_kwh, max_charging_rate_kwh
        )
        start_at, finish_at = compute_schedule(charging_time, finish_at_str)

        return fh.Main(
            fh.Div(f"Start Charging At: {start_at.strftime(STRFTIME)}"),
            fh.Div(f"Finish Charging At: {finish_at.strftime(STRFTIME)}"),
            fh.Div(f"Charging Time Required: {charging_time}"),
            fh.Div(f"Amount of Charge Needed (kWh): {charge_amount} kWh"),
            fh.Div(f"Charge Needed to Reach 100%: {charge_needed}%"),
            fh.Div(f"Remaining KM: {remaining_km}"),
            fh.Div(f"Remaining Percentage: {remaining_perc}%"),
        )

    return app
