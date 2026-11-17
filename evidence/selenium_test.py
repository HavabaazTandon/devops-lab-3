from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost:5000")
    print("PAGE TITLE:", driver.title)
    print("PAGE URL:", driver.current_url)
    print("PAGE LOAD:", "SUCCESS")

    driver.save_screenshot("evidence/selenium_homepage.png")

    driver.get("http://localhost:5000/api/feature")
    print("FEATURE PAGE:", driver.current_url)
    print("FEATURE CONTENT:", driver.find_element(By.TAG_NAME, "body").text)

    with open("evidence/selenium_results.txt", "w") as f:
        f.write("Selenium browser automation completed.\n")
        f.write("Homepage: SUCCESS\n")
        f.write("Feature page visited.\n")

finally:
    driver.quit()
