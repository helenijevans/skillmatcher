import requests
import random
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from geoIDMap import geoIDs

api_url = ('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location=United'
           '%2BKingdom&geoId={}&trk=public_jobs_jobs-search-bar_search-submit&start={}')

print("* * * * * * * * * * * * * * * * * * * * * * * * * * \n"
      "╔═╗┬┌─┬┬  ┬  ╔╦╗┌─┐┌┬┐┌─┐┬ ┬┌─┐┬─┐\n"
      "╚═╗├┴┐││  │  ║║║├─┤ │ │  ├─┤├┤ ├┬┘\n"
      "╚═╝┴ ┴┴┴─┘┴─┘╩ ╩┴ ┴ ┴ └─┘┴ ┴└─┘┴└─\n"
      "  ┬┌─┐┌┐ ┌─┐  ┌─┐┬ ┬┬┌┬┐┌─┐┌┬┐  ┌┬┐┌─┐  ┬ ┬┌─┐┬ ┬\n"
      "  ││ │├┴┐└─┐  └─┐│ ││ │ ├┤  ││   │ │ │  └┬┘│ ││ │\n"
      " └┘└─┘└─┘└─┘  └─┘└─┘┴ ┴ └─┘─┴┘   ┴ └─┘   ┴ └─┘└─┘\n"
      "* * * * * * * * * * * * * * * * * * * * * * * * * *")
print("ABOUT\nA program that finds UK-based jobs based on your skillset\n")
print("HOW IT WORKS\nScrapes LinkedIn for jobs matching the combination of keywords, a table is returned after "
      "processing and you will have the option to write it to a csv file for quick access.")
print("* * * * * * * * * * * * * * * * * * * * * * * * * *\n")

done = False
skill = ""

print("Where are you looking for jobs? Please enter the respective number option")
print("1. United Kingdom\n2. Reading\n3. Manchester\n4. London\n5. Newcastle\n6. Bristol\n7. Leeds\n")

job_location = int(input())

match job_location:
    case 1:
        job_location = "uk"
    case 2:
        job_location = "reading"
    case 3:
        job_location = "manchester"
    case 4:
        job_location = "london"
    case 5:
        job_location = "newcastle"
    case 6:
        job_location = "bristol"
    case 7:
        job_location = "leeds"
    case _:
        print("Not a valid option")
        print("Proceeding with general UK search")
        job_location = "uk"

print("\nPlease enter all your job-related skills below, to exit - type `done`")

while not done:
    check = input("Skill: ")
    if check.lower() == "done":
        done = True
    else:
        skill += f"+{check}"


print("\nThe job hunt has begun!")
current_page = 0


def load_jobs(page_no):
    page = requests.get(api_url.format(skill, geoIDs[job_location], page_no))

    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find_all("div", class_="base-card")


jobsFound = False
jobs = load_jobs(current_page)

myTable = PrettyTable(["Job", "Company", "Location", "Job Link"])
unique_jobs = set()
while jobs:
    output = random.randint(1, 1000)
    if output < 15:
        print("Looks like there's a lot of job matches to your skillset... please bear with as we collate")
    jobsFound = True
    for job in jobs:
        unique_job_no = len(unique_jobs)
        title_element = job.find("h3", class_="base-search-card__title").text.strip()
        company_element = job.find("a", class_="hidden-nested-link").text.strip()
        location_element = job.find("span", class_="job-search-card__location").text.strip()
        unique_jobs.add("{}{}{}".format(title_element, company_element, location_element))
        if len(unique_jobs) > unique_job_no:
            job_link_element = job.find("a")['href']
            myTable.add_row([title_element, company_element, location_element, job_link_element])
    current_page += 25
    jobs = load_jobs(current_page)

if not jobsFound:
    print("Sorry, no jobs were found for this criteria.\nTIP: Try a UK-wide search or reduce the number of skills in "
          "your search")
else:
    print(myTable)
    writeToFile = input("\nWould you like to export this to a csv file? (y/n): ")
    if writeToFile == "y":
        with open('skill_matched_jobs.csv', 'w', newline='') as f_output:
            f_output.write(myTable.get_csv_string())
    print("\n\n** Done **")
