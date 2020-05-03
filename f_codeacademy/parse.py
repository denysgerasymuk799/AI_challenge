import json
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def get_page_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    browser = webdriver.Chrome(options=options)

    browser.get(url)
    time.sleep(2)
    generated_html = browser.page_source
    browser.quit()

    return generated_html


def get_main_page_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    browser = webdriver.Chrome(options=options)

    browser.get(url)

    element_present = EC.presence_of_element_located((By.ID, 'course'))
    WebDriverWait(browser, 10).until(element_present)

    generated_html = browser.page_source
    browser.quit()

    return generated_html


def course_info_parser(url):
    html_data = get_page_data(url)

    soup = BeautifulSoup(html_data, 'html.parser')

    data = {}

    header = soup.find('main').find('header')
    image = header.find('img')
    data['image'] = "https://www.codecademy.com" + image['src']

    students_and_hours_data = soup.find_all('aside')[0]

    course_duration = students_and_hours_data.find('dd').get_text()
    data['course_duration'] = course_duration

    if header.find('div').find_all('img'):
        data['price'] = "15.99$"
    else:
        data['price'] = "FREE"

    description_list = soup.find_all('div', attrs={'data-testid': 'markdown'})
    long_description = ""

    for tag in description_list:
        long_description += tag.get_text() + " "
    data['long_description'] = long_description

    short_description = header.find('p').get_text()
    data['short_description'] = short_description

    data['url'] = url

    number_of_students = students_and_hours_data.find('span').get_text()
    data['number_of_students'] = number_of_students + " students"

    return data


def course_parser():
    html_data = get_main_page_data('https://www.codecademy.com/catalog/subject/all')
    soup = BeautifulSoup(html_data, 'html.parser')

    course_data = {}

    sections = soup.find_all('section')
    courses = sections[3].find_all('a')

    for course in courses:
        print("Receiving", course.find('h3').get_text())
        course_data[course.find('h3').get_text()] = course_info_parser("https://www.codecademy.com" + course['href'])
        print(course.find('h3').get_text(), "is ready")

    with open(os.path.join(os.getcwd(), 'codeacademy_courses.json'), "a", encoding="utf-8") as f:
        json.dump(course_data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    course_parser()
