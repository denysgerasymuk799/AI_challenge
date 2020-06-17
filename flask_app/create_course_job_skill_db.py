import json
import os
import sqlite3

import sqlalchemy
from flask_app import db
# from models import Profession, Skill, Course
from models import Profession2, Skill2, Course2


def inject_all():
    root = os.path.join('user_data', "courses_for_all_professions", "courses_for_IT_professions")
    files = os.listdir(root)

    course_parameters = ["number_of_students", "image", "course_duration", "price", "long_description",
                         "short_description", "url", "course_title"]

    courses = {}
    skills = {}
    for file in files:
        path = os.path.join(root, file)
        profession_name = ' '.join(file[:-5].split('+'))
        print(profession_name)

        try:
            profession = Profession2(name=profession_name)

        except Exception as er:
            print("ERROR1", er)
            continue

        info = json.load(open(path, encoding="utf-8"))
        for skill_name in info:
            if skill_name not in skills:
                try:
                    skill = Skill2(name=skill_name)

                except Exception as er:
                    print("ERROR2", er)
                    pass

                for course_data in info[skill_name]:
                    if course_data["url"] in courses:
                        course = courses[course_data["url"]]
                    else:
                        if type(course_data["image"]) == dict:
                            if "small" in course_data["image"].keys():
                                course_data["image"] = course_data["image"]["small"]

                            elif "image_125_H" in course_data["image"].keys():
                                course_data["image"] = course_data["image"]["image_125_H"]

                        for param in course_parameters:
                            if param not in course_data.keys():
                                course_data[param] = ""
                                if param == "long_description" or param == "short_description":
                                    course_data[param] = "Udemy course"

                                elif param == "number_of_students" and "udemy" in course_data["url"]:
                                    course_data["number_of_students"] = "45,000,000+ students"

                        try:
                            course = Course2(course_title=course_data["course_title"],
                                            price=course_data["price"],
                                            image=course_data["image"],
                                            number_of_students=course_data["number_of_students"],
                                            course_duration=course_data["course_duration"],
                                            short_description=course_data["short_description"],
                                            long_description=course_data["long_description"],
                                            url=course_data["url"])
                            courses[course_data["url"]] = course
                            db.session.add(course)
                            db.session.commit()

                        except Exception as er:
                            print("ERROR3", er)
                            continue

                    try:
                        skill.courses.append(course)

                    except Exception as er:
                        print("ERROR4", er)
                        continue

                skills[skill_name] = skill

                try:
                    db.session.add(skill)
                    db.session.commit()

                except Exception as er:
                    print("ERROR skill commit", er)
                    continue
            else:
                skill = skills[skill_name]

            try:
                profession.skills.append(skill)

            except Exception as er:
                print("ERROR5", er)
                continue

        try:
            db.session.add(profession)
            db.session.commit()

        except Exception as er:
            print("ERROR6", er)
            continue


if __name__ == '__main__':
    inject_all()
