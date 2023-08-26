# ZenMarket Shipping Calculator Automation 🛒🚢🚀

## Introduction ✨

ZenMarket offers a plethora of options for international shipping from Japan, providing customers flexibility and convenience. This repository contains scripts that automate the process of fetching shipping options and prices from ZenMarket based on different package weights and destination countries.

## Table of Contents 📜

- [ZenMarket Shipping Calculator Automation 🛒🚢🚀](#zenmarket-shipping-calculator-automation-)
  - [Introduction ✨](#introduction-)
  - [Table of Contents 📜](#table-of-contents-)
  - [ZenMarket Shipping Methods 🚢](#zenmarket-shipping-methods-)
  - [Script Info 📄](#script-info-)
  - [Setup \& Installation 🛠](#setup--installation-)
  - [Usage 📖](#usage-)
  - [Sample Output 📊](#sample-output-)
  - [Contribute 🤝](#contribute-)
  - [License ✅](#license-)

## ZenMarket Shipping Methods 🚢

ZenMarket provides various methods tailored to different needs:

- **Other Shipping Methods**: Ranging from DHL, SF EXPRESS, EMS to Airmail, SAL, and Pony Express. Costs and times vary based on destination, weight, and size. [Calculator here][2].

- **Savings**: Efficient packing reduces costs with private couriers, ensuring both safety and affordability. [Learn more][3].

## Script Info 📄

1. **generate_country_codes.py**: Scrapes ZenMarket to extract available countries and their respective codes. Outputs to `countries.csv`.
2. **zen_calculator.py**: Utilizes the country codes to fetch shipping options for multiple package weights. Supports both CSV and JSON outputs.

## Setup & Installation 🛠

1. **Prerequisites**:
    - Python 3.x
    - Chrome Browser

2. **Installation**:
    ```bash
    git clone [Repository URL]
    cd [Repository Directory Name]
    pip install -r requirements.txt
    ```

## Usage 📖

1. **Generate Country Codes**:
    ```bash
    python generate_country_codes.py
    ```

2. **Fetch Shipping Options**:
    ```bash
    python zen_calculator.py [COUNTRY_CODE] [WEIGHT1 WEIGHT2 ...] --format [csv/json]
    ```

    **Example**:
    ```bash
    python zen_calculator.py US 500 1000 1500 --format json
    ```

## Sample Output 📊

Here's a snippet from a [sample json](sample.json) from the above example:

```json
{
    "name": "Zen Express: Standard",
    "type": "Standard Parcel",
    "delivery_time": "10-18 days",
    "price": "$13.00 USD"
}
```

## Contribute 🤝

Contributions, issues, and feature requests are welcome! Check the [issues page](https://github.com/gibrankasif/zenmarket-shipping-cal/issues).

## License ✅

Distributed under the GPLv3 License. See `LICENSE` for more information.
