import json
import sqlite3
from config import setup_logger

# Configure logger for database operations
db_logger = setup_logger('db_logger', 'database.log')

class DatabaseManager:
    def __init__(self, db_name: str = "web_analysis.db"):
        self.db_name = db_name
        with self._get_connection() as conn:
            self.setup_database(conn)

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_name)

    def setup_database(self, conn: sqlite3.Connection) -> None:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS websites (
                    url TEXT PRIMARY KEY,
                    segment TEXT,
                    seo_status TEXT,
                    load_time TEXT,
                    design_status TEXT,
                    pwa_features_status TEXT
                )
            ''')

    def insert_website_data(self, data: tuple) -> None:
        if not isinstance(data, tuple) or len(data) != 6:
            db_logger.error("Invalid data format for insertion")
            return

        with self._get_connection() as conn:
            try:
                conn.execute('''
                    INSERT OR REPLACE INTO websites 
                    (url, segment, seo_status, load_time, design_status, pwa_features_status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', data)
            except sqlite3.Error as e:
                db_logger.error(f"Database error: {e}")

    def insert_multiple_website_data(self, data_list: list) -> None:
        if any(not isinstance(data, tuple) or len(data) != 6 for data in data_list):
            db_logger.error("Invalid data format for bulk insertion")
            return

        with self._get_connection() as conn:
            try:
                conn.executemany('''
                    INSERT OR REPLACE INTO websites 
                    (url, segment, seo_status, load_time, design_status, pwa_features_status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', data_list)
            except sqlite3.Error as e:
                db_logger.error(f"Database error: {e}")

    def url_exists(self, url: str) -> bool:
        with self._get_connection() as conn:
            try:
                cur = conn.execute('SELECT COUNT(*) FROM websites WHERE url = ?', (url,))
                return cur.fetchone()[0] > 0
            except sqlite3.Error as e:
                db_logger.error(f"Database error in url_exists: {e}")
                return False

    def query_website_data(self, query: str, params: tuple = (), export_to_json: bool = False, json_file_path: str = 'query_results.json') -> list:
        with self._get_connection() as conn:
            try:
                cur = conn.execute(query, params)
                results = cur.fetchall()
                formatted_results = [self.format_result(result) for result in results]
                if export_to_json:
                    try:
                        with open(json_file_path, 'w') as file:
                            json.dump(formatted_results, file, indent=4)
                    except FileNotFoundError as e:
                        db_logger.error(f"File not found: {e}")
                return formatted_results
            except sqlite3.Error as e:
                db_logger.error(f"Database query error: {e}")
                return []

    def update_website_data(self, query: str, params: tuple = ()) -> None:
        if not isinstance(params, tuple):
            db_logger.error("Invalid parameters for update")
            return

        with self._get_connection() as conn:
            try:
                conn.execute(query, params)
            except sqlite3.Error as e:
                db_logger.error(f"Database update error: {e}")

    def close_connection(self) -> None:
        # Deprecated as connections are now handled using context managers
        pass

    def format_result(self, result: tuple) -> dict:
        return {
            'URL': result[0],
            'Segment': result[1],
            'SEO Status': result[2],
            'Load Time': result[3],
            'Design Status': result[4],
            'PWA Features Status': result[5]
        }

if __name__ == "__main__":
    db_manager = DatabaseManager()
    # Example usage
    db_manager.insert_website_data(('https://example.com', 'health', 'SEO data', '5s', 'Responsive Design', 'PWA Compliant'))
    db_manager.insert_multiple_website_data([
        ('https://example2.com', 'tech', 'SEO data 2', '4s', 'Modern Design', 'PWA Compliant 2'),
        # Add more data as needed
    ])
    results = db_manager.query_website_data('SELECT * FROM websites WHERE segment = ?', ('health',), export_to_json=True)
    for result in results:
        print(result)
    db_manager.update_website_data('UPDATE websites SET seo_status = ? WHERE url = ?', ('Updated SEO data', 'https://example.com'))
