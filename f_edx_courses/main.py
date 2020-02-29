"""
This module generates a list of courses from edx in result.json. 
"""
import requests
from requests import HTTPError
from json import JSONDecodeError
import json

# Global variables
with open("access_token.json", 'r') as access_file:
    ACCESS_TOKEN = json.load(access_file)["access_token"]
ERROR_NUMBER = 1

def get_access_token():
    """
    creates new access token. Saves response to new file
    and changes global variable
    :return: None
    """
    client_id = "uJTHYlHuUqVuKi47LecSiu62u9UpQMLAh8SXvsn6"
    client_secret = "6d9z1S4SZLzNcrSD2liVfImUTV8FAgRmEkDdqiSL2LAnGukIvs7OHarZ23mGZiGlitzWLWJasrvRiNK7tDEeHSDkiE4y8KdWBVmmgdNDSKoQVp1gzFJeRa2wbflEIltA"
    link = "https://api.edx.org/oauth2/v1/access_token"
    response = requests.post(link, data={"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret, "token_type": "jwt"})
    with open("access_token.json", 'w') as token_file:
        json.dump(response.json(), token_file, indent=3)
    global ACCESS_TOKEN
    ACCESS_TOKEN = response.json()["access_token"]


def generate_info(max_page, route="", beginner = "http://courses.edx.org/api/", writting_way='a'):
    """
    main fucntion
    :param max_page: a number of responses
    :param route: from where you want to take information
    :param beginner:
    :param writting_way: 'a' to write all results, 'w' for saving only last
    :return: None
    """

    if route == "":
        web_page = beginner + "courses/v1/courses_ids/"
    else:
        web_page = beginner + route

    current_page = 1
    global ACCESS_TOKEN
    global ERROR_NUMBER
    while current_page <= max_page:
        "make main request"
        response = requests.get(web_page, headers={"Authorization": f"JWT {ACCESS_TOKEN}"})

        print(str(response.status_code) + '\n' + f"   Number of requests: {current_page}\n" +
              f"      Number of errors: {ERROR_NUMBER }")

        # Error handling
        if str(response.status_code)[0] == '4':
            with open("errors.json", 'r') as error_file:
                errors = json.load(error_file)
            errors[str(ERROR_NUMBER)] = response.text
            with open("errors.json", 'w') as error_file:
                json.dump(errors, error_file, indent=3)

            if response.status_code == 403 or response.status_code == 401:
                get_access_token()
                current_page += 1
            ERROR_NUMBER += 1
            continue

        try:
            data = response.json()
        except JSONDecodeError:
            current_page += 1
            continue

        # create result before writting in it
        if writting_way == 'a':
            with open("result.json", 'r', encoding='utf-8', errors='ignore') as res_file:
                result = json.load(res_file)
        else:
            result = {}

        # adding new information about new courses
        for course in data["results"]:
            result[course["name"]] = {
                "url": course["blocks_url"],
                "id": [course["id"], course["course_id"]],
                "media": course["media"],
                "short_description": course["short_description"],
                "start_end": [course["start"], course["end"]],
                "start_display": course["start_display"],
                "org": course["org"]
            }

        # saving information
        with open("result.json", 'w', encoding='utf-8', errors='ignore') as res_file:
            json.dump(result, res_file, indent=4)

        current_page += 1

        web_page = data["pagination"]["next"]
        if web_page is None:
            print(current_page)
            break

if __name__ == '__main__':
    # get_access_token()
    with open("result.json", 'w') as res_file:
        res_file.write("{}")
    with open("errors.json", 'w') as error_file:
        error_file.write("{}")
    generate_info(1000, route="courses/v1/courses/", writting_way='a')
