#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os
import re
from datetime import datetime
from pathlib import Path
from io import open

import boto3
import requests
import json
import urllib
from bs4 import BeautifulSoup
from slugify import slugify

from working_with_files_functions import save_json_name_profession


def vacancy_pages_save(url, n_save_page, name_profession_save):
    html = urllib.request.urlopen(url).read()
    mycwd = os.getcwd()
    os.chdir("..")
    vacancy_pages_path = os.path.join(os.getcwd(), 'vacancy_text_pages')
    os.chdir(mycwd)
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

    mycwd = os.getcwd()
    os.chdir("..")
    temp_directory = Path('vacancy_text_pages')
    temp_directory.mkdir(exist_ok=True)
    profession_directory = Path(os.path.join(os.getcwd(), 'vacancy_text_pages', name_profession_save))
    profession_directory.mkdir(exist_ok=True)
    os.chdir(mycwd)

    with open(os.path.join(vacancy_pages_path, profession_directory, name_profession_save + '_page{}'.format(str(n_save_page))), "w", encoding="utf-8") as f:
        f.write(text)


def cache_page(url, root_path):
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url='https://fra1.digitaloceanspaces.com',
                            aws_access_key_id='4X7VNYMKWLTZV5G5JXEV',
                            aws_secret_access_key='dmifQIBG5a8hzPcBXsohAnDeJCfMrY2W5ryOE87U1fE')

    filename = slugify(url) + ".html"

    mycwd = os.getcwd()
    os.chdir("..")
    html_pages_path = os.path.join(os.getcwd(), 'work_ua_html_pages')
    os.chdir(mycwd)
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


def parse_main_pages(url_work, n_page, urls_vacancies, root_path, root_path_vacancies, name_profession_main):
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
        vacancy_pages_save(url, start_save_page, name_profession_main)
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


def get_name_profession(name_profession):
    name_profession = name_profession.lower()
    name_profession = name_profession.replace(" ", "+")

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    root_path = os.path.join('work_ua_pages', timestamp).replace("\\", "/")
    root_path_vacancies = os.path.join('work_ua_vacancies_pages', timestamp).replace("\\", "/")

    n_pages = 200
    urls_vacancies = '{}'
    urls_vacancies = json.loads(urls_vacancies)
    for i in range(n_pages):
        # try:
            url_work = 'https://www.work.ua/jobs-{}/?advs=1&page='.format(name_profession)
            url_work += str(i + 1)
            table, html_page = parse_main_pages(url_work, i, urls_vacancies, root_path,
                                                root_path_vacancies, name_profession)
            print(i + 1)
            if table == {}:
                print(name_profession, i, "last page of this profession")
                break
            # pprint(table)
            save_json_name_profession(n_save_page=i + 1, json_page_professions=table,
                                      name_profession_json_save=name_profession)
            time.sleep(1)
        # except Exception:
        #     print(name_profession, i, "last page of this profession")


if __name__ == "__main__":
    # "Специалист технической поддержки", "Администратор",
    # "Системный администратор", "SMM-менеджер", "Аналитик",

    # "Интернет-маркетолог",
    # "Менеджер по работе с клиентами", "Маркетолог", "Программист PHP", "IT-специалист",
    #
    # "Customer support representative", "Support manager", "Спеціаліст технічної підтримки",
    #
    # "Customer support specialist", "Менеджер з продажу", "Онлайн-консультант",
    # "Менеджер інтернет-магазину", "Sales manager", "Javascript-програміст", 'Javascript developer',
    #
    # "Контент-менеджер", "Маркетолог", "Бренд-менеджер", "Marketing manager", "Content manager",
    #
    # "Business analyst", "Data analyst", "Адміністратор баз даних",
    #
    # "Інтернет-маркетолог", "Маркетолог", "Бренд-менеджер", "Менеджер з реклами",
    # "Marketing manager", "Адміністратор сайта",
    #
    # "Менеджер з продажу", "Онлайн-консультант", "Менеджер інтернет-магазину", "Sales manager",

    work_ua_vacancies = ["Бренд-менеджер", "Marketing manager", "Інтернет-маркетолог", "Data scientist", "Аналітик",
                         "Analyst",

                         "Програміст PHP", "PHP developer", "Розробник PHP", "Full stack developer",
                         "Full stack програміст",
                         "Back end програміст", "Back end developer"]

    for name_profession in work_ua_vacancies:
        get_name_profession(name_profession)
    # static_path = os.path.join(os.getcwd(), 'static')
    # with open(os.path.join(static_path, 'urls_vacancies' + ".json"), "w", encoding="utf-8") as f:
    #     json.dump(urls_vacancies, f, indent = 4)
