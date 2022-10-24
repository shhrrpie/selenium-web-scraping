# All necessary library
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


# Preparing chrome driver 
s = Service("./chromedriver.exe")
url = "https://career.sea.com/search?keyword=&level=0&location_id=0&team_id=0"
driver = webdriver.Chrome(service=s)
driver.get(url)

# To let the page load the data first
time.sleep(10)

# To find total page
totalfinder = driver.find_element(By.CLASS_NAME,"search-output-footer-text-left").text.split()
totalpage=round(int(totalfinder[0])/10)

job_added_list = []
try:

    # Looping for page
    for currentpage in range(totalpage):  
        
        # Locate where data is
        job_table = driver.find_element(By.CLASS_NAME,
            "search-output-table").find_elements(By.CLASS_NAME,
            'row.search-output-table-row.click-able-row.layout-10')  # Looping for job

        # Looping for job
        for i in job_table:  
            
            # To give some space between jobs.
            print(" ")

            # Job Position
            jobposition = i.find_element(By.TAG_NAME,
                'div').text
            print("Title: ", jobposition)

            # Job Description
            jobdesc1 = i.find_elements(By.TAG_NAME,
                'div')
            jobdesc = jobdesc1[4].text
            print("Desc: ", jobdesc)

            # Company
            company = "Sea"
            print("Company: ", company)

            # Country
            country_name = 'Singapore'
            print("Country: ")

            # Scrap_date
            s_date = datetime.datetime.now()
            print("Scrap date: ", s_date)

            # Putting the job info into dictionary
            Job_details = {
                "title": jobposition,
                "category": jobdesc,
                "country": country_name,
                "company": company,
                "scrap_datetime": s_date,
                "link":url
            }

            # Put the dictionary into the list
            job_added_list.append(Job_details)
            print("Job Added No.:", len(job_added_list))
        
        # Last page doesn't contain Next button, so need to stop the Next loop
        if currentpage != totalpage-1:

            # Press next button  
            clicknextbutton = driver.find_element(By.XPATH,
                "//li[@class='page-item'][last()]").find_element(By.CLASS_NAME,'page-link')  # Location of "Next" button
            clicknextbutton.click()
            time.sleep(2)

        else:
        
            #Break if arrive at the last page.
            break

finally:
    
    #Save data into CSV
    df = pd.DataFrame(job_added_list)
    df.to_csv('Sea.csv',
              index=False, encoding='utf-8')

    driver.quit()
