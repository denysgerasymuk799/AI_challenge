import time
import os
import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup
from slugify import slugify


def cache_page(url):
    path = slugify(url) + ".html"
    html_pages_path = os.path.join(os.getcwd(), 'work_ua_html_pages')
    if path not in os.listdir(html_pages_path):
        while True:
            try:
                r = requests.get(url)
                break
            except Exception as e:
                print(e.with_traceback())
                time.sleep(1)
        with open(os.path.join(html_pages_path, path), "w", encoding="utf-8") as f:
            f.write(r.text)
    with open(os.path.join(html_pages_path, path), encoding="utf-8") as f:
        text = f.read()
    return text


def parse_main_pages(url_work):
    html_page = cache_page(url_work)

    soup = BeautifulSoup(html_page, 'html.parser')

    all_jobs_description = soup.find_all("div", {"class": "card card-hover card-visited wordwrap job-link js-hot-block"})
    string = '{}'
    table = json.loads(string)
    for i, job_description in enumerate(all_jobs_description):
        title_date = job_description.find_all("a")[0]['title']
        title, date = '', ''
        # if i == 3:
        #     pprint(job_description)
        try:
            start_date = title_date.rfind(",")
            title, date = title_date[:start_date], title_date[start_date:]
        except:
            print('no 1 parameter')

        city_tag = job_description.find(class_="add-top-xs")

        cities = ["Львів", "Київ", "Дніпро", "Одеса", "Харків", "Львов", "Киев", "Днепр", "Одесса", "Харьков"]
        city = ''
        for city_on_site in cities:
            if str(city_tag).find(city_on_site):
                city = city_on_site
                break
        company = ''
        try:
            company = job_description.find_all("img")[0]["alt"]
        except:
            print("company is not written")
        url = job_description.a['href']
        url = "https://www.work.ua" + url
        table[i + 1] = dict()
        table[i + 1]["title"] = title
        table[i + 1]["company"] = company
        table[i + 1]["city"] = city
        table[i + 1]["date"] = date
        table[i + 1]["url"] = url
        # if i == 4:
        #     #     break

    return table


if __name__ == "__main__":
    # n_vacancy = 1
    #     # for i in range(423):
    #     #     url_work = 'https://www.work.ua/jobs-it/?advs=1&page='
    #     #     url_work += str(i + 1)
    #     #     pprint(parse_main_pages(url_work))
    #     #     print(i)
    print(time.version)
