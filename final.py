import requests
from bs4 import BeautifulSoup
import time
import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# URL of your college's GPA page
GPA_URL = "https://slcm.manipal.edu/GradeSheet.aspx"  # Replace with actual URL
LOGIN_URL = "https://slcm.manipal.edu/"  # Replace with actual login URL

# Manually extracted cookies
cookies = {
    'ASP.NET_SessionId': 'zyq0acifwxgmu2hna2541ztv',  # Replace with your actual session ID
}

# Store the last GPA
PREVIOUS_GPA = ""
def check_gpa_update():
    global PREVIOUS_GPA
    try:
        # Create a session object
        session = requests.Session()

        # Set the cookies for the session
        session.cookies.update(cookies)

        # Fetch the website content
        response = session.get(GPA_URL)
        response.raise_for_status()  # Raise error for bad HTTP status codes

        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the GPA - using the provided element
        gpa_element = soup.find('span', id='ContentPlaceHolder1_lblGPA')  # Updated to match your provided element
        if gpa_element:
            current_gpa = gpa_element.get_text(strip=True)
            print(f"GPA Found: {current_gpa}")
                       # Compare with previous GPA
            if PREVIOUS_GPA != current_gpa:
                print("🎉 GPA has been updated!")
                PREVIOUS_GPA = current_gpa
                # You can add email/notification code here
            else:
                print("No updates yet.")
        else:
            print("GPA element not found. Check the selector.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")

# Schedule the script to run every 5 minutes
schedule.every(1).minutes.do(check_gpa_update)

print("🚀 GPA Update Checker Started!")
while True:
    schedule.run_pending()
    time.sleep(1)

