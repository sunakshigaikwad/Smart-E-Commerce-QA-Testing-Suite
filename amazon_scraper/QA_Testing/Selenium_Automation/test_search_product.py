from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Start the driver
driver = webdriver.Chrome()
driver.get("http://127.0.0.1:8000/")  # Update if you're using a different local URL

try:
    # Login Step
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    email_input.send_keys("sujatamane@gmail.com")
    password_input.send_keys("123")
    login_button.click()

    print("Login successful, navigating to search...")

    # Wait for redirection and search input
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "product"))
    )
    print("Search field found, entering product name...")

    search_input.send_keys("iphone 15")
    search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    search_button.click()

    print("Test completed successfully.")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    time.sleep(3)
    driver.quit()
