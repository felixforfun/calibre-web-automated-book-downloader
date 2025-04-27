# Calibre Web Automated Book Downloader with Tolino Integration

This application allows you to search for books from various sources (primarily Anna's Archive), download them to your Calibre library, and optionally upload them directly to your Tolino cloud account.

## Features

- Search for books from Anna's Archive and other sources
- Download books directly to your Calibre library
- Upload books to Tolino cloud (Hugendubel, Thalia, etc.)
- Secure storage of Tolino credentials
- Simple and intuitive user interface

## Installation

### Option 1: Docker (Recommended)

The easiest way to run the application is using Docker and Docker Compose:

1. Clone the repository:
   ```bash
   git clone https://github.com/felixforfun/calibre-web-automated-book-downloader.git
   cd calibre-web-automated-book-downloader
   ```

2. Create the necessary directories:
   ```bash
   mkdir -p /tmp/data/calibre-web/{ingest,tmp,logs}
   ```

3. Start the application using Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Access the application at http://localhost:8084

### Option 2: Manual Installation

#### Prerequisites

- Python 3.8 or higher
- Playwright for browser automation
- Cryptography for secure credential storage

#### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/felixforfun/calibre-web-automated-book-downloader.git
   cd calibre-web-automated-book-downloader
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

3. Configure environment variables (optional):
   ```bash
   # Tolino integration settings
   export ENABLE_TOLINO=True
   export TOLINO_WEBSHOP=hugendubel  # or thalia, weltbild, buecher, osiander, mayersche
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Usage

### Searching for Books

1. Enter your search query in the search box
2. Select the desired format (EPUB, MOBI, etc.)
3. Click "Search"
4. Browse through the search results

### Downloading Books

1. Find the book you want to download
2. Click the "Download" button
3. The book will be downloaded to your Calibre library

### Uploading to Tolino

1. Configure your Tolino credentials:
   - Click the "Tolino Settings" button in the top navigation bar
   - Enter your Tolino account email and password
   - Click "Save"

2. Upload a book to Tolino:
   - Find the book you want to upload
   - Click the "Upload to Tolino" button
   - The book will be downloaded to your Calibre library and then uploaded to your Tolino cloud account

## Tolino Integration

The Tolino integration uses Playwright to automate the process of uploading books to your Tolino cloud account. It supports the following Tolino webshops:

- Hugendubel (default)
- Thalia
- Weltbild
- Buecher.de
- Osiander
- Mayersche

Your Tolino credentials are securely stored using encryption and are only used for the purpose of uploading books to your Tolino cloud account.

## Environment Variables

### General Settings

| Variable | Description | Default |
|----------|-------------|---------|
| FLASK_PORT | Port for the web interface | 8084 |
| LOG_LEVEL | Logging level (info, debug, warning, error) | info |
| BOOK_LANGUAGE | Default language for book search | en |
| USE_BOOK_TITLE | Use book title for filename | true |
| TZ | Timezone | UTC |
| APP_ENV | Application environment (prod, dev) | prod |
| UID | User ID to run the application | 1000 |
| GID | Group ID to run the application | 100 |

### Tolino Integration Settings

| Variable | Description | Default |
|----------|-------------|---------|
| ENABLE_TOLINO | Enable or disable Tolino integration | true |
| TOLINO_WEBSHOP | Tolino webshop to use (hugendubel, thalia, weltbild, buecher, osiander, mayersche) | hugendubel |
| TOLINO_CREDENTIALS_FILE | Path to store encrypted credentials | /tmp/cwa-book-downloader/tolino_credentials.enc |
| TOLINO_ENCRYPTION_KEY | Key for encrypting credentials | tolino-integration-secret-key |

### Docker Volumes

When using Docker, you should mount the following volumes:

| Volume | Description |
|--------|-------------|
| /cwa-book-ingest | Directory where downloaded books will be stored |
| /tmp/cwa-book-downloader | Directory for temporary files and Tolino credentials |
| /var/log/cwa-book-downloader | Directory for log files |

## Security Considerations

- Tolino credentials are encrypted before being stored
- No credentials are sent to any third-party services
- All automation is done locally using Playwright

## Troubleshooting

### Tolino Upload Issues

- Make sure your Tolino credentials are correct
- Check that the book format is supported by Tolino (EPUB is recommended)
- Ensure that Playwright is properly installed with `playwright install`

### Browser Automation Issues

If you encounter issues with Playwright browser automation:

1. Make sure you have the required system dependencies:
   ```bash
   apt-get install -y libxcursor1 libgtk-3-0
   ```

2. Reinstall Playwright browsers:
   ```bash
   playwright install
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on the original [calibre-web-automated-book-downloader](https://github.com/felixforfun/calibre-web-automated-book-downloader) by felixforfun
- Uses [Playwright](https://playwright.dev/) for browser automation
- Uses [Cryptography](https://cryptography.io/) for secure credential storage