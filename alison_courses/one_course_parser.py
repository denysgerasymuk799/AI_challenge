from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs


def parse(url):
    """
    Parses one page with given url
    :param url: str
    :return: dict
    """
    response = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
    source = bs(response, "html.parser")
    number_of_students = source.find("h4").string
    price = source.find(class_="course-brief--free").string
    title = source.find(class_="course-brief--title").h1.string.strip()
    short_description = source.find(class_="course-brief__headline").string
    duration = source.find(class_="course-brief--col2 match-height").span.string
    image = source.find(class_="course-brief--col3 match-height").img["src"]
    long_description = source.find(class_="course-brief--description").string.strip("\n")
    attr = ["price",
            "image",
            "course_duration",
            "number_of_students",
            "short_description",
            "long_description",
            "url"]
    value = [price, image, duration, number_of_students, short_description, long_description, url]
    attr_dict = {attr[j]: value[j] for j in range(7)}
    mini_res_dict = {title: attr_dict}
    return mini_res_dict
