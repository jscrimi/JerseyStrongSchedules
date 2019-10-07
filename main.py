import requests
import urllib.request
import time
from bs4 import BeautifulSoup

def main():
    url = 'https://www.jerseystrong.com/group-fitness-classes-in-nj'
    response = requests.get(url)
    #print(response)

    soup = BeautifulSoup(response.text, "html.parser")

    for i in range(17, 29):
        one_link = soup.findAll('a')[i].get('href')
        print(one_link)
        downloadURL = 'https://www.jerseystrong.com' + one_link
        urllib.request.urlretrieve(downloadURL)

        time.sleep(1)
    #for link in soup.find_all('a'):
    #    print(link.get('href'))

    return 1

#Run the main function
if __name__ == "__main__":
    main()