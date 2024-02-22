import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Environment variables for sensitive data
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID", "f7bb2832255ed421d")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyC7Z3EnVpUVJOfB1pD3pwV9qbk5s628NXU"),
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY", "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"
),
ORGANIZATION=os.getenv('org-5thX2SmWHafCHi5zVQ8S5ha5')
GOOGLE_OAUTH_CLIENT_ID = os.getenv(
    "GOOGLE_OAUTH_CLIENT_ID",
    "515387361174-r3oinqgbaqjn1dhbbge6ugrlk7haqfka.apps.googleusercontent.com",
)

# Database configuration
DATABASE_NAME = os.getenv("DATABASE_NAME", "web_analysis.db")

# Logging configuration
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logger(
    name, log_file, level=logging.INFO, max_log_size=10485760, backup_count=3
):
    """
    Function to set up a logger with log rotation.

    :param name: Name of the logger.
    :param log_file: Log file name.
    :param level: Logging level.
    :param max_log_size: Maximum log file size in bytes before rotation (default 10MB).
    :param backup_count: Number of backup files to keep.
    """
    log_file_path = LOG_DIR / log_file
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

    # Using RotatingFileHandler for log rotation
    handler = RotatingFileHandler(
        log_file_path, maxBytes=max_log_size, backupCount=backup_count, encoding="utf-8"
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


# Network request configurations
REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", 10)
)  # Timeout for HTTP requests in seconds
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
)

# Proxy configuration (if needed)
PROXY_URL = os.getenv("PROXY_URL", None)  # Example: 'http://10.10.1.10:3128'

# Scheduler configuration (not in use right now)
SCHEDULER_TIME = os.getenv("SCHEDULER_TIME", "10:00")  # Time to run the scheduled job

# Example usage
if __name__ == "__main__":
    # Example of setting up a logger with rotation
    test_logger = setup_logger("test_logger", "test.log")
    test_logger.info("This is a test log message.")
