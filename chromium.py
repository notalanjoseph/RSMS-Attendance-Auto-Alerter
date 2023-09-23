from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

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


from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import maskpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ENTER YOUR CREDENTIALS
uid = "U2103021"
password = "210555"

if uid == "":
    uid = str(input("Enter Uid: "))
if password == "":
    password = maskpass.askpass("Enter password: ")

# do something to reduce log info displayed in terminal

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

# initialize smtp object
smtp_object = smtplib.SMTP('smtp-relay.brevo.com', 587)
smtp_object.ehlo()  # this line should always come after the line above
smtp_object.starttls()
from_address = "notalan.notification@gmail.com"
to_address = "u{}@rajagiri.edu.in".format(uid[1:])
smtp_object.login(from_address, "Lyj8RhM6TxkO3HDB")
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address
#smtp_object.sendmail(from_address, to_address, email_body)

try:
    td_element = driver.find_element(By.XPATH, "//td[text()=todays_date]")
    # iff no error, then the below code executes
#    print("\n U R marked absent on {}\n".format(todays_date))
    msg['Subject'] = "ABSENT on {}".format(todays_date)
    body = 'Hi student,\nyou were marked absent on {}.\nMake sure to contact your professor if this was a mistake.\n\nIf you recieved this email already, please ignore.'
except:
#    print("\n U R PRESENT\n")
    msg['Subject'] = "PRESENT on {}".format(todays_date)
    body = 'Hi student please ignore.\n\nYou were marked present or professor didnt update rsms'

finally:
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    smtp_object.sendmail(from_address, to_address, text)
    smtp_object.quit()

#print("last line")    

time.sleep(2)
