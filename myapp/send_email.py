import smtplib 
import os
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_folder = os.path.expanduser(BASE_DIR) 
load_dotenv(os.path.join(project_folder, '.env'))

def sendEmail(email,subject,content):
    try: 
        smtp = smtplib.SMTP(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT")) 
        smtp.starttls() 
        from_email=os.getenv("SMTP_FROM_EMAIL")
        smtp.login(from_email,os.getenv("SMTP_FROM_EMAIL_PASSWORD"))
        message = 'Subject: %s\n\n%s'%(subject, content)

        smtp.sendmail(from_email, email,message) 
        smtp.quit() 
        return True
    except Exception as ex: 
        return False
