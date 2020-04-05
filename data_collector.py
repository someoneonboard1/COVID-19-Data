import requests
import bs4
from tqdm import tqdm
import pprint

# Website used is https://virusncov.com and https://floridahealthcovid19.gov

def collection_global():  # Collects global data
    data = {}
    selectors = ["body > div.container > div > div:nth-child(1) > div.col-40 > div > div.first-count > h2 > span",
                 "body > div.container > div > div:nth-child(1) > div.col-40 > div > div.second-count.mt-large > h2:nth-child(1) > span",
                 "body > div.container > div > div:nth-child(1) > div.col-40 > div > div.second-count.mt-large > h2:nth-child(2) > span",
                 "body > div.container > div > div:nth-child(1) > div.col-40 > div > div.first-count > h3 > strong"] #The CSS selectors that are being used
    var = ["cases", "deaths", "recovered", "serious"]

    res = requests.get("https://virusncov.com").text
    html = bs4.BeautifulSoup(res, "html.parser")
    for i in tqdm(range(len(selectors))):
        collected = html.select(selectors[i]) #collect the selector
        to_store = collected[0].text #the first item in that list is the text we need
        data[var[i]] = to_store.replace(',', "") #scrapped data usually includes a ',' between the numbers which doesnt allow for str() or int() to work, this removes that

    data["closed_case"] = str((int(data.get("recovered"))) + (int(data.get("deaths")))) #Sometimes the css selectors for there data points dont seem to work so we just caluclate them out with the data that we do have
    data["active_infected"] = str((int(data.get("cases"))) - (int(data.get("closed_case"))))
    data["mild"] = str((int(data.get("active_infected"))) - (int(data.get("serious"))))

    # pp = pprint.PrettyPrinter()
    # pp.pprint(data)
    return data


def collection_us():  # Collects data from the United States
    data = {}
    selectors = ["body > div.container > div > div:nth-child(5) > div > div.row > div:nth-child(1) > h2 > strong:nth-child(1)",
                 "body > div.container > div > div:nth-child(5) > div > div.row > div:nth-child(1) > h2 > strong.red-text",
                 "body > div.container > div > div:nth-child(5) > div > div.row > div:nth-child(1) > h2 > strong.green-text",
                 "body > div.container > div > div:nth-child(5) > div > div.row > div:nth-child(1) > h2 > small:nth-child(3) > strong"]
    var = ["cases", "deaths", "recovered", "serious"]

    res = requests.get("https://virusncov.com/covid-statistics/usa").text
    html = bs4.BeautifulSoup(res, "html.parser")
    for i in tqdm(range(len(selectors))):
        collected = html.select(selectors[i])
        to_store = collected[0].text
        data[var[i]] = to_store.replace(',', "")

    data["closed_case"] = str((int(data.get("recovered"))) + (int(data.get("deaths"))))
    data["active_infected"] = str((int(data.get("cases"))) - (int(data.get("closed_case"))))
    data["mild"] = str((int(data.get("active_infected"))) - (int(data.get("serious"))))

    # pp = pprint.PrettyPrinter()
    # pp.pprint(data)
    return data


def collection_local():  # Collects data from the state of Florida
    data = {}
    selectors = [
        "#latest-stats > div.situation__boxes-wrapper > div.col-xs-12.col-md-8.outer--box.outer--box--left > div > div:nth-child(2) > h2",
        "#latest-stats > div.situation__boxes-wrapper > div.col-xs-12.col-md-8.outer--box.outer--box--left > div > div:nth-child(3) > h2",
        "#latest-stats > div.situation__boxes-wrapper > div.col-xs-12.col-md-8.outer--box.outer--box--left > div > div:nth-child(4) > h2"]
    var = ["cases_residents", "cases_non", "total"]

    res = requests.get("https://floridahealthcovid19.gov").text
    html = bs4.BeautifulSoup(res, "html.parser")
    for i in tqdm(range(len(selectors))):
        collected = html.select(selectors[i])
        to_store = collected[0].text
        data[var[i]] = to_store.replace(',', "")

    # pp = pprint.PrettyPrinter()
    # pp.pprint(data)
    return data


#The functions created above are imported to the other files in this project folder.
#They create the dictionary that will be saved to the data set which can be found in the Excel file, "collected_data"
#All functions work the same way (commented in the first function) but they just collect different data sets