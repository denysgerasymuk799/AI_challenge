import json
import re
import ssl
import time
from datetime import datetime

import boto3
import psycopg2
import requests
from pprint import pprint
import os

from psycopg2._json import Json
from psycopg2._psycopg import AsIs
from slugify import slugify
from bs4 import BeautifulSoup

# from parser_work_ua import cache_page
from sea_db import config, db_functions


def dir_for_save_html(dir_name):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    root_path_vacancies = os.path.join(os.getcwd(), "html_pages", dir_name, timestamp).replace("\\", "/")
    return root_path_vacancies


def cache_page(url, root_path, dir_name):
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url='https://fra1.digitaloceanspaces.com',
                            aws_access_key_id='4X7VNYMKWLTZV5G5JXEV',
                            aws_secret_access_key='dmifQIBG5a8hzPcBXsohAnDeJCfMrY2W5ryOE87U1fE')

    filename = slugify(url) + ".html"
    mycwd = os.getcwd()
    os.chdir("..")
    html_pages_path = os.path.join(os.path.join(os.getcwd(), "html_pages", dir_name))
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


def parse_course_pages(url_work, root_path_vacancies, table):
    html_page = cache_page(url_work, root_path_vacancies, 'coursera_pages')

    soup = BeautifulSoup(html_page, 'html.parser')

    # short_description in json
    try:
        all_course_ul_description = soup.find_all("ul", {"class": "Row_nvwp6p list-style-none p-a-0 p-l-1 m-b-0"})
        all_skills_course_description = all_course_ul_description[0].find_all("div", {"class": "P_gjs17i-o_O-weightNormal_s9jwp5-o_O-fontBody_56f0wi"})
        skills_description = []
        for item in all_skills_course_description:
            skills_description.append(item.p.string)

    except:
        skills_description = [""]

    # price in json
    price = "Free"

    # img in json
    all_img_attr = soup.find_all("img", {"aria-hidden": "true"})
    image = all_img_attr[1]["src"]

    # course_duration in json
    all_course_duration_attr = soup.find_all("span")
    print()
    print("url_work", url_work)
    course_duration = ''
    for span in all_course_duration_attr:
        if 'Approx.' in str(span):
            course_duration = span.string
            break

    all_students_attr = soup.find_all("strong")
    number_of_students = ''
    for strong in all_students_attr:
        flag_not_digit = 0
        if ',' not in str(strong.string):
            flag_not_digit = 1

        else:
            for part in strong.string.split(','):
                if not part.isdigit():
                    flag_not_digit = 1
                    break

        if flag_not_digit == 0:
            if strong.string == '1':
                number_of_students = strong.string + ' student'

            else:
                number_of_students = strong.string + ' students'
            break
        else:
            number_of_students = ''

    if number_of_students == '':
        all_div_views = soup.find_all("div", {"class": "viewsWithTextOnlyXdpExpertiseExp_es6xlk"})
        print(all_div_views)
        try:
            number_of_students = all_div_views[0].find_all("span")[1].string
        except:
            pass

    parameters = [price, image, course_duration, number_of_students, skills_description]
    text_parameters = ["price", "image", "course_duration", "number_of_students", "short_description"]
    for n_parameter in range(len(parameters)):
        if text_parameters[n_parameter] == "short_description":
            table["short_description"] = ""
            for line_description in skills_description:
                table["short_description"] += " " + str(line_description)

        else:
            table[text_parameters[n_parameter]] = parameters[n_parameter]

    return table


def find1_course_for_skill(courses_json_find1):
    courses_for_profession = dict()
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    n = 0

    # create path for config from this module to connect to database
    temp_dir = os.getcwd()
    os.chdir('..')
    filename = os.path.join(os.getcwd(), 'sea_db', 'courses_and_skills_db.ini')
    os.chdir(temp_dir)

    db_functions.create_table("Coursera", filename=filename)
    cur, conn = db_functions.connect_to_db(filename=filename)

    if cur:
        for n_course, course in enumerate(courses_json_find1):
            courses_for_profession[course["name"]] = {}

            root_path = os.path.join('coursera_pages', timestamp).replace("\\", "/")
            url = "https://www.coursera.org/learn/" + course["slug"]

            # course_for_profession = parse_course_pages(url, root_path, course_for_profession)
            courses_for_profession[course["name"]] = parse_course_pages(url, root_path, courses_for_profession[course["name"]])

            courses_for_profession[course["name"]]["long_description"] = course["description"]
            courses_for_profession[course["name"]]["url"] = "https://www.coursera.org/learn/" + course["slug"]
            # if n_course % 200 == 0:
            n += 1

            columns = courses_for_profession[course["name"]].keys()
            values = [course["name"]] + [courses_for_profession[course["name"]][column] for column in columns]

            insert_statement = 'INSERT INTO {} (course_title, %s) VALUES %s'.format("Coursera")

            cur.execute("ROLLBACK")
            conn.commit()
            cur.execute(insert_statement, (AsIs(', '.join(columns)), tuple(values)))
            conn.commit()

            courses_for_profession = {}
            # if n == 2:
            #     break

        cur.close()
        print("key2", len(courses_for_profession.keys()))


if __name__ == '__main__':
    url = "https://api.coursera.org/api/courses.v1?start=0&limit=2150&" \
          "includes=instructorIds,partnerIds,specializations,s12nlds,v1Details," \
          "v2Details&fields=instructorIds,partnerIds,specializations,s12nlds,description"
    data = requests.get(url).json()
    courses_json = data["elements"]
    print("key1", len(data["elements"]))

    skill_list = ["AWS Machine Learning", "design", "Gamification"]
    find1_course_for_skill(courses_json)
