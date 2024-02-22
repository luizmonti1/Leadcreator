import json
import sys
import time
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from scraper.google_search import perform_google_search
from scraper.website_analysis import analyze_website
from database.db_manager import DatabaseManager
from config import setup_logger

# Configure logger
main_logger = setup_logger('main_logger', 'main.log')

def main():
    db_manager = DatabaseManager()
    main_logger.info("Starting main process...")

    start_time = time.time()
    duration = 4 * 60 * 60  # 4 hours in seconds

    segments = {
     "input yours": [
            "keywords",         
            ]

    for segment, keywords in segments.items():
        for keyword in keywords:
            current_time = time.time()
            if (current_time - start_time) > duration:
                main_logger.info("Time limit reached, ending phase 1.")
                db_manager.close_connection()
                return  # Exit the function
            
            main_logger.info(f"Searching for keyword: {keyword}")
            found_websites = perform_google_search(keyword, num_results=10)

            for url_data in found_websites:
                url = url_data['link']

                if db_manager.url_exists(url):
                    main_logger.info(f"URL already analyzed: {url}")
                    continue

                main_logger.info(f"Analyzing website: {url}")
                try:
                    analysis_result = analyze_website(url)
                    seo_status = json.dumps(analysis_result.get('SEO', {}))
                    load_time = json.dumps(analysis_result.get('Load Time', {}))
                    design_status = json.dumps(analysis_result.get('Design', {}))
                    pwa_features_status = json.dumps(analysis_result.get('PWA Features', {}))
                    db_manager.insert_website_data((url, segment, seo_status, load_time, design_status, pwa_features_status))
                except Exception as e:
                    main_logger.error(f"Error analyzing website: {url}. Error message: {str(e)}")

    db_manager.close_connection()
    main_logger.info("Main process completed.")

if __name__ == "__main__":
    main()
