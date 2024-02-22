import sys
from pathlib import Path

import urllib3
sys.path.append(str(Path(__file__).parent.parent))

from analysis.seo import analyze_seo
from analysis.load_time import analyze_load_time
from analysis.design import analyze_design
from analysis.pwa import analyze_pwa_features
from config import setup_logger

# Configure logger for website analysis
website_analysis_logger = setup_logger('website_analysis_logger', 'website_analysis.log')

def analyze_website(url_data):
    try:
        # Extract URL if url_data is a dictionary
        url = url_data['link'] if isinstance(url_data, dict) else url_data

        website_analysis_logger.info(f"Starting analysis for {url}")

        seo_result = analyze_seo(url)
        load_time_result = analyze_load_time(url)
        design_result = analyze_design(url)
        pwa_result = analyze_pwa_features(url)

        analysis_results = {
            'SEO': seo_result,
            'Load Time': load_time_result,
            'Design': design_result,
            'PWA Features': pwa_result
        }

        return analysis_results
    except Exception as e:
        website_analysis_logger.error(f"Error in website analysis for {urllib3}: {e}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    url_to_analyze = 'https://www.agenciafreela.com.br'
    result = analyze_website(url_to_analyze)
    website_analysis_logger.info(f"Website Analysis Result: {result}")