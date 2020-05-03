import json
from bs4 import BeautifulSoup


def main():
    with open("page.json", 'r', encoding='utf-8') as page_file:
        data = json.load(page_file)

    with open("page.json", 'w', encoding='utf-8') as page_file:
        json.dump(data, page_file, indent=3)

    res = {}
    for course in data:
        name = course["card"]["content"]["title"]
        res[name] = {}
        res[name]["url"] = course["card"]["href"]
        res[name]["image"] = course["card"]["background"]["url"]
        try:
            res[name]["short_description"] = course["card"]["content"]["body"][0]
        except IndexError:
            res[name]["short_description"] = course["card"]["content"]["body"]
        res[name]["price"] = "Free"
        res[name]["number_of_students"] = ""
        res[name]["long_description"] = ""
        res[name]["course_duration"] = ""

    with open("result.json", 'w', encoding='utf-8') as res_file:
        res_file.write(json.dumps(res, indent=3))


if __name__ == '__main__':
    main()
