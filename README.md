# LinkedIn Profile Scraper

This project is a Python script that automates the process of searching for LinkedIn profiles based on a company's domain and generates potential email addresses for employees. It uses Selenium WebDriver to perform web searches and processes the results to extract relevant information.

## Features

- **Domain-Based Profile Search**: Generates search queries based on the provided company's domain.
- **Search Modes**: Offers two modes: `fast` (fewer queries) and `full` (more detailed queries).
- **DuckDuckGo Integration**: Uses DuckDuckGo to perform profile searches.
- **Email Generation**: Extracts names from LinkedIn profile URLs and generates email addresses in the format `firstname.lastname@companydomain`.
- **Result Export**: Saves the generated email addresses to a file (`employee_emails.txt`).

## Requirements

- Python 3.8 or later
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)
- Required Python packages:
  - `selenium`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/linkedin-profile-scraper.git
   cd linkedin-profile-scraper
   ```
2. Install the required Python packages:
   ```bash
   pip install selenium
   ```
3. Download and set up ChromeDriver:
   - [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
   - Ensure ChromeDriver is added to your system's PATH.

## Usage

Run the script with the following command:
```bash
python linkedin_profile_scraper.py -d <company_domain> [-s <scan_mode>]
```

### Arguments

- `-d`, `--domain` (required): The company's domain (e.g., `example.com`).
- `-s`, `--scan` (optional): The scan mode. Options are:
  - `fast` (default): Performs a quick search with fewer queries.
  - `full`: Performs a more exhaustive search.

### Example

Fast mode:
```bash
python linkedin_profile_scraper.py -d example.com -s fast
```

Full mode:
```bash
python linkedin_profile_scraper.py -d example.com -s full
```

## Output

- The script generates a file named `employee_emails.txt` in the working directory containing the generated email addresses.

## Error Handling

- If the "Next" button is not found during the search, the script displays the message:
  ```
  Next page not found or no more pages available.
  ```
- Other errors are logged with descriptive messages for easier debugging.

## Disclaimer

This script is intended for educational and ethical purposes only. Ensure you comply with all applicable laws and LinkedIn's terms of service when using this tool.

