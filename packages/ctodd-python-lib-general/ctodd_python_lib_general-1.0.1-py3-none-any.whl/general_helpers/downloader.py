#!/usr/bin/env python3
"""
    Lib that allows downloading a File from the given url
    and saving to the given location
"""

# Python Library Imports
import sys
import logging
import requests
from datetime import datetime
from pathlib import Path


def download_file(url, file_location=None, overwrite=False):
    """
    Purpose:
        Download file from specified URL and store in a specfied location.
        If no location is provided, the file is downloaded in the current
        directory. If overwrite is false, the file is not downloaded.
    Args:
        url (string): Full URL path to download file from.
        file_location (string): Full path to where file will be stored.
        overwrite (Boolean): Whether or not to overwrite file if it already
            exists
    Return
        file_location (string): Full path to where file was be stored.
    """
    logging.info(f"Fetching file from {url}")

    report_date = str(datetime.now().date())
    file_type = url.split(".")[-1]
    if not file_location:
        file_location = f"./{report_date}.{file_type}"
    elif file_location.endswith("/"):
        file_location = f"{file_location}{report_date}.{file_type}"

    if not overwrite:
        existing_file = Path(file_location)
        if existing_file.is_file():
            error_msg = "Cannot Download. File exists and overwrite = False"
            logging.error(error_msg)
            raise Exception(error_msg)

    logging.info(f"Storing File to: {file_location}")

    request = requests.get(url, stream=True)
    request.raise_for_status()
    with open(file_location, "wb") as downloaded_file:
        for chunk in request.iter_content(chunk_size=1024):
            if chunk:
                downloaded_file.write(chunk)
                downloaded_file.flush()

    return file_location
