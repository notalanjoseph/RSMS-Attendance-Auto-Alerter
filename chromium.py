from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import bs4
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

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
uid = os.getenv("YOUR_UID")
password = os.getenv("RSMS_PASSWORD")

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
soup = bs4.BeautifulSoup(driver.page_source, "lxml")

today = datetime.date.today().strftime('%e-%b-%Y')
today = today.replace(' ', '')
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%e-%b-%Y')
yesterday = yesterday.replace(' ', '')
ereyesterday = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%e-%b-%Y')
ereyesterday = ereyesterday.replace(' ', '')
days = [ereyesterday, yesterday, today]

smtp_object = smtplib.SMTP('smtp.elasticemail.com', 2525)
smtp_object.ehlo()  # this line should always come after the line above
smtp_object.starttls()
from_address = "notalan.notification@gmail.com"
to_address = "u{}@rajagiri.edu.in".format(uid[1:])
smtp_object.login(from_address, "1075738EE6A62D415E157663391DEABC06B1")
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address

for day in days:
    tag = soup.find(string=day)
    if tag != None:
        msg['Subject'] = "ABSENT on {}".format(day)
        body = 'Hi student,\nyou were marked absent on {}.\nContact your professor if you were marked absent by mistake.\n\nIf you recieved this email already, please ignore.'.format(day)

    else:
        msg['Subject'] = "NOT Absent on {}".format(day)
        body = '\n\nYou were not marked absent on {} in RSMS\nOR\nyour professor did not update RSMS yet OR it was a holiday.'.format(day)

    body = body + "\n\n\n\n\nThis is an automated email. Please contact in case of any error."
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    smtp_object.sendmail(from_address, to_address, text)
    del msg['Subject']
    del msg.get_payload()[0]

smtp_object.quit()
driver.quit()
time.sleep(2)
