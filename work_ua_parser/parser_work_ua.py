import time
import os
import re
from datetime import datetime

import boto3
import requests
import json
import urllib
from pprint import pprint
from bs4 import BeautifulSoup
from slugify import slugify


def vacancy_pages_save(url, n_save_page):
    html = urllib.request.urlopen(url).read()
    vacancy_pages_path = os.path.join(os.getcwd(), 'vacancy_text_pages')
    soup = BeautifulSoup(html, "lxml")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    with open(os.path.join(vacancy_pages_path, 'vacancy_page{}'.format(str(n_save_page))), "w", encoding="utf-8") as f:
        f.write(text)


def cache_page(url, root_path):
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url='https://fra1.digitaloceanspaces.com',
                            aws_access_key_id='4X7VNYMKWLTZV5G5JXEV',
                            aws_secret_access_key='dmifQIBG5a8hzPcBXsohAnDeJCfMrY2W5ryOE87U1fE')

    filename = slugify(url) + ".html"
    html_pages_path = os.path.join(os.getcwd(), 'work_ua_html_pages')
    if filename not in os.listdir(html_pages_path):
        while True:
            try:
                r = requests.get(url)
                break
            except Exception as e:
                print(e.with_traceback())
                time.sleep(1)
        with open(os.path.join(html_pages_path, filename), "w", encoding="utf-8") as f:
            f.write(r.text)
    with open(os.path.join(html_pages_path, filename), encoding="utf-8") as f:
        text = f.read()

    tmp_file = os.path.join(html_pages_path, filename)
    client.upload_file(tmp_file, 'ai-scrapper', os.path.join(root_path, filename).replace("\\", "/"))
    return text


def parse_vacancy_pages(url_work, root_path_vacancies, table, n_vacancy):
    html_page = cache_page(url_work, root_path_vacancies)

    soup = BeautifulSoup(html_page, 'html.parser')

    all_vacancy_description = soup.find_all("div", {"class": "card wordwrap"})

    job_description = all_vacancy_description[0].find_all("div", {"id": "job-description"})
    cleanr = re.compile('<.*?>')
    clean_job_description = re.sub(cleanr, '', str(job_description))
    table[n_vacancy]["job_description"] = clean_job_description
    return table


def parse_main_pages(url_work, n_page, urls_vacancies, root_path, root_path_vacancies):
    html_page = cache_page(url_work, root_path)
    soup = BeautifulSoup(html_page, 'html.parser')

    if soup.find_all("div", {"class": "card card-hover card-visited wordwrap job-link js-hot-block"}):
        all_jobs_description = soup.find_all("div", {"class": "card card-hover card-visited wordwrap job-link js-hot-block"})
    else:
        all_jobs_description = soup.find_all("div",
                                             {"class": "card card-hover card-visited wordwrap job-link"})
    string = '{}'
    table = json.loads(string)

    for i, job_description in enumerate(all_jobs_description):
        title_date = job_description.find_all("a")[0]['title']
        title, date = '', ''
        # if i == 3:
        #     pprint(job_description)
        try:
            start_date = title_date.rfind(",")
            title, date = title_date[:start_date], title_date[start_date + 2:]
        except:
            print('no 1 parameter')

        city_tag = job_description.find(class_="add-top-xs")

        cities = ["Львів", "Київ", "Дніпро", "Одеса", "Харків", "Львов", "Киев", "Днепр", "Одесса", "Харьков"]
        city = ''
        for city_on_site in cities:
            if str(city_tag).find(city_on_site):
                city = city_on_site
                break

        company = job_description.find(class_="add-top-xs")
        company = company.find('span')
        company = str(company.find('b'))
        start_company_title = company.find('>')
        end_company_title = company.rfind('<')
        company = company[start_company_title + 1: end_company_title]

        url = job_description.a['href']
        url = "https://www.work.ua" + url
        start_save_page = n_page * len(all_jobs_description) + i + 1
        # vacancy_pages_save(url, start_save_page)
        urls_vacancies[str(start_save_page)] = url
        table[i + 1] = dict()
        table[i + 1]["title"] = title
        table[i + 1]["company"] = company
        table[i + 1]["city"] = city
        table[i + 1]["date"] = date
        table[i + 1]["url"] = url

        n_vacancy = i + 1
        table = parse_vacancy_pages(url, root_path_vacancies, table, n_vacancy)

    return table, html_page


if __name__ == "__main__":
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    root_path = os.path.join('work_ua_pages', timestamp).replace("\\", "/")
    root_path_vacancies = os.path.join('work_ua_vacancies_pages', timestamp).replace("\\", "/")

    n_vacancy = 1
    n_pages = 3
    urls_vacancies = '{}'
    urls_vacancies = json.loads(urls_vacancies)
    work_ua_vacancies = ["Администратор", "Специалист технической поддержки",
                         "Системный администратор", "SMM-менеджер", "Аналитик", "Интернет-маркетолог",
                         "Менеджер по работе с клиентами", "Маркетолог", "Программист PHP", "IT-специалист"]
    for i in range(n_pages):
        url_work = 'https://www.work.ua/jobs-it/?advs=1&page='
        url_work += str(i + 1)
        table, html_page = parse_main_pages(url_work, i, urls_vacancies, root_path, root_path_vacancies)
        print(i + 1)
        pprint(table)
        time.sleep(1)

    # static_path = os.path.join(os.getcwd(), 'static')
    # with open(os.path.join(static_path, 'urls_vacancies' + ".json"), "w", encoding="utf-8") as f:
    #     json.dump(urls_vacancies, f, indent = 4)