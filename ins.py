from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.get("https://sttn.sociair.io/login")

# Wait for the first input field to appear
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "input"))
    )
    print("✅ Page fully loaded.")
except:
    print("⚠️ No input field found within timeout.")

# Save page source
with open("page_source.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

print("✅ Page source saved! Open page_source.html to check IDs.")

driver.quit()
