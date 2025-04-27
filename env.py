import os
from pathlib import Path

def string_to_bool(s: str) -> bool:
    return s.lower() in ["true", "yes", "1", "y"]

LOG_ROOT = Path(os.getenv("LOG_ROOT", "/var/log/"))
LOG_DIR = LOG_ROOT / "cwa-book-downloader"
TMP_DIR = Path(os.getenv("TMP_DIR", "/tmp/cwa-book-downloader"))
INGEST_DIR = Path(os.getenv("INGEST_DIR", "/cwa-book-ingest"))
STATUS_TIMEOUT = int(os.getenv("STATUS_TIMEOUT", "3600"))
USE_BOOK_TITLE = string_to_bool(os.getenv("USE_BOOK_TITLE", "false"))
MAX_RETRY = int(os.getenv("MAX_RETRY", "10"))
DEFAULT_SLEEP = int(os.getenv("DEFAULT_SLEEP", "5"))
USE_CF_BYPASS = string_to_bool(os.getenv("USE_CF_BYPASS", "true"))
HTTP_PROXY = os.getenv("HTTP_PROXY", "").strip()
HTTPS_PROXY = os.getenv("HTTPS_PROXY", "").strip()
AA_DONATOR_KEY = os.getenv("AA_DONATOR_KEY", "").strip()
_AA_BASE_URL = os.getenv("AA_BASE_URL", "auto").strip()
_AA_ADDITIONAL_URLS = os.getenv("AA_ADDITIONAL_URLS", "").strip()
_SUPPORTED_FORMATS = os.getenv("SUPPORTED_FORMATS", "epub,mobi,azw3,fb2,djvu,cbz,cbr").lower()
_BOOK_LANGUAGE = os.getenv("BOOK_LANGUAGE", "en").lower()
_CUSTOM_SCRIPT = os.getenv("CUSTOM_SCRIPT", "").strip()
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", "12000"))
DEBUG = string_to_bool(os.getenv("DEBUG", "False"))

# Tolino integration settings
ENABLE_TOLINO = string_to_bool(os.getenv("ENABLE_TOLINO", "True"))
TOLINO_CREDENTIALS_FILE = Path(os.getenv("TOLINO_CREDENTIALS_FILE", str(TMP_DIR / "tolino_credentials.enc")))
TOLINO_ENCRYPTION_KEY = os.getenv("TOLINO_ENCRYPTION_KEY", "tolino-integration-secret-key")
TOLINO_WEBSHOP = os.getenv("TOLINO_WEBSHOP", "hugendubel")
# If debug is true, we want to log everything
if DEBUG:
    LOG_LEVEL = "DEBUG"
else:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
ENABLE_LOGGING = string_to_bool(os.getenv("ENABLE_LOGGING", "true"))
MAIN_LOOP_SLEEP_TIME = int(os.getenv("MAIN_LOOP_SLEEP_TIME", "5"))
DOCKERMODE = string_to_bool(os.getenv("DOCKERMODE", "false"))
_CUSTOM_DNS = os.getenv("CUSTOM_DNS", "").strip()
USE_DOH = string_to_bool(os.getenv("USE_DOH", "false"))
BYPASS_RELEASE_INACTIVE_MIN = int(os.getenv("BYPASS_RELEASE_INACTIVE_MIN", "5"))
APP_ENV = os.getenv("APP_ENV", "prod").lower()
# Logging settings
LOG_FILE = LOG_DIR / "cwa-bookd-downloader.log"

# Tolino settings
TOLINO_CREDENTIALS_FILE = Path(os.getenv("TOLINO_CREDENTIALS_FILE", str(TMP_DIR / "tolino_credentials.enc")))
ENCRYPTION_KEY_FILE = Path(os.getenv("ENCRYPTION_KEY_FILE", str(TMP_DIR / "encryption_key.bin")))
ENABLE_TOLINO = string_to_bool(os.getenv("ENABLE_TOLINO", "true"))

USING_TOR = string_to_bool(os.getenv("USING_TOR", "false"))
# If using Tor, we don't need to set custom DNS, use DOH, or proxy
if USING_TOR:
    _CUSTOM_DNS = ""
    USE_DOH = False
    HTTP_PROXY = ""
    HTTPS_PROXY = ""
    