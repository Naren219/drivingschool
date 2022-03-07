import requests
from bs4 import BeautifulSoup
import difflib
import smtplib
import ssl
import schedule
import time

selected_school = ""
oldschool = []
newschool = []
found = False

# Writing file
response = requests.get('https://jordandriving.com/driver-education-fee-class-schedules-fee/')
soup = BeautifulSoup(response.content, 'html.parser')
request = soup.find("div", class_="entry-content")
systems = request.findAll("a", class_="a1")

def main():
  writefile()
  schedule.every().day.at("7:00").do(readpage)
  time.sleep(45)
  # Choose when you want the program to be run.
  # schedule.every(10).minutes.do(readpage)
  # schedule.every().hour.do(readpage)
  # schedule.every().day.at("10:30").do(readpage)
  # schedule.every().monday.do(readpage)
  # schedule.every().wednesday.at("13:15").do(readpage)
  # schedule.every().minute.at(":17").do(readpage)

  while not found:
      schedule.run_pending()
      time.sleep(1)

def writefile():
  print("Writing File...")
  for schools in systems:
    oldschool.append(schools.text.strip())
    # Starts to read subpage
    schools_response = requests.get(schools["href"])
    schools_soup = BeautifulSoup(schools_response.content, 'html.parser')
    schools_list = schools_soup.find("div", class_="entry-content")
    for school in schools_list.findAll('a'):
      if "high" or "academy" in school.text.lower():
        oldschool.append(school.text.strip())

def readpage():
  print("Reading Page...")
  for schools in systems:
    newschool.append(schools.text.strip())
    # Starts to read subpage
    schools_response = requests.get(schools["href"])
    schools_soup = BeautifulSoup(schools_response.content, 'html.parser')
    schools_list = schools_soup.find("div", class_="entry-content")
    for school in schools_list.findAll('a'):
      if "high" or "academy" in school.text.lower():
        newschool.append(school.text.strip())

  for i in list(set(newschool) - set(oldschool)):
    if i == selected_school:
      found = True
      sendmail()

def sendmail():
  with open('new_school.txt') as new_school:
    for school in newschool:
        if "class" in school.lower():
          new_school.write(f"{school}\n\n")
        else:
          new_school.write(f"{school}\n")

    emailid = ""
    password = ""
    data = new_school.read()
    message = 'Subject: {}\n\n{}'.format("It\'s time for you to drive!", f"{selected_school} has an open slot for Jordan Driving school! Look at the list below. Your school name will have a space under it.\n{data}")
    context = ssl.create_default_context()
    print("Starting to send")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(emailid, password)
      server.sendmail("donotreply@gmail.com", emailid, message)
    print("Sent email")
    new_school.truncate(0)

if __name__ == "__main__":
    main()

