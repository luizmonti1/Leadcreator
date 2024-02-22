Project Overview: Web Scraping and Analysis for Marketing Agency
1. Main Script (main.py)
Purpose: Drives the entire web scraping, website analysis, and data storage process.
Functionality:
Uses scraper modules for Google search and website analysis.
Utilizes database module to interact with SQLite database for data storage and retrieval.
Implements logging for monitoring and debugging.
2. Scraper Module
Components:
google_search.py: Performs Google searches for predefined keywords.
website_analysis.py: Analyzes found websites for various metrics like SEO, design, etc.
Data Handling: Returns the search results and analysis data to be processed and stored in the database.
3. Database Module (db_manager.py)
Functionality:
Manages interactions with web_analysis.db.
Provides functions to insert and retrieve data.
Ensures data integrity and efficient data management.
4. Analysis Module
Components:
Individual scripts like seo.py, design.py, load_time.py, pwa.py for specific analyses.
Purpose: Performs in-depth analysis of various aspects of each website.
5. Phase 2: Data Filtering and Organization
Scoring Logic: Applies a score (0-5) based on website analysis results.
Filtering Criteria: Excludes websites with scores below 1 or above 4.
Data Organization: Organizes the remaining websites' data into individual folders.
6. Phase 3: Report Generation and Email Composition
Report Generation:
Compiles data from JSON files into comprehensive reports.
Highlights key insights and improvement areas.
Email Composition with OpenAI API:
Generates personalized email drafts using OpenAI based on report content.
Ensures efficient and relevant utilization of the API.
7. Alternate Use: Knowledge Database and Affiliate Ads
Data Utilization:
Curates a database from scraped data for internal knowledge and potential external applications.
Considers development of affiliate ads based on the comprehensive database.
Technologies and Libraries:
Python as the primary programming language.
Libraries such as selenium, beautifulsoup4, requests, sqlite3, pandas, json, and openai for various functionalities.
SQLite for database management.
OpenAI API for generating personalized email content.
Project Structure:
Folders: scraper, database, analysis, bot, logs, and others for organized project management.
Log Files: Stores logs for different components (seo_analysis.log, database.log, etc.).
