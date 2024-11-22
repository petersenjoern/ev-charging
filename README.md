# EV Charging Tool 🚗⚡

## Overview

The **EV Charging Tool** is a command-line utility designed to help you plan your electric vehicle (EV) charging schedules. By providing information about the remaining battery life, either in kilometers or as a percentage, the tool calculates how long it will take to charge your vehicle and when you need to start charging to be fully charged by a specified time (default is 6 AM).

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
   python main.py -km <remaining_km> [-f <finish_time>]
   # or
   python main.py -p <remaining_percentage> [-f <finish_time>]
   ```

   Replace `<remaining_km>` and `<remaining_percentage>` with your EV's battery status, and optionally specify a different finish time.

## Usage

### Basic Commands

- **Using Remaining Kilometers:**

  ```bash
  python main.py -km 120
  ```

  This command calculates the charging schedule assuming you have 120 kilometers of range remaining until the battery is empty.

- **Using Remaining Percentage:**

  ```bash
  python main.py -p 30
  ```

  Here, you specify that 30% of your battery is still charging.

### Specifying Finish Time

You can also specify when you need to be fully charged by using the `-f` or `--finish_at` option:

```bash
python main.py -km 120 -f "8am"
```

This command calculates how early you should start charging if you want your vehicle to be fully charged by 8 AM.

## Example Output

Running the following command:

```bash
python main.py -p 30 -f "6am"
```

Might produce an output like this:

```
Remaining number of kilometers: 93.0
Remaining battery: 30%
Percentage missing until max 70.0%
There are 28.3 KWh missing until your capacity of 38.0 KWh is reached
Total time to charge: 7:18:00
Assuming you want to be finished charging at 2023-10-14 06:00 with a battery
capacity of almost 100%, you need to start charging by: 2023-10-13 22:41:59
```

## Parameters

- **`-km`, `--remaining_km`:** The remaining range in kilometers until the battery is empty.
- **`-p`, `--remaining_percentage`:** The remaining battery percentage until the battery is empty.
- **`-f`, `--finish_at`:** (Optional) The time by which you want to be fully charged. Default value is "6am".

## Contributing

We welcome contributions! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/your-repo-url/ev-charging).

## License

This project is licensed under the MIT License.

---

Happy charging! 🚗⚡
