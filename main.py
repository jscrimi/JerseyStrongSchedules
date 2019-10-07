import requests
import urllib.request
import time
import PyPDF2
from bs4 import BeautifulSoup

def main():
    url = 'https://www.jerseystrong.com/group-fitness-classes-in-nj'
    response = requests.get(url)
    #print(response)

    soup = BeautifulSoup(response.text, "html.parser")

    for i in range(17, 29): #request and download all PDFs
        one_link = soup.findAll('a')[i].get('href')
        print(one_link)
        filename = one_link[51:]
        print(filename)
        downloadURL = 'https://www.jerseystrong.com' + one_link
        print(downloadURL)
        urllib.request.urlretrieve(downloadURL, filename)
        time.sleep(1)

    #for each pdf, open and scan in the first page
    

    return 1

#Run the main function
if __name__ == "__main__":
    main()