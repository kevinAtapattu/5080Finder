import requests
import os
from time import sleep
from datetime import datetime

# Canada Computers RTX 5080 URL (Brampton, Oakville, & Mississauga Store)


arr = ["https://www.canadacomputers.com/en/search?s=5080&pickup=15","https://www.canadacomputers.com/en/search?s=5080&pickup=4", 
      "https://www.canadacomputers.com/en/search?s=5080&pickup=69", "https://www.canadacomputers.com/en/search?s=5090&pickup=15",
      "https://www.canadacomputers.com/en/search?s=5090&pickup=4", "https://www.canadacomputers.com/en/search?s=5090&pickup=69"
]



# Discord Webhook URL (Replace with your actual webhook)
WEBHOOK_URL = ""

# Headers to mimic a browser request (prevents bot detection)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

# Log messages to file and console
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)  # Print to console
    with open("availability_log.txt", "a") as f:  # Append to log file
        f.write(log_message + "\n")

# Check if GPU is in stock
def checkAvailability(url):
    log("🔄 Checking RTX 5080 availability...")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        # If response is successful, check stock status
        if response.status_code == 200:
            available = response.text.count("No matches were found for your search") != 2
            log(f"Stock status: {'✅ Available' if available else '❌ Not in stock'}")
            return available
        else:
            log(f"⚠️ Failed to fetch page. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        log(f"🚨 Request error: {e}")
        return False

# Send a Discord webhook notification
def sendWebhookNotification(url):
    log("📢 RTX 5080 is available! Sending Discord notification...")
    data = {
        "username": "RTX Stock Informer",
        # user ids of anyone in discord to get notified by the message
        "content": f"🎉 <@{224336449422491649}> <@{412336577948155935}> <@{182321140889288704}> GPU available! Check here: {url}"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data, timeout=10)

        # Log the webhook response
        if response.status_code == 204:
            log("✅ Webhook sent successfully!")
        else:
            log(f"⚠️ Webhook failed! Status: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        log(f"🚨 Webhook request error: {e}")

# Main loop to check stock every 3 minutes
def RunAvailabilityChecker():
    log("🚀 RTX 5080 Stock Checker is online. Checking every 3 minutes...")
    seconds = 0
    while True:
        sleep(1)
        if seconds % 180 == 0:  # Check every 3 minutes
            for url in arr:
                if checkAvailability(url):
                    sendWebhookNotification(url)
                    log("✅ Stock found. Exiting script.")

        seconds += 1

# Run the script
RunAvailabilityChecker()
