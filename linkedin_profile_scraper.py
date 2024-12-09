import argparse
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def extract_company_name_from_domain(domain):
    company_name = domain.split('.')[0]
    print(f"Extracted company name from domain {domain}: {company_name}")
    return company_name

def build_queries(domain, scan_mode="fast"):
    company_name = extract_company_name_from_domain(domain)

    if scan_mode == "fast":
        queries = [
            f"site:linkedin.com/in \"{company_name}\"",
            f"site:linkedin.com/in \"works at {company_name}\"",
        ]
    elif scan_mode == "full":
        queries = [
            f"site:linkedin.com/in \"{company_name}\"",
            f"site:linkedin.com/in \"works at {company_name}\"",
            f"site:linkedin.com/in \"{company_name} team\"",
            f"site:linkedin.com/in \"{company_name} manager\"",
            f"site:linkedin.com/in \"{company_name} developer\"",
            f"site:linkedin.com/in \"{company_name} engineer\"",
            f"site:linkedin.com/in \"{company_name} marketing\"",
            f"site:linkedin.com/in \"{company_name} sales\"",
            f"site:linkedin.com/in \"{company_name} human resources\"",
            f"site:linkedin.com/in \"project at {company_name}\"",
            f"site:linkedin.com/in \"team at {company_name}\"",
            f"site:linkedin.com/in \"office of {company_name}\"",
        ]
    else:
        raise ValueError("Invalid scan mode. Use 'fast' or 'full'.")

    print(f"Generated queries for domain {domain} (mode {scan_mode}): {queries}")
    return queries

def extract_name_surname(link):
    link = re.sub(r"https?://[a-z]{2,3}\.linkedin\.com/in/", "", link)
    parts = link.split('-')
    if len(parts) >= 2:
        first_name = parts[0]
        last_name = parts[1]
        print(f"Extracted first name: {first_name}, last name: {last_name} from {link}")
        return f"{first_name}.{last_name}@".lower()
    print(f"Unable to extract first and last names from {link}")
    return None

def search_duckduckgo(query, max_pages=10):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    print(f"Launching WebDriver for query: {query}")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://duckduckgo.com/")

    try:
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        links = []
        current_page = 0

        while current_page < max_pages:
            print(f"Collecting results from page {current_page + 1}...")
            results = driver.find_elements(By.XPATH, "//a[@href]")
            for result in results:
                link = result.get_attribute("href")
                if "linkedin.com/in" in link:
                    links.append(link)

            current_page += 1
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "button#more-results")
                next_button.click()
                time.sleep(3)
            except Exception as e:
                if "no such element" in str(e):
                    print("Next page not found or no more pages available.")
                else:
                    print(f"Error while attempting to click the navigation button: {e}")
                break

        print(f"Collected links: {links}")
        return links

    except Exception as e:
        print(f"Error during search_duckduckgo execution: {e}")
        return []

    finally:
        driver.quit()

def search_with_multiple_queries(domain, max_pages=5, scan_mode="fast"):
    queries = build_queries(domain, scan_mode)
    all_results = set()

    for query in queries:
        print(f"\nExecuting search with query: {query}")
        try:
            results = search_duckduckgo(query, max_pages)
            if results:
                print(f"Results found for query: {results}")
                all_results.update(results)

            delay = random.uniform(4, 8)
            print(f"Waiting {delay:.2f} seconds before the next query...")
            time.sleep(delay)

        except Exception as e:
            print(f"Error during search with query '{query}': {e}")

    print(f"All found results: {list(all_results)}")
    return list(all_results)

def generate_email(full_name, domain):
    email = f"{full_name}{domain}".lower()
    print(f"Generated email: {email}")
    return email

def save_emails_to_file(profiles, domain):
    print(f"Saving emails to file...")
    try:
        with open("employee_emails.txt", "w") as file:
            for profile in profiles:
                full_name = extract_name_surname(profile)
                if full_name:
                    email = generate_email(full_name, domain)
                    file.write(f"{email}\n")
                    print(f"Saved email: {email}")
    except Exception as e:
        print(f"Error while saving emails: {e}")

def main():
    parser = argparse.ArgumentParser(description="Search LinkedIn profiles and generate associated emails.")
    parser.add_argument("-d", "--domain", required=True, help="Company's domain (e.g., company.com)")
    parser.add_argument("-s", "--scan", choices=["fast", "full"], default="fast", help="Scan mode: 'fast' or 'full' (default: fast)")
    args = parser.parse_args()

    domain = args.domain
    scan_mode = args.scan

    print(f"Searching LinkedIn profiles for domain: {domain} (mode {scan_mode})")

    try:
        profiles = search_with_multiple_queries(domain, max_pages=5, scan_mode=scan_mode)

        if not profiles:
            print("\nNo profiles found.")
        else:
            print("\nProfiles found and emails generated:")
            save_emails_to_file(profiles, domain)

    except Exception as e:
        print(f"Error during main execution: {e}")

if __name__ == "__main__":
    main()
