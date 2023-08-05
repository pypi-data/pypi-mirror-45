# Christopher H. Todd's Python Library For General Tasks

The ctodd-python-lib-general project is responsible for general tasks that have not been put in specific libraries. Will basically be a dumping ground for one-off tasks that are repeatable but would not call for a specific lib that can be expanded.

## Table of Contents

- [Dependencies](#dependencies)
- [Libraries](#libraries)
- [Example Scripts](#example-scripts)
- [Notes](#notes)
- [TODO](#todo)

## Dependencies

### Python Packages

- requests>=2.21.0

## Libraries

### [downloader.py](https://github.com/ChristopherHaydenTodd/ctodd-python-lib-general/blob/develop/general_helpers/downloader.py)

Lib that allows downloading a File from the given url and saving to the given location

Functions:

```
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
```

## Example Scripts

Example executable Python scripts/modules for testing and interacting with the library. These show example use-cases for the libraries and can be used as templates for developing with the libraries or to use as one-off development efforts.

### N/A

## Notes

 - Relies on f-string notation, which is limited to Python3.6.  A refactor to remove these could allow for development with Python3.0.x through 3.5.x

## TODO

 - Unittest framework in place, but lacking tests
