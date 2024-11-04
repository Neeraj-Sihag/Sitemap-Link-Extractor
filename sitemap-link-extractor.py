import os
import signal
import xml.etree.ElementTree as ET
import pandas as pd
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from bs4 import BeautifulSoup

# Paths to GeckoDriver and Firefox binary
geckodriver_path = "C:/WebDrivers/geckodriver.exe"  # Update this to your path
firefox_binary_path = "C:/Program Files/Mozilla Firefox/firefox.exe"  # Update this to your path

# Set up Firefox options
firefox_options = Options()
firefox_options.binary_location = firefox_binary_path
firefox_options.add_argument("--headless")

# Global control flag for graceful shutdown
driver = None
running = True

def display_intro():
    """Display the introduction with script and author details."""
    print("\n==========================================")
    print("Sitemap Link Extractor by Neeraj Sihag ")
    print("Repo: https://github.com/Neeraj-Sihag/Sitemap-Link-Extractor")
    print("Profile: https://github.com/Neeraj-Sihag/")
    print("==========================================\n")

def start_browser():
    """Start the browser session if needed."""
    global driver
    if not driver:
        print("[INFO] Starting browser session...")
        service = Service(geckodriver_path)
        driver = webdriver.Firefox(service=service, options=firefox_options)
        driver.set_page_load_timeout(60)
        print("[INFO] Browser session started successfully.\n")

def close_browser():
    """Close the browser session if it's open."""
    global driver
    if driver:
        driver.quit()
        driver = None
        print("\n[INFO] Browser session closed.")

def signal_handler(sig, frame):
    """Handle keyboard interrupt and exit gracefully."""
    global running
    running = False
    print("\n\n[INFO] Interrupted! Exiting and closing browser session...")
    close_browser()
    print("[INFO] All tasks completed.")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def fetch_sitemap(url, max_retries=3, load_timeout=60):
    """Fetch sitemap content with retries and return page source."""
    driver.set_page_load_timeout(load_timeout)
    attempts = 0
    while attempts < max_retries:
        if not running:
            return None, None  # Exit if interrupted
        try:
            print(f"[FETCHING] URL: {url}")
            driver.get(url)
            page_source = driver.page_source

            # Detect HTML or XML content
            if "<html" in page_source.lower():
                print("    [DETECTED] HTML content. Parsing as HTML sitemap.")
                return "html", page_source
            
            print("    [DETECTED] XML content. Parsing as XML sitemap.")
            return "xml", page_source
        except (WebDriverException, TimeoutException) as e:
            attempts += 1
            print(f"    [RETRY] Attempt {attempts} failed for {url}. Error: {e}")
    print(f"[ERROR] Failed to load {url} after {max_retries} attempts.")
    return None, None

def parse_sitemap_links(content_type, page_source, base_url):
    """Extract and return all links from the sitemap content, filtering out third-party links only in HTML."""
    links = []
    domain = urlparse(base_url).netloc
    
    if content_type == "xml":
        try:
            root = ET.fromstring(page_source)
            namespace = ""
            if root.tag.startswith("{"):
                namespace = root.tag.split("}")[0] + "}"
            
            for element in root.findall(f".//{namespace}loc"):
                link = element.text.strip()
                links.append(link)
            print(f"[INFO] Extracted {len(links)} links from XML sitemap.\n")
        except ET.ParseError as e:
            print("    [ERROR] XML ParseError:", e)
    
    elif content_type == "html":
        soup = BeautifulSoup(page_source, "html.parser")
        for link in soup.find_all("a", href=True):
            href = urljoin(base_url, link["href"])
            if urlparse(href).netloc == domain:  # Filter out third-party links in HTML
                links.append(href)
        print(f"[INFO] Extracted {len(links)} links from HTML sitemap.\n")
    
    return links

def save_links(links, output_dir, filename, file_format):
    """Save links to a file in the specified format."""
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, f"{filename}.{file_format}")
    
    if file_format == "txt":
        with open(filepath, "w") as f:
            for link in links:
                f.write(link + "\n")
        print(f"[SAVED] Links saved as {filepath}")
    
    elif file_format == "csv":
        pd.DataFrame(links, columns=["Links"]).to_csv(filepath, index=False)
        print(f"[SAVED] Links saved as {filepath}")

    elif file_format == "xlsx":
        pd.DataFrame(links, columns=["Links"]).to_excel(filepath, index=False)
        print(f"[SAVED] Links saved as {filepath}")

def extract_from_local_file():
    """Extract URLs from a local sitemap file."""
    filepath = input("Enter the path to the downloaded sitemap file: ")
    file_format = input("Choose output format (txt, csv, xlsx): ").strip().lower()
    filename = os.path.splitext(os.path.basename(filepath))[0]

    with open(filepath, "r", encoding="utf-8") as file:
        page_source = file.read()
    
    content_type = "xml" if filepath.endswith(".xml") else "html"
    links = parse_sitemap_links(content_type, page_source, filepath)
    save_links(links, "output", filename, file_format)

def extract_from_folder():
    """Extract URLs from all sitemap files in a specified folder."""
    folder_path = input("Enter the folder path containing sitemaps: ")
    file_format = input("Choose output format (txt, csv, xlsx): ").strip().lower()
    
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filepath.endswith(".xml") or filepath.endswith(".html"):
            with open(filepath, "r", encoding="utf-8") as file:
                page_source = file.read()
            content_type = "xml" if filepath.endswith(".xml") else "html"
            links = parse_sitemap_links(content_type, page_source, filepath)
            save_links(links, "output", filename.split(".")[0], file_format)

def extract_from_url():
    """Extract URLs from a sitemap at a given URL."""
    start_browser()
    url = input("Enter the URL of the sitemap: ")
    file_format = input("Choose output format (txt, csv, xlsx): ").strip().lower()
    domain = urlparse(url).netloc
    output_dir = os.path.join("output", domain)

    content_type, page_source = fetch_sitemap(url)
    if page_source:
        links = parse_sitemap_links(content_type, page_source, url)
        save_links(links, output_dir, "sitemap", file_format)
    close_browser()

def extract_from_range():
    """Extract URLs from a range of sitemaps based on a URL pattern."""
    start_browser()
    base_url = input("Enter the base URL structure (use '{}' as a placeholder for the number): ")
    start = int(input("Enter the starting number: "))
    end = int(input("Enter the ending number: "))
    file_format = input("Choose output format (txt, csv, xlsx): ").strip().lower()
    domain = urlparse(base_url).netloc
    output_dir = os.path.join("output", domain)

    save_option = input("Save links from each sitemap in separate files? (y/n): ").strip().lower()
    all_links = [] if save_option != "y" else None

    for i in range(start, end + 1):
        if not running:
            break  # Exit if interrupted
        url = base_url.format(i)
        print(f"\n[FETCHING] Sitemap {i}: {url}")
        content_type, page_source = fetch_sitemap(url)
        if page_source:
            links = parse_sitemap_links(content_type, page_source, url)
            if save_option == "y":
                save_links(links, output_dir, f"sitemap-{i}", file_format)
            else:
                all_links.extend(links)

    if save_option != "y":
        save_links(all_links, output_dir, f"{domain}_range", file_format)
    
    close_browser()

def extract_from_index_sitemap():
    """Extract URLs from an index sitemap and all its child sitemaps."""
    start_browser()
    url = input("Enter the URL of the index sitemap: ")
    file_format = input("Choose output format (txt, csv, xlsx): ").strip().lower()
    save_option = input("Save links from each child sitemap in separate files? (y/n): ").strip().lower()
    
    domain = urlparse(url).netloc
    output_dir = os.path.join("output", domain)
    
    content_type, page_source = fetch_sitemap(url)
    if page_source:
        main_sitemap_links = parse_sitemap_links(content_type, page_source, url)
        
        all_links = [] if save_option != "y" else None
        
        for i, child_sitemap_url in enumerate(main_sitemap_links, start=1):
            if not running:
                break  # Exit if interrupted
            print(f"\n[FETCHING] Child Sitemap {i}: {child_sitemap_url}")
            child_content_type, child_page_source = fetch_sitemap(child_sitemap_url)
            if child_page_source:
                child_links = parse_sitemap_links(child_content_type, child_page_source, child_sitemap_url)
                
                # Extract the original filename from the child sitemap URL
                filename = os.path.basename(urlparse(child_sitemap_url).path).split(".")[0]
                
                if save_option == "y":
                    save_links(child_links, output_dir, filename, file_format)
                else:
                    all_links.extend(child_links)
        
        if save_option != "y":
            save_links(all_links, output_dir, f"{domain}_all_links", file_format)
    
    close_browser()

def main():
    display_intro()
    print("Choose an option:")
    print("1. Extract URLs from a downloaded sitemap file")
    print("2. Extract URLs from all sitemaps in a folder")
    print("3. Extract URLs from a sitemap URL")
    print("4. Extract URLs from a range of sitemap URLs")
    print("5. Extract URLs from an index sitemap and all its child sitemaps")
    
    choice = input("Enter your choice (1, 2, 3, 4, or 5): ")
    
    if choice == "1":
        print("\n[START] Extracting URLs from a downloaded sitemap file...\n")
        extract_from_local_file()
    elif choice == "2":
        print("\n[START] Extracting URLs from all sitemaps in a folder...\n")
        extract_from_folder()
    elif choice == "3":
        print("\n[START] Extracting URLs from a sitemap URL...\n")
        extract_from_url()
    elif choice == "4":
        print("\n[START] Extracting URLs from a range of sitemap URLs...\n")
        extract_from_range()
    elif choice == "5":
        print("\n[START] Extracting URLs from an index sitemap and its child sitemaps...\n")
        extract_from_index_sitemap()
    else:
        print("[ERROR] Invalid choice. Exiting.\n")

try:
    main()
finally:
    close_browser()
    print("\n[INFO] All tasks completed successfully.")
