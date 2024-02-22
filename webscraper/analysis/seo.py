from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import re
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import setup_logger

seo_logger = setup_logger("seo_logger", "seo_analysis.log")

def fetch_soup_selenium(url):
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    service = Service(ChromeDriverManager().install())

    try:
        with webdriver.Chrome(service=service, options=options) as driver:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            return soup
    except Exception as e:
        seo_logger.error(f"Error fetching page with Selenium for {url}: {e}")
        return None

def analyze_image_alt_tags(soup):
    images = soup.find_all("img")
    images_with_alt = [img for img in images if "alt" in img.attrs]
    return len(images), len(images_with_alt)

def analyze_url_structure(url):
    if re.match(r"https?://[www\.]?[a-z0-9.-]+\.[a-z]{2,}", url):
        return "SEO Friendly"
    return "Not SEO Friendly"

def analyze_schema_markup(soup):
    schema_scripts = soup.find_all("script", type="application/ld+json")
    return bool(schema_scripts)

def on_page_seo_analysis(url, soup):
    total_images, images_with_alt = analyze_image_alt_tags(soup)
    url_structure = analyze_url_structure(url)
    has_schema_markup = analyze_schema_markup(soup)

    return {
        "total_images": total_images,
        "images_with_alt_tags": images_with_alt,
        "url_structure": url_structure,
        "schema_markup_present": has_schema_markup,
    }

def check_ssl_certificate(url):
    return url.startswith("https://")

def check_mobile_friendliness(soup):
    viewport_meta = soup.find("meta", {"name": "viewport"})
    return bool(viewport_meta)

def analyze_content_quality(soup):
    word_count = len(soup.get_text().split())
    return word_count

def technical_seo_analysis(url, soup):
    ssl_cert = check_ssl_certificate(url)
    mobile_friendly = check_mobile_friendliness(soup)
    word_count = analyze_content_quality(soup)

    return {
        "ssl_certificate": ssl_cert,
        "mobile_friendliness": mobile_friendly,
        "word_count": word_count,
    }

def analyze_seo(url):
    seo_logger.info(f"Starting SEO analysis for {url}")
    soup = fetch_soup_selenium(url)
    if not soup:
        return {}

    on_page_seo_data = on_page_seo_analysis(url, soup)
    technical_seo_data = technical_seo_analysis(url, soup)

    seo_report = {
        "on_page_seo": on_page_seo_data,
        "technical_seo": technical_seo_data,
        "seo_status": {
            "basic_seo_score": 1,
            "basic_seo_details": [
                {"id": "viewport", "weight": 1, "group": "seo-mobile"},
                {"id": "document-title", "weight": 1, "group": "seo-content"},
                {"id": "meta-description", "weight": 1, "group": "seo-content"},
                {"id": "http-status-code", "weight": 1, "group": "seo-crawl"},
                {"id": "link-text", "weight": 1, "group": "seo-content"},
                {"id": "crawlable-anchors", "weight": 1, "group": "seo-crawl"},
                {"id": "is-crawlable", "weight": 1, "group": "seo-crawl"},
                {"id": "robots-txt", "weight": 1, "group": "seo-crawl"},
                {"id": "image-alt", "weight": 1, "group": "seo-content"},
                {"id": "hreflang", "weight": 1, "group": "seo-content"},
                {"id": "canonical", "weight": 1, "group": "seo-content"},
                {"id": "font-size", "weight": 0, "group": "seo-mobile"},
                {"id": "plugins", "weight": 1, "group": "seo-content"},
                {"id": "tap-targets", "weight": 0, "group": "seo-mobile"},
                {"id": "structured-data", "weight": 0}
            ],
            "additional_seo_data": {
                "title_tag": "Present",
                "meta_description": "Present",
                "h1_tags": "Missing or Multiple",
                "canonical_tag": "Present"
            },
            "advanced_seo_analysis": {
                "content_quality": {
                    "word_count": on_page_seo_data.get('word_count', 0),
                    "readability": "To be calculated",
                    "unique_content": "To be checked"
                },
                "keyword_optimization": {
                    "keyword_counts": {
                        # ... [include keyword optimization details] ...
                    }
                },
                "backlink_profile": {
                    "backlink_profile": "API integration required"
                }
            }
        }
    }

    return seo_report

if __name__ == "__main__":
    url_to_analyze = "https://agenciafreela.com.br/"
    seo_analysis_result = analyze_seo(url_to_analyze)
    seo_logger.info(f"SEO Analysis Result: {json.dumps(seo_analysis_result, indent=4)}")
