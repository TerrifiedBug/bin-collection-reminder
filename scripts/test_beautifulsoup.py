#!/usr/bin/env python3
"""Unit tests for bin collection BeautifulSoup parsing."""

import unittest

from bs4 import BeautifulSoup


def extract_bin_collection_info(html_content):
    """
    Extract bin collection information from HTML content using BeautifulSoup.

    Args:
        html_content: HTML content as a string

    Returns:
        Dictionary containing the bin collection day, type, and special message if present
    """
    soup = BeautifulSoup(html_content, "lxml")

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
            # The bin day is the text after the <br> tag
            br_tag = strong_tag.find_next("br")
            if br_tag and br_tag.next_sibling:
                bin_day_text = br_tag.next_sibling.strip()
                # Remove anything after a hyphen if present
                bin_day = bin_day_text.split("-")[0].strip()
        else:
            # Regular bin day (no special message)
            bin_day_text = bin_extra_div.text.strip()
            # Remove anything after a hyphen if present
            bin_day = bin_day_text.split("-")[0].strip()

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


class TestBeautifulSoupParsing(unittest.TestCase):
    """Test cases for BeautifulSoup parsing of bin collection HTML."""

    def setUp(self):
        """Set up test data."""
        # Example HTML snippets
        self.normal_html = """
        <div class="binextra">Wednesday 7 May -<br>green bin, textiles, food bin<br></div>
        <div class="bintxt"><h2>It's recycling week</h2></div>
        """

        self.special_html = """
        <div class="binextra"><strong>Your usual collection day is different this week</strong><br>Wednesday 7 May -<br>green bin, textiles, food bin and <a href="https://www.whitehorsedc.gov.uk/gardenwaste" class="swipperHrefURL">garden waste bin</a><br></div>
        <div class="bintxt"><h2>It's recycling week</h2></div>
        """

        self.empty_html = """
        <div class="empty">No bin collection data</div>
        """

    def test_normal_html_parsing(self):
        """Test parsing of normal HTML (no special message)."""
        result = extract_bin_collection_info(self.normal_html)

        self.assertEqual(result["day"], "Wednesday 7 May")
        self.assertEqual(result["type"], "It's recycling week")
        self.assertNotIn("special_message", result)

        # Test notification message
        notification = f"Reminder: {result['day']} - {result['type']}"
        self.assertEqual(
            notification, "Reminder: Wednesday 7 May - It's recycling week"
        )

    def test_special_html_parsing(self):
        """Test parsing of special HTML (with special message)."""
        result = extract_bin_collection_info(self.special_html)

        self.assertEqual(result["day"], "Wednesday 7 May")
        self.assertEqual(result["type"], "It's recycling week")
        self.assertIn("special_message", result)
        self.assertEqual(
            result["special_message"],
            "Your usual collection day is different this week",
        )

        # Test notification message
        notification = f"IMPORTANT: {result['special_message']} - {result['day']} - {result['type']}"
        self.assertEqual(
            notification,
            "IMPORTANT: Your usual collection day is different this week - Wednesday 7 May - It's recycling week",
        )

    def test_empty_html_parsing(self):
        """Test parsing of HTML with no bin collection data."""
        result = extract_bin_collection_info(self.empty_html)

        self.assertEqual(result["day"], "Unknown")
        self.assertEqual(result["type"], "Unknown")
        self.assertNotIn("special_message", result)


if __name__ == "__main__":
    unittest.main()
