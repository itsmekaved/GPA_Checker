import requests
from bs4 import BeautifulSoup
import time
import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


GPA_URL = "https://slcm.manipal.edu/GradeSheet.aspx"  
LOGIN_URL = "https://slcm.manipal.edu/" 
cookies = {
    'ASP.NET_SessionId': 'session id',  
}
PREVIOUS_GPA = ""
def check_gpa_update():
    global PREVIOUS_GPA
    try:
        session = requests.Session()
        session.cookies.update(cookies)
        response = session.get(GPA_URL)
        response.raise_for_status()  

 
        soup = BeautifulSoup(response.content, 'html.parser')
     
        gpa_element = soup.find('span', id='ContentPlaceHolder1_lblGPA')  
        if gpa_element:
            current_gpa = gpa_element.get_text(strip=True)
            print(f"GPA Found: {current_gpa}")
            if PREVIOUS_GPA != current_gpa:
                print("🎉 GPA has been updated!")
                PREVIOUS_GPA = current_gpa
            else:
                print("No updates yet.")
        else:
            print("GPA element not found. Check the selector.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")

schedule.every(1).minutes.do(check_gpa_update)

print("🚀 GPA Update Checker Started!")
while True:
    schedule.run_pending()
    time.sleep(1)

