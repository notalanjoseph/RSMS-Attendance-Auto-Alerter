import requests as rq
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import time
import maskpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
# from dotenv import load_dotenv 


def login_n_scrape(login_details, url=False) :
    # Function that logs in a user and scrapes data from url. If url is False or None, it simply logs the user in
    with rq.Session() as session :
        response = session.post("https://www.rajagiritech.ac.in/stud/ktu/student/varify.asp", login_details)
        if url :
            response = session.get(url)
    return response


def get_attendence_details(login_details, sem, branch):
    def scraper(response) :
        soup = bs(response.content, "html.parser")
        dateData = soup.find_all('td', {"bgcolor": "#aaaaaa", "height": "35"})
        leaveData = dict()
        user = login_details["Userid"]
        leaveData["uid"] = user
        leaveData["leaves"] = list()

        for date in dateData:
            siblings = date.find_next_siblings("td")
            dateString = date.string
            dateleaves = list()
            for i in range(0, 7):
                sibling = siblings[i]
                if sibling["bgcolor"] == "#9f0000":
                    leavedate = sibling.find("font").string
                    dateleaves.append(leavedate)

            leaveData["leaves"].append({dateString: dateleaves})

        return leaveData

    res_str1 = f"https://www.rajagiritech.ac.in/stud/ktu/student/Leave.asp?code={str(datetime.today().year)+sem+branch}"
    res_str2 = f"https://www.rajagiritech.ac.in/stud/ktu/student/Leave.asp?code={str(datetime.today().year-1)+sem+branch}"
    response1 = login_n_scrape(login_details, res_str1)
    response2 = login_n_scrape(login_details, res_str2)
    leaveData1 = scraper(response1)
    leaveData2 = scraper(response2)
    leaveData1["leaves"].extend(leaveData2["leaves"])

    return leaveData1


# FETCHING YOUR CREDENTIALS
uid = os.getenv("YOUR_UID")
password = os.getenv("RSMS_PASSWORD")
sem = os.getenv("SEMESTER")
branch = os.getenv("BRANCH")
#load_dotenv()
from_address = os.getenv('GMAIL_ID')
gmail_api = os.getenv('GMAIL_API')
# for local testing only
if not uid:
    uid = str(input("Enter Uid: "))
if not password:
    password = maskpass.askpass("Enter password: ")
if not sem:
    sem = str(input("Enter Semester: "))
if not branch:
    branch = str(input("Enter branch: "))
if not from_address:
    from_address = str(input("Enter sender's gmail id: "))
if not gmail_api:
    gmail_api = str(input("Enter gmail api: "))


# SCRAPE FOR LEAVE DATES
jovanData = get_attendence_details({ "Userid": uid, "Password": password }, sem, branch)
#data = {'uid': 'u2103021', 'leaves': [{'5-Oct-2023': ['101003/CS500C', '101908/CO500F']}, {'18-Oct-2023': ['101003/CS500B']}, {'20-Oct-2023': ['101003/CS500A', '101003/CS500C']}, {'17-Nov-2023': ['101003/CS500C']}, {None: []}]}
leave_dates = []
for i in jovanData["leaves"]:
    leave_dates.append(*i)
print(f'\nAll leave dates - {leave_dates}\n')


# last 3 days date
today = datetime.today().strftime('%e-%b-%Y')
today = today.replace(' ', '')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%e-%b-%Y')
yesterday = yesterday.replace(' ', '')
ereyesterday = (datetime.today() - timedelta(days=2)).strftime('%e-%b-%Y')
ereyesterday = ereyesterday.replace(' ', '')
days = [ereyesterday, yesterday, today]
print(f'Last 3 days were - {days}\n')


# initialize smtp object
smtp_object = smtplib.SMTP_SSL('smtp.gmail.com', 465)
to_address = "u{}@rajagiri.edu.in".format(uid[1:])
smtp_object.login(from_address, gmail_api)
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address

# send email
took_leave = 0
for day in days:
    if day not in leave_dates:
        continue
    else:
        took_leave = 1
        msg['Subject'] = "ABSENT on {}".format(day)
        body = 'Good day student,\n\tyou were marked absent on {}.\n\nCheck your RSMS attendance page for more details.\nContact your professor if you were marked absent by mistake.\n\nIf you recieved such an email already, please ignore.'.format(day)

    body = body + "\n\n\n\n\n\n\nThis is an automated email. Please contact in case of any error."
    msg.attach(MIMEText(body, 'plain'))
    smtp_object.sendmail(from_address, to_address, msg.as_string())
    time.sleep(1)
    del msg['Subject']
    del msg.get_payload()[0]

if(took_leave == 0):
    msg['Subject'] = "NOT absent on last 3 days!"
    body = 'Good day student,\n\tyou were not marked absent for any classes today, yesterday, and the day before yesterday.\nIt was either a holiday or You attended all the classes!\n\nCheck your RSMS attendance page for more details.'
    body = body + "\n\n\n\n\n\n\nThis is an automated email. Please contact in case of any error."
    msg.attach(MIMEText(body, 'plain'))
    smtp_object.sendmail(from_address, to_address, msg.as_string())


smtp_object.quit()
