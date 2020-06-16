import json
import os
import sqlite3

import sqlalchemy
from flask_app import db
from flask_app.models import Profession, Skill, Course

def inject_all():
    root = os.path.join('user_data', "courses_for_all_professions", "courses_for_IT_professions")
    files = os.listdir(root)
    courses = {}
    skills = {}
    for file in files:
        path = os.path.join(root, file)
        profession_name = ' '.join(file[:-5].split('+')) + "6"
        print(profession_name)
        profession = Profession(name=profession_name)
        info = json.load(open(path, encoding="utf-8"))
        for skill_name in info:
            if skill_name not in skills:
                skill = Skill(name=skill_name)
                for course_data in info[skill_name]:
                    if course_data["url"] in courses:
                        course = courses[course_data["url"]]
                    else:
                        if type(course_data["image"]) == dict:
                            course_data["image"] = course_data["image"]["small"]
                        course = Course(course_title=course_data["course_title"],
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
                    skill.courses.append(course)
                skills[skill_name] = skill
                db.session.add(skill)
                db.session.commit()
            else:
                skill = skills[skill_name]
            profession.skills.append(skill)
        db.session.add(profession)
        db.session.commit()


if __name__ == '__main__':
    inject_all()
