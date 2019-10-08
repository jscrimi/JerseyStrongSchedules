import requests
import re
import pandas
import urllib.request
import time
import PyPDF2
from bs4 import BeautifulSoup

def main():
    url = 'https://www.jerseystrong.com/group-fitness-classes-in-nj'
    response = requests.get(url)
    #print(response)

    soup = BeautifulSoup(response.text, "html.parser")
    switchScriptString = soup.find_all("script")[17]
    #print(switchScriptString) #The 17th script on this page contains the links to the location schedules

    #split that string into a list by window.location= and ;
    splitString = re.split('window.location="|;', switchScriptString.string)
    #print(splitString)
    filteredStrings = [i for i in splitString if i.startswith('/class-schedules')]
    filteredStrings = ([s.replace('"', '') for s in filteredStrings])
    for i in filteredStrings:
        print(i)


    #for i in range(17, 29): #request and download all PDFs
    #    one_link = soup.findAll('a')[i].get('href')
    #    print(one_link)
    #    filename = one_link[51:]
    #    print(filename)
    #    downloadURL = 'https://www.jerseystrong.com' + one_link
    #    print(downloadURL)
    #    urllib.request.urlretrieve(downloadURL, filename)
        #readFirstPage(filename)
    #    time.sleep(1)
    return 0

#def readFirstPage(filename):
#    pdfFileObj = open(filename, 'rb')
#    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#    pageObj = pdfReader.getPage(0)
#    print(pageObj.extractText())
#    return 1

#Run the main function
if __name__ == "__main__":
    main()