import requests

try:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    # Let's try to fetch from a known public API or use a fallback
    url = "https://api.gold-api.com/price/XAU/INR" # Checking if this free endpoint exists
    r = requests.get(url, headers=headers, timeout=5)
    print("Gold API Status:", r.status_code)
    print("Gold API Response:", r.text)
except Exception as e:
    print("Error:", e)
