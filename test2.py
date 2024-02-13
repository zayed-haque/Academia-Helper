from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import username, password

driver = webdriver.Chrome(executable_path="C:/Users/ayush/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver.get("https://academia.srmist.edu.in/#Page:My_Attendance")
driver.switch_to.frame('zohoiam')
driver.find_element(By.ID, "login_id").send_keys(username) 
driver.find_element(By.ID, "nextbtn").click()
password_element = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.ID, "password")))
password_element.send_keys(password)
button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "nextbtn")))
button.click()
# table = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.TAG_NAME, 'td')))
# print(table.text)
try:
    # table = driver.find_element_by_xpath("""//*[@id="zc-viewcontainer_My_Attendance"]/div/div[4]/div/table[3]""")
    table = driver.find_element_by_xpath("""/html/body/div[3]/div[2]/div[3]/div[2]/div[2]/table[2]/tbody/tr/td/div/div[4]/div/table[3]""")

    # Find all rows in the table
    rows = table.find_elements_by_xpath(".//tr")

    # Iterate through each row and extract the data
    for row in rows:
        # Extract data from each cell in the row
        cells = row.find_elements_by_xpath(".//td")
        row_data = [cell.text for cell in cells]
        # Print or process the extracted data as needed
        print(row_data)

except Exception as e:
    print(e)
    print("Attendance fetch failed")
    # raise Exception(f"Attendance fetch failed: {str(e)}")