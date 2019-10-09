import sys
import requests
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import bs4 as bs
import os

def main():
    schedule = pd.DataFrame(columns=['Location', 'Day', 'Time', 'Class', 'Instructor'])
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 100)
    url = 'https://www.jerseystrong.com/group-fitness-classes-in-nj'
    baseURL = 'https://www.jerseystrong.com'

    response = requests.get(url)
    #print(response)

    soup = bs.BeautifulSoup(response.text, "html.parser")
    switchScriptString = soup.find_all("script")[17]
    #print(switchScriptString) #The 17th script on this page contains the links to the location schedules

    #split that string into a list by window.location= and ;
    splitString = re.split('window.location="|;', switchScriptString.string)
    #print(splitString)
    filteredStrings = [i for i in splitString if i.startswith('/class-schedules')]
    filteredStrings = ([s.replace('"', '') for s in filteredStrings])


    #TEST
    testURL = 'https://www.jerseystrong.com/class-schedules-east-brunswick'
    testResponse = requests.get(testURL).text
    testSoup = bs.BeautifulSoup(testResponse, 'html.parser')
    testiFrames = testSoup.find_all('iframe')
    extractedSRC = testiFrames[0].get('src')
    print(extractedSRC)

    #Render Dynamic WebPage and grab HTML from that
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.get(extractedSRC)

    python_button = driver.find_element_by_id("content")
    python_button.click()

    #After opening the url, hand the source to Beautiful Soup
    dynamicSoup = bs.BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()
    tables = dynamicSoup.find_all('tr')
    days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', ' ']
    day = 0

    for row in tables:
        #print(row)
        if row.text.startswith("\n" + days[day]):
            #print(days[day])
            day = day + 1
        elif (len(row.contents) == 3):
            continue
        else:
            location = testURL[45:]
            time = row.contents[1].text
            courseAndInstructor = row.contents[5].text.split('with ')
            #print(courseAndInstructor)
            if(len(courseAndInstructor) == 2):
                course = courseAndInstructor[0]
                instructor = courseAndInstructor[1]
            else:
                course = courseAndInstructor[0]
                instructor = "N/A"

            schedule = schedule.append(pd.Series([location,days[day-1],time,course,instructor],index=schedule.columns), ignore_index=True)
    print (schedule)

    # for i in filteredStrings: #go to each website and parse out each schedule item
    #     print(i[17:])
    #     scheduleURL = baseURL + i
    #     scheduleResponse = requests.get(scheduleURL)
    #     #print(scheduleResponse)
    #     #soup =        BeautifulSoup(response.text,         "html.parser")
    #     #print(scheduleResponse.text)
    #     scheduleSoup = BeautifulSoup(scheduleResponse.text, "html.parser")
    #     #print(scheduleSoup)
    #     tables = scheduleSoup.find_all('div')
    #     print(tables)
    #
    #     time.sleep(1)

    return 0

#Run the main function
if __name__ == "__main__":
    main()