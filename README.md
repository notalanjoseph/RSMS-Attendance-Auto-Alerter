# RSMS-Attendance-Auto-Alerter

<!--![main workflow](https://img.shields.io/github/actions/workflow/status/notalanjoseph/RSMS-Attendance-Auto-Alerter/actions.yml?logo=github)-->
![documentation](https://img.shields.io/readthedocs/gspread?logo=readthedocs)
![python version](https://img.shields.io/pypi/pyversions/gspread?style=pypi)
 
RSET students are asked to regularly check if they are wrongly marked absent in RSMS website. RSMS attendance gets locked 3 days after each class, so if students fail to realise and report any discrepancies, they lose their attendance.  
Checking the RSMS website everyday is a hassle and students may forget to do so.  
This project alerts you if you have been marked absent, hence saving your precious attendance!

## How it works 🧠

The python script does webscraping by automating RSMS student's login using credentials provided.  
If an absent has been marked in the attendance table for the specified dates, an email will be sent automatically to the student's college email address to notify them of this.  
Since Monday's attendance will only be locked on Wednesday, the script will have to run only on every Wednesday, Thursday & Friday.  
Github actions has been utilised to schedule the script to run every Wednesday, Thursday and Friday at 6:30pm.

## How to use this 💻

- Fork this repository. Then on the repository page, click on `Settings` -> `Security` -> `Secrets and variables` -> `Actions`.
- Save your credentials as Repository secrets named:
    - `YOUR_UID`
    - `RSMS_PASSWORD`
    - `SEMESTER`(eg: S5)
    - `BRANCH`(eg: CS-A)
    - `GMAIL_ID`
    - `GMAIL_API`.
- The `GMAIL_ID` you provide will be used to send the email automatically. You will have to configure your Gmail SMTP server settings and obtain a `GMAIL_API` by referring this [article](https://mailtrap.io/blog/gmail-smtp/#How-to-configure-Gmail-SMTP-server-settings).
- Enable the workflow `Notifier cronjob` from the repository's Actions tab. You can manually run the workflow by clicking `Run workflow` button to test if you are getting an email.
- Thats it! The service will run automatically according to schedule as explained.

## Known Issues 🤕

- Gmail api may expire or SMTP regulations may change.
- Like all web scraping projects, any design updates to the target webpage may break the automation script. Luckily, RSMS website is not frequently updated.
