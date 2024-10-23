import os

# Directory Paths for logs
LOG_DIR = os.getenv('LOG_DIR', 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, 'runtime.log')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # Default to INFO level

# Loguru formatting and style
LOGURU_FORMAT = (
    "<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan> {name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

