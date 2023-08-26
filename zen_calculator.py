import argparse
import os
import csv
import json
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

import re

# Pattern to match dollar amounts
dollar_pattern = re.compile(r'\$\d+(\.\d{2})?\s*USD')

def adjust_pricing(data):
    for entry in data:
        if entry['restrictions'] and dollar_pattern.match(entry['restrictions'][-1]):
            entry['price'] = entry['restrictions'].pop()
    return data

def is_valid_country_code(country_code):
    """Check if the provided country code exists in the CSV file."""
    with open("countries.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            if country_code == row[0]:  # Match with the country code column
                return True
    return False

def get_shipping_options(country_code, weight):
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    driver = uc.Chrome(options=options)
    driver.get("https://zenmarket.jp/calc.aspx")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddlCountry")))
    country_select = Select(driver.find_element(By.ID, "ddlCountry"))
    country_select.select_by_value(country_code)  # Selecting by country code

    weight_field = driver.find_element(By.ID, "tbxWeight")
    weight_field.send_keys(str(weight))

    # Wait for the modal to appear and close it
    try:
        close_modal = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="#" and @data-dismiss="modal" and text()="No, thanks"]'))
        )
        driver.execute_script("arguments[0].click();", close_modal)
    except:
        print("No modal found or couldn't close it.")

    shipping_options_content = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.equal"))
    ).get_attribute('outerHTML')

    driver.quit()
    return shipping_options_content

def extract_shipping_details(option_div, weight, identifier):
    text_elements = [div.text.strip() for div in option_div.find_all("div") if div.text.strip()]
    price = None
    for text in text_elements:
        if dollar_pattern.match(text):
            price = text
            break

    # If there's no price, return None (will be filtered out later)
    if not price:
        return None

    details = {
        "package": identifier,
        "weight": weight,
        "courier": text_elements[0] if len(text_elements) > 0 else None,
        "price": price,
        "delivery_time": text_elements[2] if len(text_elements) > 2 else None,
    }
    return details

def export_combined_to_file(data, country_code, file_format="csv"):
    filename = f"combined_shipping_options_{country_code}.{file_format}"
    if file_format == "csv":
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["package", "weight", "courier", "price", "delivery_time"])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    elif file_format == "json":
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data exported to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Retrieve shipping options based on country and weight.")
    parser.add_argument("country_code", type=str, help="Country code e.g., US, CA, AU.")
    parser.add_argument("weights", nargs='+', type=int, help="List of weights e.g., 500 1000 1500.")
    parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Output format: csv or json. Default is csv.")

    args = parser.parse_args()
    country_code = args.country_code.upper()
    weights = args.weights
    file_format = args.format

    # Check if countries.csv exists
    if not os.path.exists("countries.csv"):
        print("Error: The 'countries.csv' file does not exist. Please run generate_country_codes.py to generate it.")
        return

    if not is_valid_country_code(country_code):
        print(f"Error: The country code '{country_code}' is not valid or not found in the CSV file.")
        return

    combined_data = []
    identifier_counter = 1  # Start with oly1

    for weight in weights:
        shipping_options_content = get_shipping_options(country_code, weight)
        soup = BeautifulSoup(shipping_options_content, 'html.parser')
        shipping_option_divs = soup.find_all("div", class_="col-md-15 col-sm-3 sm-panel")
        all_shipping_details = [extract_shipping_details(div, weight, f"oly{identifier_counter}") for div in shipping_option_divs]

        # Filter out None values (no price options)
        all_shipping_details = [details for details in all_shipping_details if details]
        combined_data.extend(all_shipping_details)

        print(f"Shipping options for {country_code} at {weight}g:")
        for details in all_shipping_details:
            print(details)

        identifier_counter += 1  # Increment for the next weight

    export_combined_to_file(combined_data, country_code, file_format)

if __name__ == "__main__":
    main()
