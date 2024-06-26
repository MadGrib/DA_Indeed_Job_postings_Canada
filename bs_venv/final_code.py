##Please install all libraries separately BEFORE running code below

#Step 1
import requests

#Step 2
from bs4 import BeautifulSoup

#Step 3
import bs4

#Step 4
import pandas as pd

#Step 5 Run code below

def extract(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    url = f'https://ca.indeed.com/jobs?q=data+analyst&start={page}&vjk=b7c58b9a5fc8f161'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    job_listings = soup.find_all('div', class_='company_location')  # Find all divs containing company information
    job_titles = soup.find_all('a', class_='jcs-JobTitle')  # Find all job titles

    job_data = []

    for job_info, job_title in zip(job_listings, job_titles):
        # Extract and print job title
        job_title_span = job_title.find('span', id=lambda x: x and x.startswith('jobTitle'))
        job_title_text = job_title_span.text.strip() if job_title_span else "Not available"

        # Extract and print company name
        company_name = job_info.find('span', class_='css-92r8pb')  # Find the span with company name
        company_text = company_name.text.strip() if company_name else "Not available"

        # Extract and print location
        location = job_info.find('div', class_='css-1p0sjhy')  # Find the div with location
        location_text = location.text.strip() if location else "Not available"

        # Create dictionary for job data
        job = {
            'job_title': job_title_text,
            'company': company_text,
            'location': location_text
        }

        # Append job data to list
        job_data.append(job)

    return job_data

# Create an empty list to store all job data
all_job_data = []

# Iterate through the first 10 pages
for i in range(0, 70 * 15, 15):  # Scrape 10 pages, each page has 10 listings
    # Extract data from the current page
    soup = extract(i)
    # Transform the data and append it to the list
    page_job_data = transform(soup)
    all_job_data.extend(page_job_data)

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(all_job_data)

# Save the DataFrame to a CSV file
df.to_csv('job_listings.csv', index=False)

print("CSV file saved successfully!")