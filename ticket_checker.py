from selenium import webdriver
from selenium.webdriver.common.by import By
import firebase_admin
from firebase_admin import credentials, messaging

# Path to your downloaded service account JSON file
cred = credentials.Certificate("service_account.json")
firebase_admin.initialize_app(cred)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("start-maximized")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('log-level=3')
options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# options.add_argument('--window-size=1920x1080')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument('log-level=3')

driver = webdriver.Chrome(options=chrome_options)

# Change userAgent
driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

# Add implicit wait
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
cred = credentials.Certificate("service_account.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
driver.implicitly_wait(10)

link="https://shop.royalchallengers.com/ticket"


driver.get(link)

driver.implicitly_wait(10)
elems=driver.find_elements(By.CSS_SELECTOR,".css-q38j1a")

if len(elems)!=2:
  print(elems)
  print(len(elems))
  print("not yet")
else:
  send_push_notification(
    token='csbvwkfFTg6sH6Ct_jgNwa:APA91bGqgYIgKPXJ8zcrUhpu4sUCo0jeoykAsKB1CE5hlufBTHvCkouDWz_sH4FRuStsJ8a-8zDLz2fxTVNFJA_rKs5C3098sRQeSCi66aawVVdomw2ruvY',
    title='RCB vs CSK tickets are out',
    body='Grab em now!!!!'
)



