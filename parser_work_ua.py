import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup

html_page = requests.get('https://www.work.ua/jobs-it/')

soup = BeautifulSoup(html_page.text, 'html.parser')

all_jobs_description = soup.find_all("div", {"class": "card card-hover card-visited wordwrap job-link js-hot-block"})
string = '{}'
table = json.loads(string)
for i, job_description in enumerate(all_jobs_description):
    title_date = job_description.find_all("a")[0]['title']
    title, date = '', ''
    try:
        title, date = title_date.split(",")
    except:
        print('no 1 parameter')

    city_tag = job_description.find(class_="add-top-xs")

    cities = ["Львів", "Київ", "Дніпро", "Одеса", "Харків", "Львов", "Киев", "Днепр", "Одесса", "Харьков"]
    city = ''
    for city_on_site in cities:
        if str(city_tag).find(city_on_site):
            city = city_on_site
            break

    company = job_description.find_all("img")[0]["alt"]
    url = job_description.a['href']
    url = "https://www.work.ua" + url
    table[i + 1] = dict()
    table[i + 1]["title"] = title
    table[i + 1]["company"] = company
    table[i + 1]["date"] = date
    table[i + 1]["url"] = url
    # if i == 4:
    #     #     break

pprint(table)