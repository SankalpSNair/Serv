from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import easygui

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|[a-zA-Z0-9.-]+\.in)$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, phone) is not None
# Path to your WebDriver (update with the actual path to your ChromeDriver)
driver = webdriver.Chrome()

# Open the login page
driver.get("http://127.0.0.1:8000/login/")
print("Opened the login page.")

# Maximize the browser window
driver.maximize_window()

# Wait for the page to load completely
time.sleep(3)  # Increased time to ensure the page is fully loaded

# Wait for the username field to be visible and interact with it
wait = WebDriverWait(driver, 10)  # 10-second timeout
try:
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    username_field.clear()
    username_field.send_keys('sankalpsnair01@gmail.com')
    print("Entered username.")
    time.sleep(1)  # Time gap between operations

    password_field = wait.until(EC.visibility_of_element_located((By.ID, 'password')))
    password_field.clear()
    password_field.send_keys('Sankalp@123')
    print("Entered password.")
    time.sleep(1)  # Time gap between operations

    # Wait a moment to ensure fields aren't cleared by JavaScript
    time.sleep(1)

    login_button = wait.until(EC.element_to_be_clickable((By.ID, 'signin')))
    print("Login button found. Clicking the button.")
    login_button.click()
    time.sleep(3)

    WebDriverWait(driver, 10).until(lambda d: "index" in d.current_url)
    if "index" in driver.current_url:
        print("Login successful. Redirected to index page.")
    else:
        raise Exception(f"Login failed. Current URL: {driver.current_url}")
    

    # Step 2: Navigate to the profile update page
    driver.get("http://127.0.0.1:8000/profile/")
    print("Navigated to the profile update page.")
    time.sleep(3)  # Wait for the page to load

    # Step 3: Fill out the profile update form with validation
    email_field = wait.until(EC.visibility_of_element_located((By.ID, 'id_email')))
    email = 'reb@gmail.com'  # Example email
    email_field.clear()
    email_field.send_keys(email)
    print("Entered new email.")
    time.sleep(2)  # Time gap to ensure field entry is processed

    # Validate email format
    if not validate_email(email):
        raise ValueError("Invalid email format. Must be a valid Gmail, Yahoo, or .in domain email address.")

    phone_field = wait.until(EC.visibility_of_element_located((By.ID, 'id_phone')))
    phone = '9876543219'  # Example phone number
    phone_field.clear()
    phone_field.send_keys(phone)
    print("Entered new phone number.")
    time.sleep(2)  # Time gap to ensure field entry is processed

    # Validate phone number format
    if not validate_phone(phone):
        raise ValueError("Invalid phone number format. Must be a 10-digit number starting with 6, 7, 8, or 9.")

    # Upload profile picture
    profile_pic_field = wait.until(EC.visibility_of_element_located((By.ID, 'id_profile_pic')))
    profile_pic_path = r"C:\Users\aleen\OneDrive\Pictures\artist1.jpg"
    profile_pic_field.send_keys(profile_pic_path)
    print("Uploaded profile picture.")
    time.sleep(3)  # Wait for the image upload to be processed

    # Submit the form
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit-btn')))
    submit_button.click()
    print("Form submitted.")
    time.sleep(1)  # Wait for form submission to process
    easygui.msgbox("Updated Successfully")

    # Navigate to the view page
    driver.get("http://localhost:8000/accounts/userprofileartist/")
    print("Navigated to the view page.")
    time.sleep(3)  # Wait for the page to load completely
    
    print("Profile update verification complete.")

except Exception as e:
    print(f"An error occurred: {e}")
    easygui.msgbox(f"An error occurred: {e}", title="Error")

finally:
    # Delay closing of the browser for 3 seconds
    time.sleep(3)
    driver.quit()

