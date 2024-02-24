from flask import Flask, jsonify, request
import bcrypt
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


app = Flask(__name__)


class Credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class AuthenticationHandler:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="login",
            user="admin",
            password="admin",
            host='localhost'
        )

    def authenticate(self, credentials):
        cursor = self.conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (credentials.username,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return bcrypt.checkpw(credentials.password.encode(), result[0].encode())
        else:
            return False

    def create_user(self, username, password):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
            self.conn.commit()
            cursor.close()
            return True
        except psycopg2.errors.UniqueViolation:
            return False


auth_handler = AuthenticationHandler()
driver = None


def perform_login(username, password):
    global driver
    if driver is not None:
        return
    try:
        driver = webdriver.Chrome()
        driver.get("https://academia.srmist.edu.in")
        driver.switch_to.frame('zohoiam')
        driver.find_element(By.ID, "login_id").send_keys(username) 
        driver.find_element(By.ID, "nextbtn").click()

        password_element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "password")))
        password_element.send_keys(password)
        button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "nextbtn")))
        button.click()

    except Exception as e: 
        raise Exception(f"Login failed: {str(e)}")


def get_timetable():
    global driver
    if driver is None:
        raise Exception("")

    try:
        driver.get("https://academia.srmist.edu.in/#Page:My_Time_Table_2023_24")
        element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'element_id')))
        timetable_data = element.text
        return jsonify({"status": "success", "data": timetable_data})

    except Exception as e:
        raise Exception(f"Timetable fetch failed: {str(e)}")

def login_to_portal():
    driver.switch_to.frame('zohoiam')
    driver.find_element(By.ID, "login_id").send_keys(username)  # username
    driver.find_element(By.ID, "nextbtn").click()
    password_element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "password")))
    password_element.send_keys(password) # password
    button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "nextbtn")))
    button.click()


def get_attendance():
    global driver
    if driver is None:
        raise Exception("")

    try:
        driver.get("https://academia.srmist.edu.in/#Page:My_Attendance")
        login_to_portal()
        table = driver.find_element_by_xpath("""//*[@id="zc-viewcontainer_My_Attendance"]/div/div[4]/div/table[3]""")
        attendance_data = table.text
        return jsonify({"status": "success", "data": attendance_data})

    except Exception as e:
        raise Exception(f"Attendance fetch failed: {str(e)}")


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if auth_handler.authenticate(Credentials(username, password)):
        try:
            perform_login(username, password)
            return jsonify({'message': 'Login successful'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/attendance', methods=['POST'])
def attendance():
    return get_attendance()


@app.route('/timetable', methods=['GET'])
def timetable():
    return get_timetable()


if __name__ == '__main__':
    app.run(debug=True)
