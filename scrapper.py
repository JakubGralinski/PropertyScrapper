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

# -------------------------------
# CONFIGURATION
# -------------------------------
HOST_URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa"
LISTINGS_CONTAINER_CLASS = "css-1pkwj40"  # **UPDATE THIS if needed**


# -------------------------------
# INITIALIZE CHROME WEBDRIVER (WITH ANTI-DETECTION)
# -------------------------------
def init_chrome_driver():
    """
    Initialize the Chrome WebDriver with anti-detection techniques.
    """
    chrome_options = Options()

    # ✅ Remove headless mode for debugging (enable headless for automation)
    # chrome_options.add_argument("--headless")  # Comment this for debugging

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # 🛡️ Anti-bot detection bypass
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # 🔄 Rotate Random User-Agent
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    random_user_agent = random.choice(USER_AGENTS)
    chrome_options.add_argument(f"user-agent={random_user_agent}")

    # 🌎 Set a Referrer (makes request look real)
    chrome_options.add_argument("referer=https://www.google.com/")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(10)  # Allow elements to load
    return driver


# -------------------------------
# DISMISS COOKIE BANNER
# -------------------------------
def dismiss_cookie_banner(driver):
    """
    Dismiss the cookie banner.
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
# SCROLL TO LOAD LISTINGS
# -------------------------------
def scroll_to_load(driver):
    """
    Scrolls multiple times to load more listings.
    """
    for _ in range(5):  # Adjust this if needed
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow JavaScript to load


# -------------------------------
# LOAD PAGE AND WAIT FOR LISTINGS
# -------------------------------
def get_listings(driver, url):
    """
    Opens URL, dismisses cookie banner, scrolls, and returns parsed HTML.
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
# EXTRACT LISTINGS
# -------------------------------
def extract_listings(soup):
    """
    Extracts real estate listings from the parsed HTML.
    """
    listings = []

    container = soup.find("div", class_=LISTINGS_CONTAINER_CLASS)
    if not container:
        print("❌ Listing container not found.")
        return listings

    for listing in container.find_all("div", class_="css-19ucd76"):  # **UPDATE THIS CLASS if needed**
        title = listing.find("h3").text.strip() if listing.find("h3") else "No title"
        price = listing.find("span", class_="css-1wi2w6s").text.strip() if listing.find("span",
                                                                                        class_="css-1wi2w6s") else "No price"
        location = listing.find("p", class_="css-1pgwcoa").text.strip() if listing.find("p",
                                                                                        class_="css-1pgwcoa") else "No location"

        listings.append({"title": title, "price": price, "location": location})

    return listings


# -------------------------------
# SAVE TO JSON
# -------------------------------
def save_to_json(data, filename="listings.json"):
    """
    Saves extracted listings to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# -------------------------------
# MAIN FUNCTION - SCRAPER LOGIC
# -------------------------------
def scrape_otodom():
    """
    Runs the scraper and saves listings to JSON.
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


# -------------------------------
# RUN THE SCRAPER
# -------------------------------
if __name__ == "__main__":
    scrape_otodom()