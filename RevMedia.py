# All necessary library
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


# Preparing chrome driver 
s = Service("./chromedriver.exe")
url = "https://revmedia.my/career/"
driver = webdriver.Chrome(service=s)
driver.get(url)

# To let the page load the data first
time.sleep(3)


# Scroll down until the end of the page to load data
reached_page_end = False
last_height = driver.execute_script("return document.body.scrollHeight")

while not reached_page_end:
      driver.find_element(By.XPATH,'//body').send_keys(Keys.END)   
      time.sleep(2)
      new_height = driver.execute_script("return document.body.scrollHeight")
      if last_height == new_height:
            reached_page_end = True
      else:
            last_height = new_height



# Locate where data is
job_table = driver.find_elements(By.CLASS_NAME,
    'post.fusion-column.column.col.col-lg-6.col-md-6.col-sm-6')

try:

    job_added_list = []

    # Looping for job
    for i in job_table:

        # To give some space between jobs.
        print(" ")

        # Job Position
        jobposition = i.find_elements(By.TAG_NAME,
            'a')[1].text
        print("Title:", jobposition)

        # Job description
        header_job_description = i.find_elements(By.TAG_NAME,
            'p')[1].text

        # Job Link
        joblink = i.find_elements(By.TAG_NAME,
            'a')[1].get_attribute('href')
        print("Joblink:", joblink)

        # Job poster
        jobposter = i.find_elements(By.TAG_NAME,
            'a')[0].get_attribute('textContent')
        print("Job poster: ", jobposter)

        # Job poster link profile
        jobposterlinkprofile = i.find_elements(By.TAG_NAME,
            'a')[0].get_attribute('href')
        print("Job poster link: ", jobposterlinkprofile)

        # Company
        company = "RevMedia"    

        # Job posting date
        postdate = i.find_element(By.CLASS_NAME,
            'updated').get_attribute('textContent')
        print("Post Date: ", postdate)

        # Scrap_date
        s_date = datetime.datetime.now()
        print("Scrap date:", s_date)



        # Putting the job info into dictionary
        Job_details = {
            "title": jobposition,
            "header job description":header_job_description,
            "job poster": jobposter,
            "job posteer link profile": jobposterlinkprofile,
            "company":company,
            "postdate":postdate,
            "scrap_datetime": s_date,
            "link": joblink
        }

        # Put the dictionary into the list
        job_added_list.append(Job_details)
        print("Job Added No.:", len(job_added_list))
    
    #Save data into CSV
    df = pd.DataFrame(job_added_list)
    df.to_csv('RevMedia.csv',
              index=False, encoding='utf-8')

finally:
    driver.quit()
