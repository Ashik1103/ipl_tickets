from selenium import webdriver
from selenium.webdriver.common.by import By
import firebase_admin
from firebase_admin import credentials, messaging
from flask import Flask
import json
import os
app = Flask(__name__)
import chromedriver_autoinstaller 


firebase_json = os.getenv("FIREBASE_CREDENTIALS")
firebase_dict = json.loads(firebase_json)
cred = credentials.Certificate(firebase_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
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

@app.route("/", methods=["GET"])
def home():
    return "Its running!!!"

@app.route("/check_tickets", methods=["GET"])
def check_tickets():
    chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")


    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'
    })

    try:
        driver.get("https://shop.royalchallengers.com/ticket")
        driver.implicitly_wait(10)
        elems = driver.find_elements(By.CSS_SELECTOR, ".css-q38j1a")
        print(f"Found {len(elems)} elements")

        if len(elems) != 2:
            return "Tickets not yet available"

        send_push_notification(
            token='csbvwkfFTg6sH6Ct_jgNwa:APA91bGqgYIgKPXJ8zcrUhpu4sUCo0jeoykAsKB1CE5hlufBTHvCkouDWz_sH4FRuStsJ8a-8zDLz2fxTVNFJA_rKs5C3098sRQeSCi66aawVVdomw2ruvY',
            title='RCB vs CSK tickets are out',
            body='Grab em now!!!!'
        )
        return "Notification sent!"
    except Exception as e:
        print("Error:", e)
        return "An error occurred"
    finally:
        driver.quit()

# Required for Render
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
