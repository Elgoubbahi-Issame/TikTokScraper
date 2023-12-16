# TikTok Post Scraper

A Python script to scrape TikTok posts based on specified search terms and save the data in a CSV file.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
- [Data Conversion](#data-conversion)
- [Example](#example)
- [License](#license)
- [Contact](#contact)

## Introduction

This script uses Selenium to scrape TikTok posts based on predefined search terms. The scraped data includes post descriptions, tags, user information, post links, and more. The scraped data is then converted, and the final results are saved in a CSV file.

## Prerequisites

- [Python](https://www.python.org/) installed
- [Selenium](https://www.selenium.dev/documentation/en/) installed (`pip install selenium`)
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) installed and added to the system PATH

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/tiktok-post-scraper.git
   cd tiktok-post-scraper
   ```
2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

   ```bash
   pip install -r requirements.txt
   ```
## Usage

Run the script:

    ```bash
    python Script.py
    ```

## Functions

### `ScrapTiktokPost(browser, search)`

- Takes a Selenium WebDriver instance (`browser`) and a search term (`search`).
- Scrapes TikTok posts based on the search term.
- Returns a list of dictionaries containing post information.

### `convert_to_date(date_str)`

- Converts different date formats to 'YYYY-MM-DD'.
- Used for converting posted dates from string to date.

### `StringToNumber(strr)`

- Converts viewer count strings to numbers.
- Handles cases where counts are in thousands (K) or millions (M).

## Data Conversion

The script includes functions for converting posted dates and viewer counts to the desired format.

## Example

```python
# Example Usage
WordsToSearch = ['morocco', 'maroc', 'المغرب']

for search in WordsToSearch:
    browser = webdriver.Chrome(options=options)
    browser.get('https://www.tiktok.com')
    db = ScrapTiktokPost(browser, search)
    df = df.append(db, ignore_index=True)

df['Posted_Date'] = df['Posted_Date'].apply(convert_to_date)
df['Viewer_Count'] = df['Viewer_Count'].apply(StringToNumber)
df.to_csv('ScrapingTikTokPost.csv', index=False)
```

## License (Continued)

This project is licensed under the [Issame].

## Contact

For questions, feedback, or further assistance, feel free to contact:

- **Your Name**
  - Email: [your-email@example.com](mailto:issamalgoubahi@gmail.com)
  - GitHub: [Elgoubbahi-Issame](https://github.com/Elgoubbahi-Issame/)

