import csv
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def get_country_options():
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    driver = uc.Chrome(options=options)

    driver.get("https://zenmarket.jp/calc.aspx")

    WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, "ddlCountry")))
    country_select = Select(driver.find_element(By.ID, "ddlCountry"))

    country_options = [(option.get_attribute('value'), option.text) for option in country_select.options]

    driver.quit()
    return country_options

def save_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Country Code', 'Country Name'])
        writer.writerows(data)

def main():
    country_options = get_country_options()
    save_to_csv("countries.csv", country_options)
    print(f"Extracted {len(country_options)} countries and saved to countries.csv")

if __name__ == "__main__":
    main()
