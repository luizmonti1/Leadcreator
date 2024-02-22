import requests
from bs4 import BeautifulSoup
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import setup_logger, GOOGLE_API_KEY

# Configure logger for design analysis
design_logger = setup_logger("design_logger", "design_analysis.log")

def check_css_frameworks(soup):
    css_links = [link.get("href", "") for link in soup.find_all("link", {"rel": "stylesheet"})]
    frameworks = {
        "Bootstrap": "bootstrap",
        "Materialize": "materialize",
        "Foundation": "foundation",
        "Bulma": "bulma",
        "Tailwind CSS": "tailwind",
        "Semantic UI": "semantic",
        "UIKit": "uikit",
    }
    for name, identifier in frameworks.items():
        if any(identifier in link for link in css_links):
            return name
    return "No Framework Detected"

def check_modern_js_usage(soup):
    scripts = [script.get("src", "") for script in soup.find_all("script")]
    js_frameworks = {
        "React": "react",
        "Vue": "vue",
        "Angular": "angular",
        "Svelte": "svelte",
        "Backbone.js": "backbone",
        "Ember.js": "ember",
        "Alpine.js": "alpine",
    }
    for name, identifier in js_frameworks.items():
        if any(identifier in script for script in scripts):
            return f"Modern JavaScript Framework Detected: {name}"
    return "No Modern JavaScript Framework Detected"

def analyze_mobile_usability(url):
    design_logger.info(f"Starting mobile usability analysis for {url}")
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={GOOGLE_API_KEY}"
    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        result = response.json()
        lighthouse = result.get("lighthouseResult", {}).get("categories", {}).get("performance", {})
        audits = result.get("lighthouseResult", {}).get("audits", {})
        mobile_usability_data = {
            "Mobile Usability Score": lighthouse.get("score"),
            "First Contentful Paint": audits.get("first-contentful-paint", {}).get("displayValue"),
            "Speed Index": audits.get("speed-index", {}).get("displayValue"),
            "Time to Interactive": audits.get("interactive", {}).get("displayValue"),
            "Total Blocking Time": audits.get("total-blocking-time", {}).get("displayValue"),
        }
        return mobile_usability_data
    except requests.HTTPError as http_err:
        design_logger.error(f"HTTP error occurred: {http_err}")
    except requests.Timeout as timeout_err:
        design_logger.error(f"Timeout occurred: {timeout_err}")
    except Exception as e:
        design_logger.error(f"Error in Mobile Usability Analysis for {url}: {e}")
    return {}

def analyze_responsive_design(soup):
    viewport_meta = soup.find("meta", {"name": "viewport"})
    return "Responsive" if viewport_meta else "Not Responsive"

def analyze_html5_usage(soup):
    doctype = soup.doctype
    return "HTML5" if doctype and "html" in doctype.lower() else "Non-HTML5"

def analyze_accessibility_features(soup):
    aria_roles = soup.find_all(attrs={"role": True})
    return "Accessibility Features Used" if aria_roles else "No Accessibility Features"

def analyze_pagespeed_insights(url):
    design_logger.info(f"Starting PageSpeed Insights analysis for {url}")
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={GOOGLE_API_KEY}"

    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        result = response.json()
        lighthouse = result.get('lighthouseResult', {}).get('categories', {}).get('performance', {})
        audits = result.get('lighthouseResult', {}).get('audits', {})

        pagespeed_data = {
            "Performance Score": lighthouse.get('score'),
            "First Contentful Paint": audits.get('first-contentful-paint', {}).get('displayValue'),
            "Largest Contentful Paint": audits.get('largest-contentful-paint', {}).get('displayValue'),
            "Cumulative Layout Shift": audits.get('cumulative-layout-shift', {}).get('displayValue'),
            "Speed Index": audits.get('speed-index', {}).get('displayValue'),
            "Time to Interactive": audits.get('interactive', {}).get('displayValue'),
            "Total Blocking Time": audits.get('total-blocking-time', {}).get('displayValue'),
            "First Meaningful Paint": audits.get('first-meaningful-paint', {}).get('displayValue'),
            "Efficiently Encode Images": audits.get('uses-optimized-images', {}).get('displayValue'),
            "Render Blocking Resources": audits.get('render-blocking-resources', {}).get('displayValue'),
            "Server Response Time": audits.get('server-response-time', {}).get('displayValue')
            # Add any other relevant metrics you need from the PageSpeed Insights result
        }
        return pagespeed_data
    except requests.HTTPError as http_err:
        design_logger.error(f"HTTP error occurred: {http_err}")
    except requests.Timeout as timeout_err:
        design_logger.error(f"Timeout occurred: {timeout_err}")
    except Exception as e:
        design_logger.error(f"Error in PageSpeed Insights Analysis for {url}: {e}")
    return {}

def analyze_design(url):
    design_logger.info(f"Starting design analysis for {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        css_framework = check_css_frameworks(soup)
        modern_js = check_modern_js_usage(soup)
        mobile_usability = analyze_mobile_usability(url)
        responsive_design = analyze_responsive_design(soup)
        html5_usage = analyze_html5_usage(soup)
        accessibility_features = analyze_accessibility_features(soup)
        pagespeed_insights = analyze_pagespeed_insights(url)  # New line to analyze PageSpeed Insights

        return {
            "CSS Framework": css_framework,
            "Modern JavaScript Usage": modern_js,
            "Mobile Usability": mobile_usability,
            "Responsive Design": responsive_design,
            "HTML5 Usage": html5_usage,
            "Accessibility Features": accessibility_features,
            "PageSpeed Insights": pagespeed_insights  # Include PageSpeed Insights data in the result
        }
    except requests.HTTPError as http_err:
        design_logger.error(f"HTTP error occurred while fetching {url}: {http_err}")
    except requests.Timeout as timeout_err:
        design_logger.error(f"Timeout occurred while fetching {url}: {timeout_err}")
    except Exception as e:
        design_logger.error(f"Error in Design Analysis for {url}: {e}")
    return {}

if __name__ == "__main__":
    url_to_analyze = "https://www.example.com"
    design_analysis_result = analyze_design(url_to_analyze)
    design_logger.info(f"Design Analysis Result: {design_analysis_result}")
