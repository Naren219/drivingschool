import requests
from bs4 import BeautifulSoup
import difflib
import smtplib
import ssl
import schedule
import time


selected_school = "Research Triangle High School"
oldschool = []
newschool = []
found = False

# Writing file boilerplate
response = requests.get('https://jordandriving.com/driver-education-fee-class-schedules-fee/')
soup = BeautifulSoup(response.content, 'html.parser')
request = soup.find("div", class_="entry-content")
systems = request.findAll("a", class_="a1")

def main():
  writefile()
  schedule.every().day.at("7:00").do(readpage)

  # Choose when you want the program to be run each day. You can replace the .day with .what every day you want. This uses military time.
  # schedule.every().day.at("7:00").do(readpage)
  while not found:
      schedule.run_pending()
      time.sleep(1)

def writefile():
  print("writefile")
  with open("old_school.txt", "w") as schools_file:
    for schools in systems:
      schools_file.write(f"{schools.text}\n\n")
      # Starts to read subpage
      schools_response = requests.get(schools["href"])
      schools_soup = BeautifulSoup(schools_response.content, 'html.parser')
      schools_list = schools_soup.find("div", class_="entry-content")
      for school in schools_list.findAll('a'):
        if "high" in school.text.lower() or "academy" in school.text.lower():
          schools_file.write(f"{school.text}\n")

def readpage():
  print("readpage")
  for schools in systems:
    newschool.append(schools.text.strip())
    # Starts to read subpage
    schools_response = requests.get(schools["href"])
    schools_soup = BeautifulSoup(schools_response.content, 'html.parser')
    schools_list = schools_soup.find("div", class_="entry-content")
    for school in schools_list.findAll('a'):
      if "high" in school.text.lower() or "academy" in school.text.lower():
        newschool.append(school.text.strip())
  with open('old_school.txt') as f1:
    for item in f1:
      oldschool.append(item.strip())
  print("diff")
  for i in list(set(newschool) - set(oldschool)):
    if i == selected_school:
      found = True
      for school in newschool:
        if "class" in school.lower():
          new_school.write(f"{school}\n\n")
        else:
          new_school.write(f"{school}\n")
      sendmail()

def sendmail():
  emailid = "nmanikandan219@gmail.com"
  password = "naren2007"
  with open("new_school.txt", "r") as f:
    data = f.read()
  message = 'Subject: {}\n\n{}'.format("It\'s time for you to drive!", f"{selected_school} has an open slot for Jordan Driving school! Look at the list below. Your school name will have a space under it.\n{data}")
  context = ssl.create_default_context()
  print("Starting to send")
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(emailid, password)
    server.sendmail("donotreply@gmail.com", emailid, message)
  print("Sent email")
  #file = open("schools.txt","r+")
  #file.truncate(0)
  #file.close()

if __name__ == "__main__":
    main()

