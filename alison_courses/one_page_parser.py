from one_course_parser import parse
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

MAIN_PAGE_URL = "https://alison.com/courses"
FILE_NAME = "it_courses.json"
PAGE_NUMBER = 78


def get_main_page_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    browser = webdriver.Chrome(options=options)

    browser.get(url)

    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'course-block-wrapper'))
    WebDriverWait(browser, 20).until(element_present)

    generated_html = browser.page_source
    browser.quit()

    return generated_html


def course_parser(url):
    course_list = []
    html_data = get_main_page_data(url)
    soup = BeautifulSoup(html_data, 'html.parser')

    courses_data = soup.find('ul', attrs={'class': 'search-items clearfix'})
    courses = courses_data.find_all('li')

    for course in courses:
        if course != '\n':
            course_info = course.find('a')
            if course_info:
                course_list.append(course_info['href'])
    return course_list


def get_all_courses(start_url, num_of_pages):
    index = 1
    all_courses = []
    while index < num_of_pages + 1:
        current_url = start_url + "?page={}".format(index)
        all_courses.extend(course_parser(current_url))
        index += 1
    return all_courses


def main(url, path, num_of_pages):
    links_list = get_all_courses(url, num_of_pages)
    with open(path) as f:
        data = json.load(f)
    for j, link in enumerate(links_list):
        try:
            course = parse(link)
            key = list(course.keys())[0]
            data[key] = course[key]
            print(j, "/", len(links_list))
            if j % 50 == 0:
                with open(path, 'w') as json_file:
                    json.dump(data, json_file, indent=4, sort_keys=True, ensure_ascii=True)
        except Exception:
            continue
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4, sort_keys=True, ensure_ascii=True)


if __name__ == '__main__':
    main(MAIN_PAGE_URL, FILE_NAME, PAGE_NUMBER)
