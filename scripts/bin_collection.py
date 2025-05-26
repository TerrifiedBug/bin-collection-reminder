"""
Module for retrieving bin collection information from Vale of White Horse Council website.
"""

import os
import sys
from typing import Dict

import requests
from bs4 import BeautifulSoup

from scripts.notifications import send_notifications


def get_bin_collection(uprn: str) -> Dict[str, str]:
    """
    Fetch bin collection information for a given UPRN from the Vale of White Horse Council website.

    Args:
        uprn: Unique Property Reference Number

    Returns:
        Dictionary containing the bin collection day, type, and special message if present
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

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, "lxml")

        # Extract special message if it exists
        special_message = None
        bin_day = "Unknown"
        bin_type = "Unknown"

        # Find the bin extra div which contains the collection day
        bin_extra_div = soup.find("div", class_="binextra")
        if bin_extra_div:
            # Check if there's a special message (inside a strong tag)
            strong_tag = bin_extra_div.find("strong")
            if strong_tag:
                special_message = strong_tag.text.strip()

                # Get all text content and split by lines to find the day
                all_text = bin_extra_div.get_text(separator="\n", strip=True)
                lines = [line.strip() for line in all_text.split("\n") if line.strip()]

                # Find the line that contains the day (usually after the special message)
                for line in lines:
                    if line != special_message and "-" in line:
                        # Extract day part (before the hyphen)
                        bin_day = line.split("-")[0].strip()
                        break
            else:
                # Regular bin day (no special message)
                # Get clean text and extract day part
                all_text = bin_extra_div.get_text(strip=True)
                if "-" in all_text:
                    bin_day = all_text.split("-")[0].strip()
                else:
                    bin_day = all_text.strip()

        # Find the bin type in the h2 tag inside the bintxt div
        bin_txt_div = soup.find("div", class_="bintxt")
        if bin_txt_div:
            h2_tag = bin_txt_div.find("h2")
            if h2_tag:
                bin_type = h2_tag.text.strip()

        result = {"day": bin_day, "type": bin_type}
        if special_message:
            result["special_message"] = special_message

        return result

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
