import json
import os
import requests
import re
from bs4 import BeautifulSoup


def get_page_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    return result.content.decode()


def course_info_parser(url):
    html_data = get_page_data(url)

    soup = BeautifulSoup(html_data, 'html.parser')

    data = {}

    image = soup.find('img', attrs={'class': 'img-responsive'})
    data['image'] = "https://www.tutorialspoint.com" + image['src']

    data['course_duration'] = ""

    buttons = soup.find_all('a')
    price_url = ""
    for button in buttons:
        if button.get_text() == "PDF Version":
            price_url = "https://www.tutorialspoint.com" + button['href']
            break
    try:
        price_data = get_page_data(price_url)

        soup_price = BeautifulSoup(price_data, 'html.parser')
        price = re.findall(r'\$\d+\.\d+', soup_price.find('p').get_text())[0]

        data['price'] = price + ", but tutorial is free"
    except:
        data['price'] = "FREE"

    data['long_description'] = ""

    description_list = soup.find_all('p')
    long_description = ""

    for tag in description_list[:2:]:
        long_description += tag.get_text() + " "
    data['short_description'] = long_description

    data['url'] = url

    data['number_of_students'] = ""

    return data


def course_parser():
    html_data = get_page_data('https://www.tutorialspoint.com/tutorialslibrary.htm')
    soup = BeautifulSoup(html_data, 'html.parser')

    course_data = {}

    courses_groups = soup.find_all('ul', attrs={'class': 'menu'})

    for courses_group in courses_groups:
        for course in courses_group.find_all('li'):
            try:
                print("Receiving", course.find('a').get_text())
                url = "https://www.tutorialspoint.com" + course.find('a')['href']
                course_data[course.find('a').get_text()] = course_info_parser(url)
                print(course.find('a').get_text(), "is ready")

            except Exception as err:
                print(err)
                continue

    with open(os.path.join(os.getcwd(), 'tutorialspoint_courses.json'), 'w', encoding="utf-8") as f:
        json.dump(course_data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    course_parser()
