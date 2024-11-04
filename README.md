# Sitemap Link Extractor

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)  
A flexible Python tool to extract URLs from various types of XML and HTML sitemaps. Supports multiple extraction options, including single files, folders, URL ranges, and index sitemaps with nested links. Outputs extracted URLs in `TXT`, `CSV`, or `XLSX` formats for flexible data management.

**Author**: Neeraj Sihag  
**Repository**: [GitHub - Sitemap Link Extractor](https://github.com/Neeraj-Sihag/Sitemap-Link-Extractor)  
**GitHub Profile**: [Neeraj Sihag](https://github.com/Neeraj-Sihag/)

> **Need to download sitemaps first?** Check out my other repository: [Sitemap Downloader](https://github.com/Neeraj-Sihag/Sitemap-Downloader).

---

## ✨ Features

- **Single File Extraction**: Extract URLs from a single downloaded XML or HTML sitemap file.
- **Folder Extraction**: Extract URLs from all sitemaps in a specific folder.
- **URL Extraction**: Fetch and extract links directly from a live sitemap URL.
- **Range-Based Extraction**: Specify a base URL and range to extract URLs from multiple numbered sitemaps.
- **Index Sitemap Extraction**: Extract URLs from an index sitemap and all its child sitemaps.

---

## ⚙️ Prerequisites

1. **Python 3.7+**
2. **Firefox Browser** - [Download here](https://www.mozilla.org/en-US/firefox/new/).
3. **GeckoDriver** - [Install instructions](https://github.com/mozilla/geckodriver/releases).  
   - Place `geckodriver` in your system’s PATH or specify its location in the script.

---

## 🚀 Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Neeraj-Sihag/Sitemap-Link-Extractor.git
   cd Sitemap-Link-Extractor
   ```

2. **Install Dependencies**  
   - Using `requirements.txt`:  
     ```bash
     pip install -r requirements.txt
     ```
   - Or install directly:  
     ```bash
     pip install selenium pandas beautifulsoup4 lxml
     ```

---

## 🧩 Usage

Run the script:

```bash
python sitemap-link-extractor.py
```

### Options

1. **Extract from a Downloaded Sitemap File**: Enter the path to a saved XML or HTML sitemap.
   - Example: `C:/path/to/sitemap.xml`

2. **Extract from All Sitemaps in a Folder**: Enter the folder path containing multiple sitemaps.
   - Example: `C:/path/to/sitemaps_folder/`

3. **Extract from a Sitemap URL**: Provide the URL of an online sitemap.
   - Example: `https://example.com/sitemap.xml`

4. **Extract from a Range of Sitemap URLs**: Define a base URL and range for multiple numbered sitemaps.
   - Example: `https://example.com/sitemap-{}.xml`  
     Starting number: `1`, Ending number: `50`

5. **Extract from an Index Sitemap with Child Sitemaps**: Enter an index sitemap URL to extract URLs from it and its child sitemaps.
   - Example: `https://example.com/sitemap_index.xml`

### Saving Options

- Select the desired output format (`TXT`, `CSV`, `XLSX`) when prompted.
- Choose to save links from each sitemap in separate files or combine them into one.

### Example Output

```plaintext
==========================================
Sitemap Link Extractor by Neeraj Sihag  
Repo: https://github.com/Neeraj-Sihag/Sitemap-Link-Extractor
Profile: https://github.com/Neeraj-Sihag/
==========================================

Choose an option:
1. Extract URLs from a downloaded sitemap file
2. Extract URLs from all sitemaps in a folder
3. Extract URLs from a sitemap URL
4. Extract URLs from a range of sitemap URLs
5. Extract URLs from an index sitemap and its child sitemaps
Enter your choice (1, 2, 3, 4, or 5): 
```

### Output

- **Extracted links** are saved in the `output` directory, organized by domain name.
- Each file will be named according to the domain and specified options, such as `sitemap-1.txt` or `example.com_range.csv`.

---

## 📌 Additional Information

- **Interrupting**: Press `Ctrl+C` to stop the script gracefully.
- **Headless Mode**: Firefox runs in headless mode by default. To disable, remove the `--headless` argument in the script.

---

## 🛠 Troubleshooting

- **Browser Not Starting**: Ensure `geckodriver` is installed and paths to both Firefox and GeckoDriver are correct.
- **Permission Issues**: Verify write permissions for the output directory.

For **Windows**:
   - Place `geckodriver.exe` in `C:/WebDrivers` or update the path in the script.
   - Run `python sitemap-link-extractor.py` from the command prompt.

For **Linux**:
   - Place `geckodriver` in `/usr/local/bin/` or update the path in the script.
   - Run `python3 sitemap-link-extractor.py` from the terminal.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
