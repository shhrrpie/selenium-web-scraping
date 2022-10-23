# All necessary library
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Preparing chrome driver 
s = Service("./chromedriver.exe")
url = "https://www.acronis.com/en-us/careers/#positions"
driver = webdriver.Chrome(service=s)
driver.get(url)

# To let the page load the data first
time.sleep(10)

# Locating the drop down option. 
dropdownoption = driver.find_element(By.CLASS_NAME,
    'selector').find_element(By.CLASS_NAME,
    'countries')

# Open the drop down option
opendropdown = dropdownoption.click()

# To let the page load the data first
time.sleep(5)

# Find & select Singapore
findsingapore = dropdownoption.find_element(By.XPATH,
    '//*[@data-value="Singapore"]')
selectsingapore = findsingapore.click() 

# Locate where data is
job_table = driver.find_element(By.CLASS_NAME,
    'vacancies').find_elements(By.TAG_NAME,
    'div')

try:

    job_added_list = []

    # Looping for job
    for i in job_table:

        # To give some space between jobs.
        print(" ")

        # Job Position
        try:
            jobposition = i.find_element(By.TAG_NAME,
                'a').text
            print("Title:", jobposition)
        except:
            break

        # Company
        company = "Acronis"
        print("Company: ", company)
        
        # Country
        country_name = i.find_element(By.TAG_NAME,
            'strong').text
        print('Country:', country_name)

        # Scrap_date
        s_date = datetime.datetime.now()
        print("Scrap date:", s_date)

        # Job Link
        joblink = i.find_element(By.TAG_NAME,
            'a').get_attribute('href')
        print("Joblink:", joblink)

        # Putting the job info into dictionary
        Job_details = {
            "title": jobposition,
            "categories": None,
            "location": country_name,
            "company": company,
            "scrap_datetime": s_date,
            "link": joblink
        }

        # Put the dictionary into the list
        job_added_list.append(Job_details)
        print("Job Added No.:", len(job_added_list))
    
    #Save data into CSV
    df = pd.DataFrame(job_added_list)
    df.to_csv('Acronis.csv',
              index=False, encoding='utf-8')

finally:
    driver.quit()
