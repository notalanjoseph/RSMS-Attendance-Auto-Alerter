from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# ENTER YOUR CREDENTIALS
uid = "U2103021"
password = "210555"

driver.get('https://www.rajagiritech.ac.in/stud/ktu/student/')
time.sleep(2)
driver.find_element("name", "Userid").send_keys(uid)
driver.find_element("name", "Password").send_keys(password)
driver.find_element("name", "Password").send_keys("\ue007")
time.sleep(2)

attendance_link = driver.find_element(By.LINK_TEXT, "Attendance")
attendance_link.click()
time.sleep(2)

submit_button = driver.find_element(By.CLASS_NAME, "ibox1")
submit_button.click()
time.sleep(2)

todays_date = datetime.date.today().strftime('%d-%b-%Y')
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%d-%b-%Y')
ereyesterday = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%d-%b-%Y')
days = [ereyesterday, yesterday, todays_date]

smtp_object = smtplib.SMTP('smtp-relay.brevo.com', 587)
smtp_object.ehlo()  # this line should always come after the line above
smtp_object.starttls()
from_address = "notalan.notification@gmail.com"
to_address = "u{}@rajagiri.edu.in".format(uid[1:])
smtp_object.login(from_address, "Lyj8RhM6TxkO3HDB")
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address

try:
    td_element = driver.find_element(By.XPATH, "//td[text()=todays_date]")
    msg['Subject'] = "ABSENT on {}".format(todays_date)
    body = 'Hi student,\nyou were marked absent on {}.\nMake sure to contact your professor if this was a mistake.\n\nIf you recieved this email already, please ignore.'
except:
    msg['Subject'] = "PRESENT on {}".format(todays_date)
    body = 'Hi student please ignore.\n\nYou were marked present or professor didnt update rsms'

finally:
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    smtp_object.sendmail(from_address, to_address, text)
    smtp_object.quit()

driver.quit()
time.sleep(2)
