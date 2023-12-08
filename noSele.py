import requests as rq
from bs4 import BeautifulSoup as bs
from datetime import datetime

def login_n_scrape(login_details, url=False) :
    """
    Function that logs in a user and scrapes data from a mentioned url
    If url is False or None, it simply logs the user in
    """
    with rq.Session() as session :
        response = session.post("https://www.rajagiritech.ac.in/stud/ktu/student/varify.asp", login_details)
        if url :
            response = session.get(url)

    return response


def extract_profile_details(login_details) :
    response = login_n_scrape(login_details, "https://www.rajagiritech.ac.in/stud/ktu/Student/Home.asp")
    
    soup = bs(response.content, "html.parser")
    for div in soup.find_all("div") :
        try :
            if div["class"] == ["scroller"] :
                # Scrape the users name
                name = div.text
                name = name[name.index(":")+1: -1].strip()
                # Scrape the users image
                imgs = soup.find_all("img")
                # Extract the photo and sign file names
                for i in imgs :
                    img = i["src"]
                    if img[-14: -19: -1][-1::-1] == "Photo" :
                        img_name = img
                    elif img[-14: -18: -1][-1::-1] == "sign" :
                        sign_name = img
                
                img_url = "https://www.rajagiritech.ac.in/stud/ktu/" + img_name[3:]
                sign_url = "https://www.rajagiritech.ac.in/stud/ktu/" + sign_name[3:]

                return {
                    "User_name": name,
                    "Userid": login_details["Userid"],
                    "User_image": img_url,
                    "User_sign": sign_url
                }

        except Exception as ex :
            print(f"Exception: {ex}")

    return False


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
    print(leaveData1)
    return leaveData1



from datetime import timedelta
import time
import maskpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# ENTER YOUR CREDENTIALS
uid = os.getenv("YOUR_UID")
password = os.getenv("RSMS_PASSWORD")
sem = os.getenv("SEMESTER")
branch = os.getenv("BRANCH")

if uid == "":
    uid = str(input("Enter Uid: "))
if password == "":
    password = maskpass.askpass("Enter password: ")

# last 3 days date
today = datetime.today().strftime('%e-%b-%Y')
today = today.replace(' ', '')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%e-%b-%Y')
yesterday = yesterday.replace(' ', '')
ereyesterday = (datetime.today() - timedelta(days=2)).strftime('%e-%b-%Y')
ereyesterday = ereyesterday.replace(' ', '')
days = [ereyesterday, yesterday, today]

# initialize smtp object
smtp_object = smtplib.SMTP('smtp.elasticemail.com', 2525)
smtp_object.ehlo()  # this line should always come after the line above
smtp_object.starttls()
from_address = "notalan.notification@gmail.com"
to_address = "u{}@rajagiri.edu.in".format(uid[1:])
smtp_object.login(from_address, "1075738EE6A62D415E157663391DEABC06B1")
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address



jovanData = get_attendence_details({ "Userid": uid, "Password": password }, sem, branch)
#data = {'uid': 'u2103021', 'leaves': [{'5-Oct-2023': ['101003/CS500C', '101908/CO500F']}, {'18-Oct-2023': ['101003/CS500B']}, {'20-Oct-2023': ['101003/CS500A', '101003/CS500C']}, {'17-Nov-2023': ['101003/CS500C']}, {None: []}]}
leave_dates = []
for i in jovanData["leaves"]:
    leave_dates.append(*i)
#print(leave_dates)


flag = 0
for day in days:
    if day not in leave_dates:
        continue
    else:
        flag = 1
        msg['Subject'] = "ABSENT on {}".format(day)
        body = 'Good day student,\n\tyou were marked absent on {}.\n\nCheck your RSMS attendance page for more details.\nContact your professor if you were marked absent by mistake.\n\nIf you recieved this email already, please ignore.'.format(day)

    body = body + "\n\n\n\n\n\n\nThis is an automated email. Please contact in case of any error."
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    smtp_object.sendmail(from_address, to_address, text)
    time.sleep(1)
    del msg['Subject']
    del msg.get_payload()[0]

if(flag == 0):
    msg['Subject'] = "NOT absent on last 3 days!"
    body = 'Good day student,\n\tyou were not marked absent for any classes today, yesterday, and the day before yesterday.\nIt was either a holiday or You attended all the classes!\n\nCheck your RSMS attendance page for more details.'
    body = body + "\n\n\n\n\n\n\nThis is an automated email. Please contact in case of any error."
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    smtp_object.sendmail(from_address, to_address, text)


smtp_object.quit()
