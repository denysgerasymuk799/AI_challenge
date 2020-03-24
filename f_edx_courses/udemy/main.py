from pyudemy import Udemy
import json
import random
import time
try:
    from .get_more_info import get_more_info
except ImportError:
    from get_more_info import get_more_info


CLIENT_ID = 'XGwKUxLDixGf4mD9UHJNCPLXD9vzVfM6NA9YKufa'
CLIENT_SECRET = 'gYeTjrLot8ndRDdGyBwe1dx3SEVzrwVmAzOpxieZWZOqPYXwGpt6dWmd5xWZ1L7Rxazec5o25' \
                'LANhkgByzsm3J0XtQJxPFpMHJRpzMUb7fFAXidW2hYygnebyO67X83L'
UDEMY = Udemy(CLIENT_ID, CLIENT_SECRET)


def generate_result(max_page=999999999):
    """
    Main function, that generates udemy_results.json file
    :param max_page: number of pages to search
    """
    current_page = 1
    while current_page <= max_page:
        # getting result dictionary
        result = json.load(open("udemy_results.json", 'r'))

        # getting information from API
        current_courses_info = UDEMY.courses(page=current_page)

        print(f"Number of requests: {current_page}")

        # Adding information from API to result dict
        for course in current_courses_info["results"]:
            course_name = course["title"]
            result[course_name] = {}

            result[course_name]["id"] = course["id"]
            result[course_name]["url"] = 'https://udemy.com' + course["url"]
            result[course_name]["price"] = course["price"]
            result[course_name]["short_description"] = course["headline"]
            result[course_name]["image"] = {
                "image_125_H": course["image_125_H"],
                "image_240x135": course["image_240x135"],
                "image_480x270": course["image_480x270"]
            }

            # # More info
            # more_info = get_more_info(result[course_name]["url"], course_name)
            # if more_info == {}:
            #     print("      Trying again in 5 seconds...")
            #     time.sleep(5)
            #     more_info = get_more_info(result[course_name]["url"], course_name)
            #     if more_info == {}:
            #         continue
            # result[course_name]["number_of_students"] = more_info["number_of_students"]
            # result[course_name]["short_description"] = more_info["short_description"]
            # result[course_name]["long_description"] = more_info["long_description"]
            #
            # time.sleep(random.random()*2 + 1)

        with open("udemy_results.json", 'w', encoding='utf-8', errors='ignore') as res_file:
            json.dump(result, res_file, indent=4)

        current_page += 1


if __name__ == '__main__':
    with open("udemy_results.json", 'w') as res_file:
        res_file.write("{}")
    generate_result()
