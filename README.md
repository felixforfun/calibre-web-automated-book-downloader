# Calibre Web Automated Book Downloader with Tolino Integration

This application allows you to search for books from various sources (primarily Anna's Archive), download them to your Calibre library, and optionally upload them directly to your Tolino cloud account.

## Features

- Search for books from Anna's Archive and other sources
- Download books directly to your Calibre library
- Upload books to Tolino cloud (Hugendubel, Thalia, etc.)
- Secure storage of Tolino credentials
- Simple and intuitive user interface

## Installation

### Prerequisites

- Python 3.8 or higher
- Playwright for browser automation
- Cryptography for secure credential storage

### Setup

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

| Variable | Description | Default |
|----------|-------------|---------|
| ENABLE_TOLINO | Enable or disable Tolino integration | True |
| TOLINO_WEBSHOP | Tolino webshop to use | hugendubel |
| TOLINO_CREDENTIALS_FILE | Path to store encrypted credentials | /tmp/cwa-book-downloader/tolino_credentials.enc |
| TOLINO_ENCRYPTION_KEY | Key for encrypting credentials | tolino-integration-secret-key |

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