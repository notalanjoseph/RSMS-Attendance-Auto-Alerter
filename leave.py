from selenium import webdriver

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

# check for last 3 days date in the sheet
todays_date = datetime.date.today().strftime('%d-%b-%Y')
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%d-%b-%Y')
ereyesterday = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%d-%b-%Y')
days = [ereyesterday, yesterday, todays_date]

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

for day in days:
    try:
        td_element = driver.find_element(By.XPATH, "//td[text()=day]")
        # iff no error, then the below code executes
        msg['Subject'] = "ABSENT on {}".format(day)
        body = 'Hi student,\nyou were marked absent on {}.\nContact your professor if this was a mistake.\n\nIf you recieved this email already, please ignore.'.format(day)

    except:
        msg['Subject'] = "PRESENT on {}".format(day)
        body = '\n\nYou were marked present on {} in RSMS\nOR\nyour professor did not update RSMS yet.'.format(day)

    #finally:
    body = body + "\n\n\n\n\nThis is an automated email. Please contact in case of any errors."
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    smtp_object.sendmail(from_address, to_address, text)
    del msg['Subject']
    del msg.get_payload()[0]

smtp_object.quit()
driver.quit()
time.sleep(2)
