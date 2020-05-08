import copy
import json
import os
import re
import sqlite3

from sea_db.db_functions import get_parts, transform_data_from_table_in_json
from flack_app.application import Course, Profession, Skill, db

temp_dir = os.getcwd()
update_courses_dir = os.path.join(temp_dir, 'courses_jsons', 'courses_for_IT_professions')


def sort_courses_by_num_students(dict_courses_for_job):
    for skill in dict_courses_for_job.keys():
        start_lst_courses_positions = []
        lst_courses_before_sort = []
        for position_course, course in enumerate(dict_courses_for_job[skill]):
            if "number_of_students" in course.keys():
                if course["number_of_students"] != "" \
                        and ',' in course["number_of_students"]:
                    print('position', position_course)
                    str_number = course["number_of_students"].split()[0]
                    int_num = ''.join(str_number.split(','))
                    int_num = int(int_num)
                    start_lst_courses_positions.append(int_num)
                    lst_courses_before_sort.append(course)

        sorted_courses_lst = []
        sorted_positions_lst_courses = copy.deepcopy(start_lst_courses_positions)
        # print('start_lst_courses_positions', start_lst_courses_positions)
        sorted_positions_lst_courses.sort(reverse=True)
        # print('sorted_positions_lst_courses', sorted_positions_lst_courses)
        # print('sorted_positions_lst_courses', len(sorted_positions_lst_courses))
        # print('dict_courses_for_job[skill]', len(dict_courses_for_job[skill]))
        for num_students in range(len(sorted_positions_lst_courses)):
            position_to_sort_courses_in_skill = start_lst_courses_positions.index(sorted_positions_lst_courses[num_students])
            sorted_courses_lst.append(lst_courses_before_sort[position_to_sort_courses_in_skill])

        dict_courses_for_job[skill] = sorted_courses_lst

    return dict_courses_for_job


def is_profession_skills_course(description, title_profession):
    """

    :param description: str
    :param title_profession: str
    :return: if description teach a skill from skill set of profession - True and name_skills_list,
     else - False and None
    """
    global filtered_skills_for_professions
    skill_lst = []

    for skill in filtered_skills_for_professions[title_profession]:
        if len(skill.split()) > 1:
            flag_similar = 0
            for word in str(description).strip().split():
                if word.lower() in [item.lower() for item in skill.split()]:
                    flag_similar += 1

                if flag_similar > 1:
                    skill_lst.append(skill)
                    break

        else:
            for word in str(description).strip().split():
                if skill.lower() == word.lower():
                    skill_lst.append(skill)
                    break

    if skill_lst:
        return True, skill_lst

    return False, None


def create_courses_json_for_profession(title_profession):
    i = 0
    courses = Course.query.all()

    profession = Profession.query.filter_by(name=title_profession).first()
    for course in courses:
        print()
        print('number of course', course.id)
        # print('course --', course)
        # i += 1
        # if course.id == 50:
        #     checker_break = 1
        #     break

        # clean long_description from html tags
        try:
            if course.long_description.strip()[0] == "<":
                letter_near_end_tag = re.findall(r'.>[A-Z]{1}.',
                                                 course.long_description)
                index_end_tag = course.long_description.find(letter_near_end_tag[0])
                index_end_string = course.long_description.find('</p>')
                course.long_description = \
                    course.long_description[index_end_tag + 2: index_end_string]

        except IndexError:
            pass
        except KeyError:
            pass

        # clean short_description from html tags
        try:
            if course.short_description.strip()[0] == "<":
                letter_near_end_tag = re.findall(r'.>[A-Z]{1}.',
                                                 course.short_description)
                index_end_tag = course.short_description.find(
                    letter_near_end_tag[0])
                index_end_string = course.short_description.find('</p>')
                course.short_description = \
                    course.short_description[index_end_tag + 2: index_end_string]

        except IndexError:
            pass
        except KeyError:
            pass

        is_profession_skills_course_checker, skill_names_lst = is_profession_skills_course(
            course, title_profession)

        try:
            is_profession_skills_course_checker,\
            skill_names_lst = is_profession_skills_course(course.short_description, title_profession)

        # for udemy_result.json, which courses descriptions we do not have
        except KeyError:
            try:
                # check if courses teach skills of title_profession in short_description
                if not is_profession_skills_course_checker:
                    is_profession_skills_course_checker, skill_names_lst = is_profession_skills_course(
                        course.long_description, title_profession)
            except KeyError:
                pass
        else:
            pass
        # check if courses teach skills of title_profession in long_description if not check in short_description
        if not is_profession_skills_course_checker:
            continue

        for skill_from_course in skill_names_lst:
            checker_not_english_course = 0
            for word in course.course_title.split():
                for character in word:
                    if re.match(r'[^ A-z]', character) and re.match(r'[^ \d]', character) and re.match(
                            r'[^ \s]', character) and character not in '(I)&-:!.,?;_/™|+–\'“”#':
                        checker_not_english_course = 1
                        print(character)
                        print('course', course)
                        break

                if checker_not_english_course == 1:
                    break

            if checker_not_english_course == 1:
                continue

            # add relationship between course-profession-skill
            skill = Skill.query.filter_by(name=skill_from_course).first()
            profession.skills.append(skill)
            skill.courses.append(course)
            db.create_all()
            try:
                db.session.commit()
            except sqlite3.IntegrityError:
                continue

        # if checker_break == 1:
        #     break


if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'flack_app', 'user_data', 'skills_for_professions',
                           "filtered_skills_for_IT_professions.json"),
              'r', encoding="utf-8") as skills_for_profession:
        filtered_skills_for_professions = json.load(skills_for_profession)

    for profession in filtered_skills_for_professions.keys():
        # if profession[-1] == "2":
        #     profession2 = profession[:-1]
        #     profession2 = ' '.join(profession2.split("+"))
        # else:
        #     profession2 = ' '.join(profession.split("+"))

        create_courses_json_for_profession(profession)
        print(profession, "-" * 20)
        # break
        # i += 1
        # if i == 4:
        #     break
