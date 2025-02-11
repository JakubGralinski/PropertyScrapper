import asyncio
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv
from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.data_utils import save_properties_to_csv
from utils.scraper_utils import fetch_and_process_page, get_browser_config, get_llm_strategy

load_dotenv()


async def crawl_properties():
    """
    Main function to crawl property data from the website.
    """
    # Initialize configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "property_crawl_session"

    # Initialize state variables
    page_number = 1
    all_properties = []
    seen_names = set()

    # Start the web crawler context
    async with AsyncWebCrawler(config=browser_config) as crawler:
        while True:
            properties, no_results_found = await fetch_and_process_page(
                crawler,
                page_number,
                BASE_URL,
                CSS_SELECTOR,
                llm_strategy,
                session_id,
                REQUIRED_KEYS,
                seen_names,
            )

            if no_results_found:
                print("No more properties found. Ending crawl.")
                break

            if not properties:
                print(f"No properties extracted from page {page_number}.")
                break

            all_properties.extend(properties)
            page_number += 1

            # Pause between requests to avoid being rate-limited
            await asyncio.sleep(2)

    # Save the collected properties to a CSV file
    if all_properties:
        save_properties_to_csv(all_properties, "properties.csv")
        print(f"Saved {len(all_properties)} properties to 'properties.csv'.")
    else:
        print("No properties were found during the crawl.")


async def main():
    """
    Entry point of the script.
    """
    await crawl_properties()


if __name__ == "__main__":
    asyncio.run(main())