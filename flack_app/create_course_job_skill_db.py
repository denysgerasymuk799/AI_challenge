import json
import os
import sqlite3
from application import db, Profession, Skill, Course


def create_db():
    # write in db
    for num_file, filename in enumerate(os.listdir(os.path.join('user_data', "courses_for_all_professions",
                                                                "courses_for_IT_professions"))):
        with open(os.path.join(os.getcwd(), 'user_data', "courses_for_all_professions",
                               "courses_for_IT_professions", filename),
                  'r', encoding="utf-8") as courses_for_profession:
            json_skills_for_profession = json.load(courses_for_profession)
            profession_name = ' '.join(filename[:-6].split('+'))
            try:
                print('profession_name', profession_name)
                p = Profession(name=profession_name.lower())
                db.session.add(p)

            except sqlite3.IntegrityError:
                continue

            # write skills for the special profession in db
            for skill_name in json_skills_for_profession.keys():
                s = Skill(name=skill_name.lower())
                db.session.add(s)

                p.skills.append(s)

                # write courses for the special profession in db
                for course_data in json_skills_for_profession[skill_name]:
                    if isinstance(course_data["image"], dict):
                        course_data["image"] = course_data["image"]["small"]
                    try:
                        course = Course(course_title=course_data["course_title"],
                                        price=course_data["price"],
                                        image=course_data["image"],
                                        number_of_students=course_data["number_of_students"],
                                        course_duration=course_data["course_duration"],
                                        short_description=course_data["short_description"],
                                        long_description=course_data["long_description"],
                                        url=course_data["url"])
                        db.session.add(course)
                    except sqlite3.IntegrityError:
                        continue

                    s.courses.append(course)

                db.create_all()
                try:
                    db.session.commit()
                except sqlite3.IntegrityError:
                    continue

    job1 = Profession.query.filter_by(name='analyst').first()
    print(job1.skills)


if __name__ == '__main__':
    create_db()
