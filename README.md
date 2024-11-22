# EV Charging Tool 🚗⚡

## Overview

The **EV Charging Tool** is a command-line utility designed to help you plan your electric vehicle (EV) charging schedules. By providing information about the remaining battery life, either in kilometers or as a percentage, the tool calculates how long it will take to charge your vehicle and when you need to start charging to be fully charged by a specified time.

## Features

- **Calculate Charging Time:** Determine the total charging duration based on the current battery status.
- **Determine Start Time:** Find out when to begin charging to reach full capacity by a desired completion time.
- **Flexible Input Options:** Enter remaining range either in kilometers or as a percentage of battery life.

## Installation

To use the EV Charging CLI, you need Python 3.x installed on your system. Here’s how you can set up and run the tool:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-repo-url/ev-charging.git
   cd ev-charging
   ```

2. **Run the Script Directly:**

   You can execute the script using Python:

   ```bash

   python main.py -km <remaining_km> --max_battery_capacity_kwh <capacity> --max_charging_rate_kwh <rate> --max_range_km <range>
   # or
   python main.py -p <remaining_percentage> --max_battery_capacity_kwh <capacity> --max_charging_rate_kwh <rate> --max_range_km <range>
   ```

   Replace `<remaining_km>` and `<remaining_percentage>` with your EV's battery status, and optionally specify a different finish time.

## Usage

### Basic Commands

- **Using Remaining Kilometers:**

  ```bash
  python main.py -km 120 --max_battery_capacity_kwh 38 --max_charging_rate_kwh 3.8 --max_range_km 310 -f 6:00
  ```

  This command calculates the charging schedule assuming you have 120 kilometers of range remaining until the battery is empty and you want to have your EV charged fully charged by 6 AM.

- **Using Remaining Percentage:**

  ```bash
  python main.py -p 30 --max_battery_capacity_kwh 38 --max_charging_rate_kwh 3.8 --max_range_km 310 -f 6:00
  ```

  Here, you specify that 30% of your battery is still remaining.

## Example Output

Running the following command:

```bash
python main.py -p 30 --max_battery_capacity_kwh 38 --max_charging_rate_kwh 3.8 --max_range_km 310 -f 6:00
```

Might produce an output like this:

```
Remaining KM: 124.0
Remaining Percentage: 40.0%
Charge Needed to Reach 100%: 60.0%
Amount of Charge Needed (kWh): 22.8 kWh
Charging Time Required: 6:00:00
Finish Charging At: 2024-11-23 06:00
Start Charging At: 2024-11-23 00:00
```

## Parameters

- **`-km`, `--remaining_km`:** The remaining range in kilometers until the battery is empty.
- **`-p`, `--remaining_percentage`:** The remaining battery percentage until the battery is empty.
- **`-f`, `--finish_at`:** The time by which you want to be fully charged.

## Contributing

We welcome contributions! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/your-repo-url/ev-charging).

## License

This project is licensed under the MIT License.

---

Happy charging! 🚗⚡
