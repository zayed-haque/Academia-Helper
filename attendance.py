from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import username, password

driver = webdriver.Chrome()
driver.get("https://academia.srmist.edu.in/#Page:My_Attendance")
driver.switch_to.frame('zohoiam')
driver.find_element(By.ID, "login_id").send_keys(username) 
driver.find_element(By.ID, "nextbtn").click()
password_element = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.ID, "password")))
password_element.send_keys(password)
button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "nextbtn")))
button.click()
driver.get("https://academia.srmist.edu.in/#Page:My_Attendance")
table = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "(//table)[5]")))
print(table.text)