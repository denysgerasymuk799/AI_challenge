from pyudemy import Udemy
import json


CLIENT_ID = 'XGwKUxLDixGf4mD9UHJNCPLXD9vzVfM6NA9YKufa'
CLIENT_SECRET = 'gYeTjrLot8ndRDdGyBwe1dx3SEVzrwVmAzOpxieZWZOqPYXwGpt6dWmd5xWZ1L7Rxazec5o25' \
                'LANhkgByzsm3J0XtQJxPFpMHJRpzMUb7fFAXidW2hYygnebyO67X83L'
UDEMY = Udemy(CLIENT_ID, CLIENT_SECRET)


def generate_result(max_page=999999999):
    """
    Main function, that generates udemy_result.json file
    :param max_page: number of pages to search
    """
    current_page = 1
    while current_page != max_page:
        # getting result dictionary
        result = json.load(open("udemy_result.json", 'r'))

        # getting information from API
        current_courses_info = UDEMY.courses(page=current_page)

        # Adding information from API to result dict
        for course in current_courses_info["results"]:
            course_name = course["title"]
            result[course_name]["id"] = course["id"]
            result[course_name]["url"] = course["url"]
            result[course_name]["price"] = course["price"]
            result[course_name]["image"] = {
                "image_125_H": course["image_125_H"],
                "image_240x135": course["image_240x135"],
                "image_480x270": course["image_480x270"]
            }
            result[course_name]["short_description"] = course["headline"]

            # >>>>>>>Here will be more code, that uses parcing

        json.dump(open("udemy_result.json", 'w'), result, indent=3)


if __name__ == '__main__':
    with open("udemy_result.json", 'w') as res_file:
        res_file.write("{}")
    generate_result(10)