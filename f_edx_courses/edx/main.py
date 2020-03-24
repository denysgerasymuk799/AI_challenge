import requests
from json import JSONDecodeError
import json
import get_descriptions
from price_student_number import get_price, get_student_number

# Global variables
with open("tmp_files/access_token.json", 'r') as access_file:
    ACCESS_TOKEN = json.load(access_file)["access_token"]
ERROR_NUMBER = 0
SKIPPED = 0
PARSED_NUMBER = 0


def generate_duration(start, end):
    start = start.split('-')
    end = end.split('-')
    result = 0
    start_year, end_year = int(start[0]), int(end[0])
    start_week, end_week = int(start[1]), int(end[1])
    start_day, end_day = int(start[2][:2]), int(end[2][:2])
    result += abs(end_year - start_year)*52
    result += abs(end_week - start_week)
    result += abs(end_day - end_week)/7
    return str(int(result)) + " weeks"


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
    with open("tmp_files/access_token.json", 'w') as token_file:
        json.dump(response.json(), token_file, indent=3)
    global ACCESS_TOKEN
    ACCESS_TOKEN = response.json()["access_token"]


def generate_info(max_page, route="", beginner = "http://courses.edx.org/api/"):
    """
    main fucntion
    :param max_page: a number of responses
    :param route: from where you want to take information
    :param beginner:
    :param writting_way: 'a' to write all results, 'w' for saving only last
    :return: None
    """
    global SKIPPED, PARSED_NUMBER

    if route == "":
        web_page = beginner + "courses/v1/courses/"
    else:
        web_page = beginner + route

    # some variables
    current_page = 1
    global ACCESS_TOKEN
    global ERROR_NUMBER

    while current_page <= max_page:
        PARSED_NUMBER += 1
        # make main request
        response = requests.get(web_page, headers={"Authorization": f"JWT {ACCESS_TOKEN}"})

        # some info
        print(str(response.status_code) + '\n' + f"   Number of API requests: {current_page}\n" +
              f"      Number of errors: {ERROR_NUMBER }")

        # Error handling
        if str(response.status_code)[0] == '4':
            # writing error to file
            with open("tmp_files/errors.json", 'r', encoding="utf-8") as error_file:
                errors = json.load(error_file)
            errors[str(ERROR_NUMBER)] = response.text
            with open("tmp_files/errors.json", 'w', encoding="utf-8") as error_file:
                json.dump(errors, error_file, indent=3)

            # 401 - you should get new access token
            if response.status_code == 401:
                get_access_token()
                current_page += 1
            ERROR_NUMBER += 1
            continue

        try:
            data = response.json()
        except JSONDecodeError:
            print(">>> Json error occured! something wrong!!!")
            current_page += 1
            continue

        # create result from result file before writting in it
        with open("edx_results.json", 'r', encoding='utf-8', errors='ignore') as res_file:
            result = json.load(res_file)

        # adding new information about new courses
        for course in data["results"]:
            PARSED_NUMBER += 1

            # Writing all needed information
            course_name = course["name"]
            course_url = get_descriptions.convert_to_url(course_name)
            description = get_descriptions.generate_description(course_name)
            if description == -1:
                SKIPPED += 1
                continue

            result[course_name] = {
                "id": [course["id"], course["course_id"]],
                "image": course["media"]["image"],
            }

            # duration generation
            start, end = course["start"], course["end"]
            if start and end:
                result[course_name]["course_duration"] = generate_duration(start, end)
            else:
                result[course_name]["course_duration"] = ""

            result[course_name]["price"] = get_price()
            result[course_name]["long_description"] = description["long_description"]
            result[course_name]["short_description"] = description["short_description"]
            result[course_name]["url"] = course_url
            result[course_name]["number_of_students"] = get_student_number()
            skipped_percentage = round(SKIPPED/PARSED_NUMBER, 2)
            print(f"        Parsed_number: {PARSED_NUMBER}, Skipped Percentage: {skipped_percentage}\n"
                  f"        Successful parse: {course_name}. ")

        # saving information
        with open("edx_results.json", 'w', encoding='utf-8', errors='ignore') as res_file:
            json.dump(result, res_file, indent=4)

        current_page += 1

        web_page = data["pagination"]["next"]
        with open("tmp_files/last_page.txt", 'w', encoding="utf-8") as last_page_file:
            last_page_file.write(web_page + '\n')


if __name__ == '__main__':
    # get_access_token()
    with open("edx_results.json", 'w', encoding="utf-8") as res_file:
        res_file.write("{}")
    with open("tmp_files/errors.json", 'w', encoding="utf-8") as error_file:
        error_file.write("{}")
    generate_info(10, route="courses/v1/courses/")
