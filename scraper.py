import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("secretkey.json", scopes) #access the json key you downloaded earlier 
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open("Development Jobs") #open sheet
sheet = sheet.sheet1

sheet.update_acell('C2', 'Blue')

URL="https://www.linkedin.com/jobs/search?keywords=junior%2Bdeveloper&location=London%2C%2BEngland%2C%2BUnited%2BKingdom&geoId=102257491&trk=public_jobs_jobs-search-bar_search-submit&currentJobId=3809466569&position=1&pageNum=0"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("div", class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")

index = 2
for result in results:
    job_title = result.find("h3", class_="base-search-card__title").text
    job_company = result.find("h4", class_="base-search-card__subtitle").text
    job_link = result.find("a", class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]").get("href")
    sheet.update_acell('A' + str(index), job_title)
    sheet.update_acell('B' + str(index), job_company)
    sheet.update_acell('C' + str(index), job_link)
    index = index + 1


