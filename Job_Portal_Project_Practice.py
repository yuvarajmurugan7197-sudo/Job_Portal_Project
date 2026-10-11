import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.python.org/jobs/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")

job_container = soup.find("ol", class_="list-recent-jobs")
print(job_container)

if not job_container:
    print("Job container not found")
    raise SystemExit(1)

jobs = job_container.find_all("li")

job_info = []
for job in jobs:
    job_info.append(" ".join(job.prettify().split()))

job_df = pd.DataFrame(job_info, columns=["Info"])
job_df["Info"] = job_df["Info"].replace("", None)
job_df = job_df.dropna(axis=0, subset=["Info"])

raw_file_name = r"D:\downloads\Data Engineer\jobs_info_raw.csv"
job_df.to_csv(raw_file_name, index=False)
print("Raw data stored successfully")

job_info = job_df["Info"].to_dict().values()

job_titles = []
companies = []
posted_dates = []
locations = []

for element in job_info:
    job_soup = BeautifulSoup(str(element), "html.parser")

    title_tag = job_soup.find("a")
    if title_tag:
        job_titles.append(title_tag.get_text(strip=True))
    else:
        job_titles.append("-")

    company_tag = job_soup.find("span", class_="listing-company-name")
    if company_tag:
        company_lines = company_tag.get_text("\n", strip=True).split("\n")
        cleaned = [
            item.strip()
            for item in company_lines
            if item.strip() and item.strip() != "New"
        ]
        companies.append(cleaned[-1] if cleaned else "-")
    else:
        companies.append("-")

    posted_tag = job_soup.find("time")
    if posted_tag:
        posted_dates.append(posted_tag.get_text(strip=True))
    else:
        posted_dates.append("_")

    location_tag = job_soup.find("span", class_="listing-location")
    if location_tag:
        locations.append(location_tag.get_text(strip=True))
    else:
        locations.append("-")

job_df = pd.DataFrame({
    "Job Title": job_titles,
    "Company": companies,
    "Posted Date": posted_dates,
    "Location": locations,
})

jobs_file_name = r"D:\downloads\Data Engineer\jobs.csv"
job_df.to_csv(jobs_file_name, index=False)

print(job_df)
print("job_df_Data_Stored_Successfully")