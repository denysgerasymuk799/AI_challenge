import json
import requests


TRASH = ["<","<p>","/",">","</p>",]
CONVERT_TRASH = [":", "\"", ",", "(", ")", "  archived", "-", "archived"]


def convert_to_url(course_name):
    course_name = course_name.lower()
    for piece in CONVERT_TRASH:
        course_name = course_name.replace(piece, '')
    url_course_name = '-'.join(course_name.split(" "))
    return "https://www.edx.org/course/" + url_course_name


def parsing_special_courses(key_word):
    description = ""

    # this is case, when page has another format
    with open("tmp_file/description.html", 'r', encoding="utf-8") as html_file:
        data = html_file.read()
        begin_index = data.find(key_word)

        if begin_index == -1:
            return description

        begin_index += 14

        # Now let'l parse this stuff
        try:
            while True:

                description += data[begin_index]

                if data[begin_index] == "\"" and data[begin_index + 1] == "," and \
                        data[begin_index + 2] == "\"":
                    break

                begin_index += 1

        except Exception as err:
            print(str(err))

    return description


def generate_description(course_name):

    # generate url
    URL = convert_to_url(course_name)

    # make request and generate file to parse
    response = requests.get(URL)
    with open("tmp_files/description.html", 'w', encoding="utf-8") as res_file:
        res_file.write(response.text)

    result = {}

    # Look for description and parse it
    description = ""
    what_you_learn = ""
    with open("tmp_files/description.html", 'r', encoding="utf-8") as html_file:
        end_reading = False
        for line in html_file:
            if "course-description" in line: # Checkpot!
                line = line.split("div")
                for elem in line:

                    # in this line surely is course description
                    if "course-description" in elem:
                        description = elem

                        # Now let's delete all shit
                        description = description.replace("class=\"course-description\">", '')
                        for piece in TRASH:
                            description.replace(piece, '')

                        # save found description
                        result["long_description"] = description
                        end_reading = True
                        break

            if end_reading:
                break

    # Look for <what you'll be learnt> in the course
    with open("tmp_files/description.html", 'r', encoding="utf-8") as html_file:
        for line in html_file:
            if line.startswith("<li>"):
                new_line = line
                new_line = new_line.replace("<li>", '')
                new_line = new_line.replace("</li>", '')
                what_you_learn += new_line + '\n'

        result["short_description"] = what_you_learn

    # manage skipped courses
    if not description:

        # # this is case, when page has another format. 1.description
        # description = parsing_special_courses("\"description\":")
        #
        # # Now let's look for what you'll learn
        # what_you_learn = parsing_special_courses("\"educationalOutcome\":")
        #
        # if not description:
        #     # with open("skipped_courses.json", 'a') as skipped_file:
        #     #     skipped_file.write(course_name + ': ' + URL + '\n')
        #     return -1
        #
        # result["long_description"] = description
        # result["short_description"] = what_you_learn
        return -1

    return result


def download_course_page(course_name=""):

    # Make request and print corresponding info
    URL = convert_to_url(course_name)

    response = requests.get(URL)
    print("    " + str(response.status_code))

    with open("tmp_files/description.html", 'w', encoding="utf-8") as res_file:
        res_file.write(response.text)


if __name__ == '__main__':
    course_name = "Essential Human Biology: Cells and Tissues"
    download_course_page(course_name)