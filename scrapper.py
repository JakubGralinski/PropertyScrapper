import os
import time
import json
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium_stealth import stealth  # Import stealth to bypass bot detection

# -------------------------------
# Configuration
# -------------------------------
HOST_URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa"
LISTINGS_CONTAINER_CLASS = "css-1pkwj40"  # **UPDATE** based on site inspection!


# -------------------------------
# Initialize Chrome WebDriver
# -------------------------------
def init_chrome_driver():
    """
    Initialize the Chrome WebDriver with stealth mode.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without opening browser
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-infobars")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Apply stealth mode
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.implicitly_wait(10)  # Allow elements to load
    return driver


# -------------------------------
# Dismiss Cookie Banner
# -------------------------------
def dismiss_cookie_banner(driver):
    """
    Dismiss the cookie banner by clicking "Akceptuję".
    """
    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Akceptuję')]"))
        )
        accept_button.click()
        print("✅ Cookie banner dismissed.")
    except Exception:
        print("⚠️ Cookie banner not found or already dismissed.")


# -------------------------------
# Scroll Down and Wait for JavaScript
# -------------------------------
def scroll_to_load(driver):
    """
    Scroll multiple times to trigger lazy loading of listings.
    """
    for _ in range(5):  # Adjust if needed
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 5))  # Randomized delay to avoid detection


# -------------------------------
# Get Page and Wait for Listings
# -------------------------------
def get_listings(driver, url):
    """
    Navigate to the given URL, dismiss cookie banner, scroll, and return BeautifulSoup object.
    """
    driver.get(url)
    dismiss_cookie_banner(driver)
    scroll_to_load(driver)

    try:
        # ✅ Wait for JavaScript-rendered listings to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, LISTINGS_CONTAINER_CLASS))
        )
        print("✅ Listings successfully loaded.")
    except Exception:
        print("❌ Listings did not load in time.")
        print("📜 Debugging Page Source:\n")
        print(driver.page_source[:5000])  # Print for debugging
        return None

    return BeautifulSoup(driver.page_source, "html.parser")


# -------------------------------
# Extract Listings
# -------------------------------
def extract_listings(soup):
    """
    Extract listings from the parsed HTML.
    """
    listings = []

    container = soup.find("div", class_=LISTINGS_CONTAINER_CLASS)
    if not container:
        print("❌ Listing container not found.")
        return listings

    for listing in container.find_all("div", class_="css-19ucd76"):  # **UPDATE** based on site inspection!
        title = listing.find("h3").text.strip() if listing.find("h3") else "No title"
        price = listing.find("span", class_="css-1wi2w6s").text.strip() if listing.find("span",
                                                                                        class_="css-1wi2w6s") else "No price"
        location = listing.find("p", class_="css-1pgwcoa").text.strip() if listing.find("p",
                                                                                        class_="css-1pgwcoa") else "No location"

        listings.append({"title": title, "price": price, "location": location})

    return listings


# -------------------------------
# Save to JSON
# -------------------------------
def save_to_json(data, filename="listings.json"):
    """
    Save listings to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# -------------------------------
# Main Function
# -------------------------------
def scrape_otodom():
    """
    Main function to scrape Otodom listings.
    """
    driver = init_chrome_driver()
    try:
        soup = get_listings(driver, HOST_URL)
        if soup:
            listings = extract_listings(soup)
            print(f"✅ Found {len(listings)} listings.")
            save_to_json(listings)
            print("💾 Listings saved to listings.json.")
    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_otodom()