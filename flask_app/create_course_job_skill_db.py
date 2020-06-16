import json
import os
import sqlite3

import sqlalchemy
from flask_app import db, Profession, Skill, Course


def create_db():
    # write in db
    for num_file, filename in enumerate(os.listdir(os.path.join('user_data', "courses_for_all_professions",
                                                                "courses_for_IT_professions"))):
        with open(os.path.join(os.getcwd(), 'user_data', "courses_for_all_professions",
                               "courses_for_IT_professions", filename),
                  'r', encoding="utf-8") as courses_for_profession:
            json_skills_for_profession = json.load(courses_for_profession)
            profession_name = ' '.join(filename[:-5].split('+')) + "6"
            try:
                print('profession_name', profession_name)
                p = Profession(name=profession_name.lower())
                db.session.add(p)
                # db.session.commit()

            except sqlite3.IntegrityError:
                continue
            except Exception:
                continue

            i = 0
            # write skills for the special profession in db
            for skill_name in json_skills_for_profession.keys():
                skill_name += "8"
                s = Skill(name=skill_name.lower())
                db.session.add(s)
                # db.session.commit()
                skill_name = skill_name[:-1]

                p.skills.append(s)
                db.session.add(p)
                # db.session.commit()

                # write courses for the special profession in db
                for course_data in json_skills_for_profession[skill_name]:
                    new_course = Course.query.filter_by(course_title=course_data["course_title"]).first()
                    # if isinstance(course_data["image"], dict):
                    #     course_data["image"] = course_data["image"]["small"]
                    # try:
                    #     course = Course(course_title=course_data["course_title"],
                    #                     price=course_data["price"],
                    #                     image=course_data["image"],
                    #                     number_of_students=course_data["number_of_students"],
                    #                     course_duration=course_data["course_duration"],
                    #                     short_description=course_data["short_description"],
                    #                     long_description=course_data["long_description"],
                    #                     url=course_data["url"])
                    #     db.session.add(course)
                    # except sqlite3.IntegrityError:
                    #     continue
                    # except Exception:
                    #     continue
                    # db.session.flush()
                    s.courses.append(new_course)
                    db.session.rollback()
                    db.session.add(s)
                    db.session.commit()
                    db.create_all()

                    print(skill_name, " - ", course_data["course_title"])
                    i += 1
                    if i == 4:
                        break

                # try:
                db.session.rollback()
                db.session.commit()
                db.create_all()
                if i == 4:
                    break
                #
                # except sqlite3.IntegrityError:
                #     continue
                # except sqlalchemy.exc.IntegrityError:
                #     continue
                # except sqlalchemy.exc.InvalidRequestError:
                #     continue

        break
                # except Exception:
                #     continue

    # job1 = Profession.query.filter_by(name='analyst').first()
    # print(job1.skills)


if __name__ == '__main__':
    create_db()
