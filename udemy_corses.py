from pprint import pprint

from pyudemy import Udemy
import json
import requests
from pprint import pprint
import os


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


def find1_course_for_skill(courses_json_find1, skill_list_find1):
    courses_for_profession = dict()
    for course in courses_json_find1["results"]:
        for skill in skill_list_find1:
            if skill in course["headline"]:
                if course["title"] not in courses_for_profession:
                    courses_for_profession[skill] = {}
                    courses_for_profession[skill][course["title"]] = {}

                    courses_for_profession[skill][course["title"]]["headline"] = course["headline"]
                    courses_for_profession[skill][course["title"]]["url"] = "https://www.udemy.com" + course["url"]
                    courses_for_profession[skill][course["title"]]["price"] = course["price"]
                    courses_for_profession[skill][course["title"]]["image_240x135"] = course["image_240x135"]

    with open(os.path.join(os.getcwd(), 'udemy_courses_for_profession' + '.json'), "w", encoding="utf-8") as f:
        json.dump(courses_for_profession, f, indent=4)

    print("key2", len(courses_for_profession.keys()))


if __name__ == '__main__':
    client_id = 'XGwKUxLDixGf4mD9UHJNCPLXD9vzVfM6NA9YKufa'
    client_secret = 'gYeTjrLot8ndRDdGyBwe1dx3SEVzrwVmAzOpxieZWZOqPYXwGpt6dWmd5xWZ1L7Rxazec5o25' \
                    'LANhkgByzsm3J0XtQJxPFpMHJRpzMUb7fFAXidW2hYygnebyO67X83L'

    udemy = Udemy(client_id, client_secret)

    courses = udemy.courses()
    with open(os.path.join(os.getcwd(), 'udemy_courses' + '.json'), "w", encoding="utf-8") as f:
        json.dump(courses, f, indent=4)

    skill_list = ["AWS Machine Learning", "design", "Gamification"]
    find1_course_for_skill(courses, skill_list)
