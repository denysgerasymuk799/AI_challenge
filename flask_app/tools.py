"""
This module contains different tools for:
a) getting and saving information about user
b) getting skills for job and courses for skills
c) filtering skills and courses
"""

import os
import json
from flask_app.models import Profession, Skill


def get_user_info():
    """returns dict with information that user inputted"""
    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'r', encoding='utf-8') as \
            user_data_json_from_file:
        all_user_data = json.load(user_data_json_from_file)
    return all_user_data


def write_user_data(all_user_data):
    """Saves information about user"""
    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'w', encoding='utf-8') as \
            user_data_json_from_file:
        json.dump(all_user_data, user_data_json_from_file, indent=4, ensure_ascii=False)


def get_translation():
    """returns translation from file"""
    with open('translation.json') as json_file:
        dct = json.load(json_file)
        return dct


def skills_for_job(job):
    """
    :param job: str from user input
    :return: a list of skills for this profession from db
    """
    if job.endswith("2"):
        job = job[:-1]
    list_from_db = Profession.query.filter_by(name=job).first().skills

    result_skill_list = []
    print("list_from_db", list_from_db)
    for skill_db in list_from_db:
        skill_db = str(skill_db)
        skill_start = skill_db.find("'")
        skill_end = skill_db.rfind("'")
        skill = skill_db[skill_start + 1: skill_end]
        result_skill_list.append(skill)

    return result_skill_list


def get_courses(current_skills):
    """
    :param current_skills: a list of user skills which he input
    :return: a dict of courses for the special skill
    """
    all_user_data = get_user_info()

    skills_list = all_user_data["all_job_skills"]
    courses_dict = {}
    course_id = 0
    for skill in skills_list:
        if skill not in current_skills:
            courses_db = Skill.query.filter_by(name=skill).first().courses
            skill = skill.lower()
            courses_dict[skill] = []
            course_dict = {}
            for course in courses_db:
                course_id += 1
                course_dict["id"] = str(course_id)
                course_dict["course_title"] = course.course_title
                course_dict["price"] = course.price
                course_dict["image"] = course.image
                course_dict["course_duration"] = course.course_duration
                course_dict["number_of_students"] = course.number_of_students
                course_dict["short_description"] = course.short_description
                course_dict["long_description"] = course.long_description
                course_dict["url"] = course.url

            courses_dict[skill].append(course_dict)

    print("courses_dict", courses_dict)

    # use this filter for every courses for skill
    courses_dict = students_filter(courses_dict)

    return courses_dict

# <------------------- Filters ------------------>


def students_filter(courses_dict):
    """
    :param courses_dict:
    :return: filtered by number of students dict of courses
    """
    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'r', encoding='utf-8') as \
            user_data_json_from_file:
        all_user_data = json.load(user_data_json_from_file)

    skills_list = all_user_data["all_job_skills"]
    print(courses_dict)
    for skill in skills_list:
        try:
            skill = skill.lower()
            courses_dict[skill] = filter_param(courses_dict[skill])
        except KeyError:
            continue

    return courses_dict


def filter_param(courses_lst):
    """
    filter a list of courses by a number of students
    :param courses_lst:
    :return:
    """
    rest_courses = []
    position = 0
    while position != len(courses_lst):
        if not "," in courses_lst[position]['number_of_students']:
            rest_courses.append(courses_lst.pop(position))

        else:
            position += 1

    courses_lst = sorted(courses_lst,
                         key=lambda courses_lst: int("".join(courses_lst["number_of_students"].split()[0].split(","))),
                         reverse=True)
    courses_lst += rest_courses

    # for checking results
    for course in courses_lst:
        print(course["course_title"])
        print(course["number_of_students"])
        print()

    return courses_lst


def price_filter(courses_db):
    """

    :return: a list of special courses with parameter
    """
    for position in range(len(courses_db)):
        if courses_db[position].price.split()[0].lower() == "free":
            courses_db[position].price = "FREE    mix free"

        else:
            courses_db[position].price = courses_db[position].price + "    mix payed"

    return courses_db


def duration_filter(courses_lst):
    """

    :param courses_lst:
    :return: a result filtered list
    """
    duration_dict = {
        "0-10_hours": (0, 10),
        "10-20_hours": (11, 20),
        "20-30_hours": (21, 30),
        "30+_hours": (31, 40)
    }
    for position in range(len(courses_lst)):
        course_duration = courses_lst[position].course_duration.lower()
        if "minutes" in course_duration:
            course_duration = int(course_duration.split()[0]) / 60
        elif "approx." in course_duration:
            course_duration = int(course_duration.split()[1])
        elif "week" in course_duration:
            course_duration = 35
        elif course_duration.strip() == "yes":
            course_duration = 7
        elif "-" in course_duration and "hours" in course_duration:
            course_duration = int(course_duration.split("-")[0])
        elif "hour" in course_duration:
            course_duration = int(course_duration.split()[0])

        else:
            dict_durations = {"https://www.tutorialspoint.com/": 12,
                              "https://udemy.com/course/": 32,
                              "https://techdevguide.withgoogle.com/": 7}

            for site in dict_durations.keys():
                if site in course_duration:
                    course_duration = dict_durations[site]
                    break

        if course_duration == "":
            course_duration = 32

        for course_time in duration_dict.keys():
            min_duration, max_duration = duration_dict[course_time]
            if min_duration <= course_duration <= max_duration:
                courses_lst[position].price += " " + course_time
                break

        # courses_db[position].price = " " + courses_db[position].skill

    return courses_lst


def certificate_filter(courses_lst):
    """

    :param courses_lst:
    :return: a result list with courses in which url is one item from with_certificates list
    """
    with_certificates = ["https://alison.com/", "https://www.edx.org/", "https://www.codecademy.com/",
                         "https://udemy.com/", "https://www.coursera.org/"]

    for position in range(len(courses_lst)):
        flag_with_cerf = 0

        for site in with_certificates:
            if courses_lst[position].url.startswith(site):
                courses_lst[position].price += " with_cerf"
                flag_with_cerf = 1
                break

        if flag_with_cerf == 0:
            courses_lst[position].price += " without_cerf"

    return courses_lst

