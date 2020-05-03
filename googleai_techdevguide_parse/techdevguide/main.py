from bs4 import BeautifulSoup
import re
import json
import requests

# load text from main page with courses
with open("main_page.html", 'r', encoding='utf-8') as page_file:
    text = page_file.read()

# load to soup
soup = BeautifulSoup(text, "html.parser")

result = {}

# iterate through elements of list in html
for item in soup.find_all("li"):
    try:
        # find the in online-courses category  and save name + url
        if item["class"] == ['resource', 'grid__item', 'one-whole', 'tablet--one-half', 'desk--one-third']:

            name = re.search(r"(?<=<span itemprop=\"name\">)(.)*(?=</span>)", str(item)).group(0)
            if name:
                result[name] = {}
            url = re.search(r"(?<=<a class=\"link link--header\" href=\")(.)*(?=\" itemprop=\"url\")", str(item))
            result[name]["url"] = "https://techdevguide.withgoogle.com" + url.group(0)
            #break
    except KeyError:
        pass

# iterate through found courses
i = 1
length = len(result)
for course in result:
    print(f"Parsing {course}...")
    text = requests.get(result[course]["url"]).text

    short_description = re.search("(?<=name=\"description\" content=\")(.)*(?=\" itemprop=\"description\")", text).group(0)
    result[course]["short_description"] = short_description

    image_link = re.search("(?<=property=\"og:image\" content=\")(.)*(?=\">)", text).group(0)
    result[course]["image"] = image_link

    result[course]["price"] = "Free"

    result[course]["number_of_students"] = ""
    result[course]["course_duration"] = ""
    result[course]["long_description"] = ""

    print(f"done ({i}/{length})")
    i += 1

with open("techdevguide_result.json", 'w', encoding='utf-8') as res_file:
    res_file.write(json.dumps(result, indent=3))


