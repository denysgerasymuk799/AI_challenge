import json
import os
import sqlite3

import sqlalchemy

from flask_app import db, Profession, Skill, Course


def create_db():
    # write in db
    with open(os.path.join(os.getcwd(), 'user_data', 'skills_for_professions',
                           "filtered_skills_for_IT_professions.json"),
              'r', encoding="utf-8") as skills_for_profession:
        json_skills_for_profession = json.load(skills_for_profession)
        for profession_name in json_skills_for_profession.keys():
            if profession_name[-1] == "2":
                profession_name2 = profession_name[:-1]
                profession_name2 = ' '.join(profession_name2.split("+"))
            else:
                profession_name2 = ' '.join(profession_name.split("+"))

            # if db.session.query(Profession.id).filter_by(name=profession_name2).scalar() is not None:
            #     print("Found in db")
            #     continue

            try:
                p = Profession(name=profession_name2)
                db.session.add(p)
                db.session.commit()

            except sqlite3.IntegrityError:
                pass
            except sqlalchemy.exc.IntegrityError:
                pass
            except Exception:
                continue

            print('profession_name', profession_name2)
            # write skills for the special profession in db
            for skill_name in json_skills_for_profession[profession_name]:
                s = Skill(name=skill_name)
                try:
                    if db.session.query(Skill.id).filter_by(name=skill_name).scalar() is not None:
                        print("Found in db")
                        continue
                    db.session.add(s)
                    db.session.commit()
                except sqlite3.IntegrityError:
                    continue
                except sqlalchemy.exc.IntegrityError:
                    continue
                except sqlalchemy.exc.InvalidRequestError:
                    continue
                except Exception:
                    continue

            try:
                db.session.rollback()
                db.session.commit()
                db.create_all()
            except sqlite3.IntegrityError:
                continue
            except sqlalchemy.exc.IntegrityError:
                continue
            except Exception:
                continue

    num_course = 0
    # for num_file, filename in enumerate(os.listdir(os.path.join('user_data', "courses_for_all_professions",
    #                                                             "IT_courses"))):
    # print(filename, "-" * 20)
    with open(os.path.join(os.getcwd(), 'user_data', "courses_for_all_professions",
                           "IT_courses", "edx_results.json"),
              'r', encoding="utf-8") as courses_for_profession:
        json_courses_for_profession = json.load(courses_for_profession)
        for course_title in json_courses_for_profession.keys():
            # write courses for the special profession in db
            course_data = json_courses_for_profession[course_title]
            try:
                if db.session.query(Course.id).filter_by(course_title=course_title).scalar() is not None:
                    print("Found in db")
                    continue
            except sqlite3.IntegrityError:
                continue
            except sqlalchemy.exc.IntegrityError:
                continue
            except sqlalchemy.exc.InvalidRequestError:
                continue
            except Exception:
                continue

            if isinstance(course_data["image"], dict):
                if "small" in course_data["image"].keys():
                    course_data["image"] = course_data["image"]["small"]
                else:
                    course_data["image"] = course_data["image"]["image_480x270"]
            try:
                course = Course(course_title=course_title,
                                price=course_data["price"],
                                image=course_data["image"],
                                number_of_students=course_data["number_of_students"],
                                course_duration=course_data["course_duration"],
                                short_description=course_data["short_description"],
                                long_description=course_data["long_description"],
                                url=course_data["url"])
                db.session.add(course)
                db.session.commit()

            # for udemy json which does not have image
            except KeyError:
                course = Course(course_title=course_title,
                                price=course_data["price"],
                                image=course_data["image"],
                                number_of_students="",
                                course_duration="",
                                short_description="",
                                long_description="",
                                url=course_data["url"])
                db.session.add(course)
                db.session.commit()

            except sqlite3.IntegrityError:
                continue
            except sqlalchemy.exc.IntegrityError:
                pass
            except (sqlalchemy.exc.InvalidRequestError and sqlalchemy.exc.DataError):
                continue
            except Exception:
                continue

            # db.create_all()
            num_course += 1
            print("num_course", num_course)
            print(course_title)
            try:
                db.session.rollback()
                db.session.commit()
                db.create_all()

            except sqlite3.IntegrityError:
                continue
            except sqlalchemy.exc.IntegrityError:
                continue
            except sqlalchemy.exc.InvalidRequestError:
                continue
            except Exception:
                continue

    # job1 = Profession.query.filter_by(name='analyst').first()
    # print(job1.skills)


if __name__ == '__main__':
    create_db()
