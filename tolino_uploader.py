"""Tolino cloud upload functionality using Playwright."""

import os
import time
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from cryptography.fernet import Fernet
import json
import base64

from logger import setup_logger
from env import TOLINO_CREDENTIALS_FILE, ENCRYPTION_KEY_FILE

logger = setup_logger(__name__)

class TolinoUploader:
    """Class to handle uploading books to Tolino cloud."""
    
    def __init__(self):
        """Initialize the TolinoUploader."""
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._credentials: Dict[str, str] = {}
        self._encryption_key: Optional[bytes] = None
        self._load_encryption_key()
        self._load_credentials()
        
    def _load_encryption_key(self) -> None:
        """Load or generate encryption key for credentials."""
        try:
            if os.path.exists(ENCRYPTION_KEY_FILE):
                with open(ENCRYPTION_KEY_FILE, 'rb') as key_file:
                    self._encryption_key = key_file.read()
            else:
                # Generate a new key if none exists
                self._encryption_key = Fernet.generate_key()
                with open(ENCRYPTION_KEY_FILE, 'wb') as key_file:
                    key_file.write(self._encryption_key)
                logger.info("Generated new encryption key")
        except Exception as e:
            logger.error_trace(f"Error loading/generating encryption key: {e}")
            
    def _load_credentials(self) -> None:
        """Load Tolino credentials from encrypted file."""
        try:
            if os.path.exists(TOLINO_CREDENTIALS_FILE) and self._encryption_key:
                with open(TOLINO_CREDENTIALS_FILE, 'rb') as cred_file:
                    encrypted_data = cred_file.read()
                    
                cipher_suite = Fernet(self._encryption_key)
                decrypted_data = cipher_suite.decrypt(encrypted_data)
                self._credentials = json.loads(decrypted_data.decode('utf-8'))
                logger.info("Loaded Tolino credentials")
        except Exception as e:
            logger.error_trace(f"Error loading credentials: {e}")
            self._credentials = {}
            
    def save_credentials(self, username: str, password: str) -> bool:
        """Save Tolino credentials to encrypted file."""
        try:
            if not self._encryption_key:
                self._load_encryption_key()
                
            self._credentials = {
                "username": username,
                "password": password
            }
            
            cipher_suite = Fernet(self._encryption_key)
            encrypted_data = cipher_suite.encrypt(json.dumps(self._credentials).encode('utf-8'))
            
            with open(TOLINO_CREDENTIALS_FILE, 'wb') as cred_file:
                cred_file.write(encrypted_data)
                
            logger.info("Saved Tolino credentials")
            return True
        except Exception as e:
            logger.error_trace(f"Error saving credentials: {e}")
            return False
            
    def has_credentials(self) -> bool:
        """Check if Tolino credentials are available."""
        return bool(self._credentials.get("username") and self._credentials.get("password"))
    
    async def _init_browser(self) -> None:
        """Initialize the browser for Tolino upload."""
        try:
            playwright = await async_playwright().start()
            self._browser = await playwright.chromium.launch(headless=True)
            self._context = await self._browser.new_context()
            self._page = await self._context.new_page()
            logger.info("Browser initialized for Tolino upload")
        except Exception as e:
            logger.error_trace(f"Error initializing browser: {e}")
            raise
    
    async def _close_browser(self) -> None:
        """Close the browser."""
        try:
            if self._browser:
                await self._browser.close()
                self._browser = None
                self._context = None
                self._page = None
                logger.info("Browser closed")
        except Exception as e:
            logger.error_trace(f"Error closing browser: {e}")
    
    async def _login_to_tolino(self) -> bool:
        """Login to Tolino cloud via Hugendubel."""
        if not self._page or not self.has_credentials():
            return False
            
        try:
            # Navigate to Hugendubel Tolino WebReader
            await self._page.goto("https://webreader.hugendubel.de/")
            
            # Wait for the login page to load
            await self._page.wait_for_selector('input[type="email"]', timeout=30000)
            
            # Fill in credentials
            await self._page.fill('input[type="email"]', self._credentials["username"])
            await self._page.fill('input[type="password"]', self._credentials["password"])
            
            # Click login button
            await self._page.click('button[type="submit"]')
            
            # Wait for login to complete
            try:
                # Check for successful login by waiting for the library view
                await self._page.wait_for_selector('.library-view', timeout=30000)
                logger.info("Successfully logged in to Tolino cloud")
                return True
            except Exception as e:
                logger.error_trace(f"Login failed: {e}")
                return False
                
        except Exception as e:
            logger.error_trace(f"Error during Tolino login: {e}")
            return False
    
    async def upload_book(self, book_path: str) -> bool:
        """Upload a book to Tolino cloud.
        
        Args:
            book_path: Path to the EPUB file
            
        Returns:
            bool: True if upload was successful
        """
        if not os.path.exists(book_path):
            logger.error(f"Book file not found: {book_path}")
            return False
            
        try:
            await self._init_browser()
            
            if not self._page:
                logger.error("Browser initialization failed")
                return False
                
            # Login to Tolino
            login_success = await self._login_to_tolino()
            if not login_success:
                logger.error("Failed to login to Tolino cloud")
                return False
                
            # Navigate to the upload page or find the upload button
            try:
                # Look for the upload button or menu
                upload_button = await self._page.wait_for_selector('button.upload-button, button[aria-label="Upload"], button:has-text("Upload")', timeout=10000)
                await upload_button.click()
            except Exception:
                logger.info("Upload button not found, looking for alternative upload options")
                # Try alternative methods to find upload functionality
                try:
                    # Look for menu options that might contain upload
                    menu_button = await self._page.wait_for_selector('button.menu-button, button[aria-label="Menu"]', timeout=5000)
                    await menu_button.click()
                    
                    # Wait for menu to open and look for upload option
                    upload_option = await self._page.wait_for_selector('li:has-text("Upload"), button:has-text("Upload")', timeout=5000)
                    await upload_option.click()
                except Exception as e:
                    logger.error_trace(f"Could not find upload option: {e}")
                    return False
            
            # Handle file upload
            async with self._page.expect_file_chooser() as fc_info:
                # The file chooser dialog should be triggered by the previous click
                # If not, we might need to click a specific element
                pass
                
            file_chooser = await fc_info.value
            await file_chooser.set_files(book_path)
            
            # Wait for upload to complete
            try:
                # Look for success message or indicator
                await self._page.wait_for_selector('.upload-success, .success-message, div:has-text("Upload successful")', timeout=60000)
                logger.info(f"Successfully uploaded book to Tolino cloud: {book_path}")
                return True
            except Exception as e:
                logger.error_trace(f"Upload confirmation not found: {e}")
                return False
                
        except Exception as e:
            logger.error_trace(f"Error uploading book to Tolino: {e}")
            return False
        finally:
            await self._close_browser()

# Create a global instance
tolino_uploader = TolinoUploader()

async def upload_book_to_tolino(book_path: str) -> bool:
    """Upload a book to Tolino cloud.
    
    Args:
        book_path: Path to the EPUB file
        
    Returns:
        bool: True if upload was successful
    """
    return await tolino_uploader.upload_book(book_path)

def save_tolino_credentials(username: str, password: str) -> bool:
    """Save Tolino credentials.
    
    Args:
        username: Tolino account username/email
        password: Tolino account password
        
    Returns:
        bool: True if credentials were saved successfully
    """
    return tolino_uploader.save_credentials(username, password)

def has_tolino_credentials() -> bool:
    """Check if Tolino credentials are available.
    
    Returns:
        bool: True if credentials are available
    """
    return tolino_uploader.has_credentials()