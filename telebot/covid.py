from bs4 import BeautifulSoup
import requests
# country="italy"

def total_cases(msg):
    country= msg.strip()
    URL = 'https://www.worldometers.info/coronavirus/'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, features="html.parser")

    table = soup.table
    table_rows = table.find_all('tr')

    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        try:
            if (row[0].lower().rstrip(":") == country.lower()):
                return ("Total cases in {} are {} and total deaths are {}.".format(country.upper(), row[1], row[3] ))

        except IndexError:
            pass
    error="Sorry, the country you entered seems to be absent from our data source.\n\nPlease try again, ensure you have no typos! \n\nIf the problem persists, please raise a support request via bit.ly/coronabotsupport"
    return (error)

def all_info(msg):
    country = msg[1:].strip()
    URL = 'https://www.worldometers.info/coronavirus/'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, features="html.parser")

    table = soup.table
    table_rows = table.find_all('tr')

    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        try:
            if (row[0].lower().rstrip(":") == country.lower()):
                info=" \t {}: \nTotal cases: {} \nTotal deaths: {} \nTotal recovered: {} \nActive cases: {} \nCritical cases: {} \nTotal cases per 1 million population: {}".format(country.upper(), row[1], row[3],row[5],row[6],row[7],row[8])
                return (info)

        except IndexError:
            pass
    error="Sorry, the country you entered seems to be absent from our data source.\n\nPlease try again, ensure you have no typos! \n\nIf the problem persists, please raise a support request via bit.ly/coronabotsupport"
    return (error)
