from selenium import webdriver

from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

# ENTER YOUR CREDENTIALS
uid = ""
password = ""


driver = webdriver.Edge()

# login
driver.get('https://www.rajagiritech.ac.in/stud/ktu/student/')
time.sleep(2)
driver.find_element("name", "Userid").send_keys(uid)
driver.find_element("name", "Password").send_keys(password)
# sending unicode of enter key
driver.find_element("name", "Password").send_keys("\ue007")
time.sleep(2)

# navigating to attendance page
attendance_link = driver.find_element(By.LINK_TEXT, "Attendance")
attendance_link.click()
time.sleep(2)

# navigation to attendance sheet of current sem
submit_button = driver.find_element(By.CLASS_NAME, "ibox1")
submit_button.click()
time.sleep(2)

# check for todays date in the sheet
todays_date = datetime.date.today().strftime('%d-%b-%Y')
try:
    td_element = driver.find_element(By.XPATH, "//td[text()=todays_date]")
    # iff no error, then the below code executes
    # sendemail()
    print("\n U R marked absent on {}\n".format(todays_date))
except:
    print("\n U R PRESENT\n")

time.sleep(5)
