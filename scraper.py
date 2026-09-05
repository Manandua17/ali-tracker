import re
import csv
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

def get_cashback():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Target the Rakuten Canada page
        page.goto("https://www.rakuten.ca/aliexpress", wait_until="domcontentloaded")
        content = page.content()
        
        # Extract the percentage
        match = re.search(r'(\d+(?:\.\d+)?)%\s*Cash Back', content, re.IGNORECASE)
        rate = match.group(1) if match else "0"
        
        browser.close()
        return rate

if __name__ == "__main__":
    rate = get_cashback()
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    file_path = 'cashback_history.csv'
    
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Date', 'Rate'])
        writer.writerow([date, rate])
        
    print(f"Recorded {rate}% on {date}")
