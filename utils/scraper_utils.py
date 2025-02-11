import json
from typing import List, Set, Tuple
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)
from models.property import Property
import os


def get_browser_config() -> BrowserConfig:
    """
    Returns the browser configuration for the crawler.
    """
    return BrowserConfig(
        browser_type="chromium",
        headless=False,
        verbose=True,
    )


def get_llm_strategy() -> LLMExtractionStrategy:
    """
    Returns the configuration for the language model extraction strategy.
    """
    return LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",
        api_token=os.getenv("GROQ_API_KEY"),
        schema=Property.model_json_schema(),
        extraction_type="schema",
        instruction=(
            "Extract all property listings with 'name', 'price', 'location', and 'description' "
            "from the following content. Ignore irrelevant content."
        ),
        input_format="html",
        verbose=True,
    )


def split_content(content: str, max_length: int = 4000) -> List[str]:
    """
    Splits large content into smaller chunks to fit within the token limit.
    """
    chunks = []
    while len(content) > max_length:
        split_index = content[:max_length].rfind(".") + 1
        if split_index <= 0:
            split_index = max_length
        chunks.append(content[:split_index].strip())
        content = content[split_index:]
    chunks.append(content.strip())
    return chunks


async def fetch_and_process_page(
    crawler: AsyncWebCrawler,
    page_number: int,
    base_url: str,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
    required_keys: List[str],
    seen_names: Set[str],
) -> Tuple[List[dict], bool]:
    """
    Fetches and processes a single page of property data.
    """
    url = f"{base_url}&page={page_number}"
    print(f"Loading page {page_number}...")

    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            css_selector=css_selector,
            session_id=session_id,
        ),
    )

    if not (result.success and result.cleaned_html):
        print(f"Error fetching page {page_number}: {result.error_message}")
        return [], False

    content_chunks = split_content(result.cleaned_html, max_length=4000)

    extracted_data = []
    for chunk in content_chunks:
        llm_result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=llm_strategy,
                session_id=session_id,
                input_data=chunk,
            ),
        )

        if llm_result.success and llm_result.extracted_content:
            extracted_data.extend(json.loads(llm_result.extracted_content))
        else:
            print(f"Error processing chunk: {llm_result.error_message}")

    complete_properties = []
    for prop in extracted_data:
        if not all(key in prop for key in required_keys):
            continue
        if prop["name"] in seen_names:
            print(f"Duplicate property '{prop['name']}' found. Skipping.")
            continue

        seen_names.add(prop["name"])
        complete_properties.append(prop)

    if not complete_properties:
        print(f"No complete properties found on page {page_number}.")
        return [], True

    return complete_properties, False