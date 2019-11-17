import requests
import re
import pandas as pd
from selenium import webdriver
import time
import bs4 as bs
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gsd
import datetime

def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 100)

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    #sheetsAvailable = client.list_spreadsheet_files()
    #print("sheets:")
    #print(sheetsAvailable)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("Jersey Strong Schedules").sheet1

    today = datetime.date.today()
    SundayOffset = (today.weekday() - 6)%7
    lastSunday = today - datetime.timedelta(days=SundayOffset)
    lastSunday = str(lastSunday)

    weekOf = sheet.cell(1,2).value
    print(today)
    print(lastSunday)
    print(weekOf)

    #########################
    ### When running on Windows Task Scheduler...
    ### switch which of these lines is commented
    ###    If running manually: manual = 1 should be uncommented
    ###    If running on a timer: manual = 0 should be uncommented
    # manual = 1
    manual = 0
    if(manual == 1):
        if weekOf == "":
            print("No Schedule Found, updating now")
            sheet.update_cell(1,2,str(lastSunday))
            updateSchedule(sheet)
        elif weekOf != lastSunday:
            print("Schedule outdated, found from: ", weekOf)
            print("Would you like to update?")
            print("1 = Yes, Update")
            print("2 = No, Don't Update")
            choice = int(input())
            if choice == 1:
                sheet.update_cell(1, 2, str(lastSunday))
                updateSchedule(sheet)
            elif choice == 2:
                df = gsd.get_as_dataframe(sheet, parse_dates=True, usecols=[0,1,2,3,4,5], skiprows=1)
                displaySchedule(df)
            else:
                print("Invalid Option, quitting")
                return 0
        else:
            print("Schedule found from this week, printing")
            df = gsd.get_as_dataframe(sheet, parse_dates = True, usecols=[0,1,2,3,4,5], skiprows=1)
            displaySchedule(df)
    else: #manual == 0 (running on automatic task scheduler)
        updateSchedule(sheet)
        #update data on sheet only if schedule gets updated
        sheet.update_cell(1, 2, str(lastSunday))
        return 0
    return 0

def updateSchedule(sheet):

    schedule = pd.DataFrame(columns=['Location', 'Day', 'Time', 'Class', 'Instructor First Name', 'Instructor Last Name'])
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
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

    for i in filteredStrings:  # go to each website and parse out each schedule item
        #print(i[17:])
        scheduleURL = baseURL + i
        #testURL = 'https://www.jerseystrong.com/class-schedules-east-brunswick'
        testResponse = requests.get(scheduleURL).text
        testSoup = bs.BeautifulSoup(testResponse, 'html.parser')
        testiFrames = testSoup.find_all('iframe')
        extractedSRC = testiFrames[0].get('src')
        #print(extractedSRC)

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
        days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'NA']
        day = 0

        for row in tables:
            #print(row)
            if row.text.startswith("\n" + days[day]):
                #print(days[day])
                day = day + 1
            elif (len(row.contents) == 3):
                continue
            else:
                location = scheduleURL[45:]
                #print(location)
                courseTime = row.contents[1].text
                courseAndInstructor = row.contents[5].text.split('with ')
                #print(courseAndInstructor)
                if(len(courseAndInstructor) == 2):
                    course = courseAndInstructor[0]
                    instructor = courseAndInstructor[1].split(' ')
                    instructorFN = instructor[0]
                    instructorLN = instructor[1]
                else:
                    course = courseAndInstructor[0]
                    instructor = "N/A"
                    instructorFN = instructor
                    instructorLN = instructor
                if(course != "Description"):
                    print(location,days[day-1],courseTime,course,instructorFN,instructorLN)
                    schedule = schedule.append(pd.Series([location,days[day-1],courseTime,course,instructorFN,instructorLN],index=schedule.columns), ignore_index=True)
        time.sleep(1)

    cell_list = sheet.range('A3:F2000')
    for cell in cell_list:
        print(cell.col, cell.row)
        cell.value = ""
    sheet.update_cells(cell_list)
    gsd.set_with_dataframe(sheet, schedule, row=2, col=1)
    displaySchedule(schedule)
    return 0


def displaySchedule(schedule):

    print (schedule)

    print()
    print()
    #########################
    ### When running on Windows Task Scheduler...
    ### switch which of these lines is commented
    ###    If running manually: shell = 1 should be uncommented
    ###    If running on a timer: shell = 0 should be uncommented
    #shell = 1
    shell = 0
    while(shell == 1):
        print("Sort schedule by what?")
        print("1 = Location")
        print("2 = Day")
        print("3 = Time")
        print("4 = Class")
        print("5 = Instructor")
        print("Press 0 to Quit")

        choice = int(input())
        if choice == 0:
            shell = 0
        elif choice == 1: #Sort by Location
            schedule = schedule.sort_values(by=['Location'])
            locations = schedule.Location.unique()
            print("Type in a Location!")
            print(locations)
            locationChoice = str(input())
            if (locationChoice in locations):
                print(schedule.loc[schedule['Location'] == locationChoice].sort_index())
            else:
                print("That's not a valid Location")
        elif choice == 2: #Sort by Day
            scheDays = schedule.Day.unique()
            print("Type in a Day!")
            print("['SUN' 'MON' 'TUE' 'WED' 'THU' 'FRI' 'SAT']")
            dayChoice = str(input())
            if (dayChoice in scheDays):
                print(schedule.loc[schedule['Day'] == dayChoice].sort_index())
            else:
                print("That's not a valid Day")
        elif choice == 3: #Sort by Time
            schedule = schedule.sort_values(by=['Time'])
            times = schedule.Time.unique()
            print("Type in a Time!")
            print(times)
            timeChoice = str(input())
            if (timeChoice in times):
                print(schedule.loc[schedule['Time'] == timeChoice].sort_index())
            else:
                print("That's not a valid Time")
        elif choice == 4: #Sort by Class
            schedule = schedule.sort_values(by=['Class'])
            courses = schedule.Class.unique()
            print("Type in a Class!")
            print(courses)
            courseChoice = str(input())
            if (courseChoice in courses):
                print(schedule.loc[schedule['Class'] == courseChoice].sort_index())
            else:
                print("That's not a valid Class")
        elif choice == 5: #Sort by Instructor
            schedule = schedule.sort_values(by=['Instructor First Name'])
            instructors = schedule.Instructor.unique()
            print("Type in a Instructor!")
            print(instructors)
            instructorChoice = str(input())
            if (instructorChoice in instructors):
                print(schedule.loc[schedule['Instructor'] == instructorChoice].sort_index())
            else:
                print("That's not a valid Instructor")
        else:
            "That's not a valid option, try again"
    return 0

#Run the main function
if __name__ == "__main__":
    main()