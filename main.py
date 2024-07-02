import requests
import random
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import time

api_url = ('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location=United'
           '%2BKingdom&geoId=101165590&trk=public_jobs_jobs-search-bar_search-submit&start={}')

print("* * * * * * * * * * * * * * * * * * * * * * * * * * \n"
      "╔═╗┬┌─┬┬  ┬  ╔╦╗┌─┐┌┬┐┌─┐┬ ┬┌─┐┬─┐\n"
      "╚═╗├┴┐││  │  ║║║├─┤ │ │  ├─┤├┤ ├┬┘\n"
      "╚═╝┴ ┴┴┴─┘┴─┘╩ ╩┴ ┴ ┴ └─┘┴ ┴└─┘┴└─\n"
      "  ┬┌─┐┌┐ ┌─┐  ┌─┐┬ ┬┬┌┬┐┌─┐┌┬┐  ┌┬┐┌─┐  ┬ ┬┌─┐┬ ┬\n"
      "  ││ │├┴┐└─┐  └─┐│ ││ │ ├┤  ││   │ │ │  └┬┘│ ││ │\n"
      " └┘└─┘└─┘└─┘  └─┘└─┘┴ ┴ └─┘─┴┘   ┴ └─┘   ┴ └─┘└─┘\n"
      "* * * * * * * * * * * * * * * * * * * * * * * * * *")

skill = input("Please enter a skill you have: ")
print("\nThank you. You can take this time to grab a drink and relax - the job search has begun")
current_page = 0


def load_jobs(page_no):
    page = requests.get(api_url.format(skill, page_no))

    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find_all("div", class_="base-card")


jobsFound = False
jobs = load_jobs(current_page)

myTable = PrettyTable(["Job", "Company", "Location", "Job Link"])
unique_jobs = set()
while jobs:
    output = random.randint(1, 1000)
    if output < 15:
        print("Things are happening... please bear with")
    jobsFound = True
    for job in jobs:
        unique_job_no = len(unique_jobs)
        title_element = job.find("h3", class_="base-search-card__title").text.strip()
        company_element = job.find("a", class_="hidden-nested-link").text.strip()
        location_element = job.find("span", class_="job-search-card__location").text.strip()
        unique_jobs.add("{}{}{}".format(title_element,company_element, location_element))
        if len(unique_jobs) > unique_job_no:
            job_link_element = job.find("a")['href']
            myTable.add_row([title_element, company_element, location_element, job_link_element])
    jobs = load_jobs(current_page + 25)

if not jobsFound:
    print("Sorry, no jobs were found for this criteria.")
else:
    print(myTable)
    print("\n\n** Done **")
