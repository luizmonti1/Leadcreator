import requests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import setup_logger, GOOGLE_API_KEY
import logging

# Configure logger for load time analysis
load_time_logger = setup_logger("load_time_logger", "load_time_analysis.log")


def analyze_load_time(url):
    load_time_logger.info(f"Starting load time analysis for {url}")
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={GOOGLE_API_KEY}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        result = response.json()
        lighthouse = (
            result.get("lighthouseResult", {})
            .get("categories", {})
            .get("performance", {})
        )
        audits = result.get("lighthouseResult", {}).get("audits", {})

        performance_metrics = {
            "Performance Score": lighthouse.get("score"),
            "First Contentful Paint": audits.get("first-contentful-paint", {}).get(
                "displayValue", "N/A"
            ),
            "Speed Index": audits.get("speed-index", {}).get("displayValue", "N/A"),
            "Time to Interactive": audits.get("interactive", {}).get(
                "displayValue", "N/A"
            ),
            "First Meaningful Paint": audits.get("first-meaningful-paint", {}).get(
                "displayValue", "N/A"
            ),
            "Total Blocking Time": audits.get("total-blocking-time", {}).get(
                "displayValue", "N/A"
            ),
            "Largest Contentful Paint": audits.get("largest-contentful-paint", {}).get(
                "displayValue", "N/A"
            ),
            "Cumulative Layout Shift": audits.get("cumulative-layout-shift", {}).get(
                "displayValue", "N/A"
            ),
            "Critical Request Chains": audits.get("critical-request-chains", {}).get(
                "displayValue", "N/A"
            ),
            "JavaScript Execution Time": audits.get("bootup-time", {}).get(
                "displayValue", "N/A"
            ),
            "Main Thread Work Breakdown": audits.get(
                "mainthread-work-breakdown", {}
            ).get("displayValue", "N/A"),
            "Offscreen Images": audits.get("offscreen-images", {}).get(
                "displayValue", "N/A"
            ),
            "Efficiently Encode Images": audits.get("uses-optimized-images", {}).get(
                "displayValue", "N/A"
            ),
            "Text Compression": audits.get("uses-text-compression", {}).get(
                "displayValue", "N/A"
            ),
            "Render-Blocking Resources": audits.get(
                "render-blocking-resources", {}
            ).get("displayValue", "N/A"),
            "Server Response Time": audits.get("server-response-time", {}).get(
                "displayValue", "N/A"
            ),
            "Uses Efficient Image Formats": audits.get("modern-image-formats", {}).get(
                "displayValue", "N/A"
            ),
            "Minified JavaScript": audits.get("unminified-javascript", {}).get(
                "displayValue", "N/A"
            ),
            "Minified CSS": audits.get("unminified-css", {}).get("displayValue", "N/A"),
            "Properly Sized Images": audits.get("uses-responsive-images", {}).get(
                "displayValue", "N/A"
            ),
            "Third-Party Payloads": audits.get("third-party-summary", {}).get(
                "displayValue", "N/A"
            ),
            "Render-Blocking Resources Count": len(
                audits.get("render-blocking-resources", {})
                .get("details", {})
                .get("items", [])
            ),
        }

        # Processing opportunities for optimization
        opportunities = {}
        for audit_key, audit_value in audits.items():
            if audit_value.get("details", {}).get("type") == "opportunity":
                opportunity_data = {
                    "Description": audit_value.get("title"),
                    "Estimated Savings": audit_value.get("details", {}).get(
                        "overallSavingsMs", 0
                    ),
                }
                opportunities[audit_key] = opportunity_data

        performance_metrics["Opportunities for Optimization"] = opportunities

        return performance_metrics

    except requests.HTTPError as http_err:
        load_time_logger.error(f"HTTP error occurred: {http_err}")
    except Exception as e:
        load_time_logger.error(f"Error in Load Time Analysis for {url}: {e}")
    return {}


if __name__ == "__main__":
    url_to_analyze = "https://agenciafreela.com.br"
    load_time_analysis_result = analyze_load_time(url_to_analyze)
    load_time_logger.info(f"Load Time Analysis Result: {load_time_analysis_result}")
