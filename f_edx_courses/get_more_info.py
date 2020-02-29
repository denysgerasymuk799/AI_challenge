import requests
from requests import HTTPError
from json import JSONDecodeError
import json

# Global variables
with open("access_token.json", 'r') as access_file:
    ACCESS_TOKEN = json.load(access_file)["access_token"]

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


def generate_info(max_page, route="", beginner = "http://courses.edx.org/api/"):
    """
    main fucntion
    :param max_page: a number of responses
    :param route: from where you want to take information
    :param beginner:
    :param writting_way: 'a' to write all results, 'w' for saving only last
    :return: None
    """

    if route == "":
        web_page = beginner + "courses/v2/blocks/?course_id=course-v1%3ABerkeleyX%2BCS169.1x%2B3T2017SP"
    else:
        web_page = beginner + route

    current_page = 1
    global ACCESS_TOKEN
    while current_page <= max_page:
        "make main request"
        response = requests.get(web_page, headers={"Authorization": f"JWT {ACCESS_TOKEN}"},
                                params={
                                    "all_blocks": "true"
                                })
        """
        "depth": "all",
        "requested_fields": "graded,format,student_view_multi_device,lti_url",
        "block_counts": "video", "student_view_data": "video",
        "block_types_filter": "problem,html"
        """

        print(response.status_code)
        try:
            data = response.json()
        except JSONDecodeError:
            current_page += 1
            continue

        # saving information
        with open("more_result.json", 'w', encoding='utf-8', errors='ignore') as res_file:
            json.dump(data, res_file, indent=4)

        current_page += 1

if __name__ == '__main__':
    # get_access_token()
    generate_info(1, route="courseware/course/course-v1%3ABerkeleyX%2BCS169.1x%2B3T2017SP/")
