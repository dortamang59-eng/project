import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ===== CONFIGURATION =====
BASE_FOLDER = r"D:\HRS_DOC"   # Main folder where employee sub-folders exist
URL = "https://sttn.sociair.io/login"  # Website URL
USERNAME = "subashlama22836@gmail.com"
PASSWORD = "Lama123@#"

# Mapping file keywords to dropdown options
DOC_TYPE_MAPPING = {
    "slc": "SLC Certificate",
    "see": "SEE Certificate",
    "cv": "Curriculum Vitae",
    "marriage": "Marriage Certificate",
    "nid": "National ID",
    "citizenship": "Citizenship",
    "experience": "Experience Certificate",
    "bachelor": "Bachelor Certificate",
    "master": "Master Certificate",
    "other": "Other Document"
}

# ===== SELENIUM SETUP =====
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get(URL)
wait = WebDriverWait(driver, 20)

# ===== LOGIN =====
username_field = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Enter your username, email or number']"))
)
username_field.send_keys(USERNAME)

password_field = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Enter your password']"))
)
password_field.send_keys(PASSWORD)

login_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(normalize-space(.), 'Login')]"))
)
login_button.click()

print("✅ Logged in successfully!")
print("Current URL after login:", driver.current_url)
driver.save_screenshot("after_login.png")

# ===== NAVIGATE TO EMPLOYEE PAGE =====
# Wait until page is fully loaded by checking the URL or presence of Employee menu/button
wait.until(EC.url_contains("/dashboard"))  # Adjust if needed, or remove if uncertain

# Click on "Employee" menu - if there is a menu with Employee text
employee_menu = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Employee')]"))
)
employee_menu.click()
sleep(2)

# ===== SEARCH AND NAVIGATE TO EMPLOYEE DETAILS =====
employee_name = input("Enter employee name to upload documents: ")

# Wait for search box and enter employee name
search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search']")))
search_box.clear()
search_box.send_keys(employee_name)
search_box.send_keys(Keys.ENTER)
sleep(2)

# Find employee link by name dynamically
employee_link_element = wait.until(
    EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{employee_name}')]"))
)
employee_url = employee_link_element.get_attribute("href")
print(f"Navigating to employee detail page: {employee_url}")
employee_link_element.click()
sleep(2)

# ===== NAVIGATE TO DOCUMENTS TAB =====
documents_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Documents')]")))
documents_tab.click()
sleep(2)

# ===== FIND EMPLOYEE FOLDER LOCALLY =====
employee_folder = os.path.join(BASE_FOLDER, employee_name)
if not os.path.exists(employee_folder):
    print(f"❌ Employee folder not found: {employee_folder}")
    driver.quit()
    exit()

# ===== UPLOAD FILES =====
for file_name in os.listdir(employee_folder):
    file_path = os.path.join(employee_folder, file_name)
    if os.path.isfile(file_path):
        # Default doc type
        doc_type = "Other Document"

        # Match filename with doc type
        for key in DOC_TYPE_MAPPING:
            if key.lower() in file_name.lower():
                doc_type = DOC_TYPE_MAPPING[key]
                break

        print(f"📂 Uploading {file_name} as {doc_type}")

        # Click "Add Document" button
        add_doc_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Document')]")))
        add_doc_btn.click()
        sleep(1)

        # Select document type dropdown
        doc_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='documentType']")))
        select = Select(doc_dropdown)
        select.select_by_visible_text(doc_type)

        # Upload file - the file input may be hidden, so make sure it is interactable
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(file_path)

        # Submit document
        submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
        submit_btn.click()

        sleep(2)

print("✅ All files uploaded successfully!")
driver.quit()
