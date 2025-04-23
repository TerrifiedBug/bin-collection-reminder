"""
Module for retrieving bin collection information from Vale of White Horse Council website.
"""

import os
import re
import sys
from typing import Dict

import requests

from scripts.notifications import send_notifications


def get_bin_collection(uprn: str) -> Dict[str, str]:
    """
    Fetch bin collection information for a given UPRN from the Vale of White Horse Council website.

    Args:
        uprn: Unique Property Reference Number

    Returns:
        Dictionary containing the bin collection day and type
    """
    if not uprn:
        raise ValueError("UPRN cannot be empty")

    # Set up the request
    cookies = {
        "SVBINZONE": f"VALE%3AUPRN%40{uprn}",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    }
    params = {
        "SOVA_TAG": "VALE",
        "ebd": "0",
    }

    try:
        # Make the request
        response = requests.get(
            "https://eform.southoxon.gov.uk/ebase/BINZONE_DESKTOP.eb",
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=10,
        )
        response.raise_for_status()  # Raise exception for HTTP errors

        # Extract bin day using
        bin_day_match = re.search(
            r'<div class="binextra">(?:.*?<br>)?(?P<binday>[^-]+?)(?:\s*-\s*)',
            response.text,
        )

        bin_day = bin_day_match.group("binday") if bin_day_match else "Unknown"

        # Extract bin type using regex
        bin_type_match = re.search(
            r'<div class="bintxt"><h2>(?P<bintype>.*?)</h2></div>', response.text
        )
        bin_type = bin_type_match.group("bintype") if bin_type_match else "Unknown"

        return {"day": bin_day, "type": bin_type}

    except requests.RequestException as error:
        print(f"[!] Error fetching bin collection data: {error}")
        return {"day": "Error", "type": "Unable to retrieve collection data"}


def main() -> None:
    """Main function to retrieve bin collection data and send notifications."""
    # Get UPRN from environment variable
    uprn = os.environ.get("UPRN")

    if not uprn:
        print("[!] Error: UPRN environment variable not set")
        sys.exit(1)

    try:
        # Get bin collection information
        collection = get_bin_collection(uprn)
        print(f"[🗑️] Bin collection: {collection['day']}: {collection['type']}")

        # Send notifications
        send_notifications(collection)
    except Exception as error:
        print(f"[!] An error occurred: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
