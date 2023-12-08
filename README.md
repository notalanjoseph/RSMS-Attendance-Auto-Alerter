# RSMS-Attendance-Auto-Alerter

<!--![main workflow](https://img.shields.io/github/actions/workflow/status/notalanjoseph/RSMS-Attendance-Auto-Alerter/actions.yml?logo=github)-->
![documentation](https://img.shields.io/readthedocs/gspread?logo=readthedocs)
![python version](https://img.shields.io/pypi/pyversions/gspread?style=pypi)
 
RSET students are asked to regularly check if they are wrongly marked absent in RSMS website. RSMS attendance gets locked 3 days after each class, so if students fail to realise and report any discrepancies, they lose their attendance.  
Checking the RSMS website everyday is a hassle and students may forget to do so.  
This project alerts you if you have been marked absent, hence saving your precious attendance!

## How it works 🧠

The python script uses selenium to automate RSMS student's login using credentials provided.  
If an absent has been marked in the attendance table for the specified dates, an email will be sent automatically to the student's college email address to notify them of this.  
Since Monday's attendance will only be locked on Wednesday, the script will have to run only on every Wednesday, Thursday & Friday.  
Github actions has been utilised to schedule the script to run every Wednesday, Thursday and Friday at 6:30pm.

## How to use this 💻

- Fork this repository.  
- Edit `noSele.py` to enter your credentials OR even better save your credentials as github secrets named `YOUR_UID`, `RSMS_PASSWORD`, `SEMESTER`(eg: S5) and `BRANCH`(eg: CS-A).
- Enable the workflow `Python script cronjob` from the repository's action tab. You can manually run the workflow by clicking `Run workflow` button to test if it's working.
- Thats it! The service will run automatically according to schedule as explained.

## Known Issues 🤕

- Like all web scraping projects, any design updates to the target webpage may break the automation script. Luckily, RSMS website is not frequently updated.
- During some runs, the virtual machine provided by Github Actions seems to install incompatible versions of chromium and it's webdriver. This happens for a few days after a new version of chromium is released. During these days, the code won't work. After a few days, the updated chromium gets installed, solving the issue. Read more about the problem [here](https://stackoverflow.com/questions/50692358/how-to-work-with-a-specific-version-of-chromedriver-while-chrome-browser-gets-up)
