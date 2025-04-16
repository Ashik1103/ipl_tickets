from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

app = Flask(__name__)

# Load Firebase credentials from environment variable
firebase_json = os.getenv("FIREBASE_CREDENTIALS")
firebase_dict = json.loads(firebase_json)
cred = credentials.Certificate(firebase_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Function to send a push notification
def send_push_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )
    response = messaging.send(message)
    print("Successfully sent message:", response)

# Basic health check
@app.route("/", methods=["GET"])
def home():
    return "It's running!!!"

# Route to check ticket availability
@app.route("/check_tickets", methods=["GET"])
def check_tickets():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--remote-debugging-port=9222')  # Important for headless Chrome
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://shop.royalchallengers.com/ticket")
        driver.implicitly_wait(10)

        elems = driver.find_elements(By.CSS_SELECTOR, ".css-q38j1a")
        print(f"Found {len(elems)} elements")

        if len(elems) != 2:
            return "Tickets not yet available"

        # Example token – replace with your FCM token
        send_push_notification(
            token='csbvwkfFTg6sH6Ct_jgNwa:APA91bGqgYIgKPXJ8zcrUhpu4sUCo0jeoykAsKB1CE5hlufBTHvCkouDWz_sH4FRuStsJ8a-8zDLz2fxTVNFJA_rKs5C3098sRQeSCi66aawVVdomw2ruvY',
            title='RCB vs CSK tickets are out',
            body='Grab em now!!!!'
        )
        return "Notification sent!"
    except Exception as e:
        print("Error:", e)
        return f"An error occurred: {e}"
    finally:
        driver.quit()

# Optional route to check Chrome installation
@app.route("/check_chrome", methods=["GET"])
def check_chrome():
    try:
        import subprocess
        output = subprocess.check_output(["/usr/bin/google-chrome", "--version"])
        return f"Chrome installed: {output.decode().strip()}"
    except Exception as e:
        return f"Chrome not found: {e}"

# Run app (for Docker/Render)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
