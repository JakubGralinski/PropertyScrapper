# config.py

BASE_URL = "https://www.zoopla.co.uk/for-sale/property/london/?q=London&search_source=home"
CSS_SELECTOR = ".listing-results-wrapper"  # Updated CSS selector for property listings
REQUIRED_KEYS = [
    "name",
    "price",
    "location",
    "description",
]