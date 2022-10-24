# All necessary library
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Preparing chrome driver 
s=Service('./chromerdriver.exe')
url="https://www.momjunction.com/baby-names/malay/page/3/"
driver=webdriver.Chrome()
driver.get(url)

# To let the page load the data first
time.sleep(5)

# Declaring empty list for the next use to store data
list_name=[]
final_name_list=[]

# Finding the location of name in the data
find_name=driver.find_element(By.TAG_NAME,
    'tbody').find_elements(By.TAG_NAME,'tr')

# For future use to calculate error/ads that get in a way
number_of_error=0

# Extract name
for name_location in find_name:
    
    try:
        # Appending the list name from Momjunction
        person_name=name_location.find_elements(By.TAG_NAME,
            'td')[0].find_element(By.TAG_NAME,'a').text
        list_name.append(person_name)
    
    except:
        # If ads/error get in the way
        number_of_error+=1

# To close the current window
driver.close()

# Error/ads that get in the way
print("Total number of ads: " + str(number_of_error) )

# To know where are these country, gender and age for this certain name using API
for name_default in list_name:
    k="https://api.nationalize.io/?name="+name_default
    p="https://api.genderize.io/?name="+name_default
    l="https://api.agify.io/?name="+name_default
    r = requests.get(k)
    h = requests.get(p)
    j = requests.get(l)

    # Country
    try:
        country=r.json()['country'][0]['country_id']
    except:
        country="unknown"

    # Gender
    gender=h.json()['gender']
    if gender==None:
        gender="unknown"

    # Age
    age=j.json()['age']
    if age==None:
        age="unknown"

    # Putting the information into dictionary
    information_details={
        "name_default": name_default,
        "country":country,
        "gender":gender,
        "age":age
    }            

    # Put the dictionary into the list
    final_name_list.append(information_details)
    print("Name Added :", str(len(final_name_list)) + " : " + information_details['name_default']) 
    
#Save data into CSV
df = pd.DataFrame(final_name_list)
df.to_csv('gender_nationality_age_identifier.csv',
            index=False, encoding='utf-8')