import copy
import json
import os
import re

from sea_db.db_functions import get_parts, transform_data_from_table_in_json

temp_dir = os.getcwd()
update_courses_dir = os.path.join(temp_dir, 'courses_jsons', '28.03.2020')


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
            for word in description.strip().split():
                if word.lower() in [item.lower() for item in skill.split()]:
                    flag_similar += 1

                if flag_similar > 1:
                    skill_lst.append(skill)
                    break

        else:
            for word in description.strip().split():
                if skill.lower() == word.lower():
                    skill_lst.append(skill)
                    break

    if skill_lst:
        return True, skill_lst

    return False, None


def create_courses_json_for_profession(title_profession):
    dict_courses_for_profession = {}
    i = 0
    checker_break = 0
    table_names = ['Coursera']

    filename = os.path.join(os.getcwd(), 'sea_db', 'courses_and_skills_db.ini')

    page_courses_json = {}

    # from dir courses_jsons//28.03.2020 extract all courses
    for table_name in table_names:
        page_courses_json = transform_data_from_table_in_json(table_name, filename)
        # print("file--------------------------------------------", file)
        # with open(os.path.join(update_courses_dir, file), 'r', encoding='utf-8') as json_file:
        #     page_courses_json = json.load(json_file)
        # get description from all courses
        for course_title in page_courses_json.keys():
            print()
            print('number of course', i + 1)
            # print('course_title --', course_title)
            i += 1
            # if i == 500:
            #     checker_break = 1
            #     break

            # clean long_description from html tags
            try:
                if page_courses_json[course_title]["long_description"].strip()[0] == "<":
                    letter_near_end_tag = re.findall(r'.>[A-Z]{1}.',
                                                     page_courses_json[course_title]["long_description"])
                    index_end_tag = page_courses_json[course_title]["long_description"].find(letter_near_end_tag[0])
                    index_end_string = page_courses_json[course_title]["long_description"].find('</p>')
                    page_courses_json[course_title]["long_description"] = \
                        page_courses_json[course_title]["long_description"][index_end_tag + 2: index_end_string]

            except IndexError:
                pass
            except KeyError:
                pass

            # clean short_description from html tags
            try:
                if page_courses_json[course_title]["short_description"].strip()[0] == "<":
                    letter_near_end_tag = re.findall(r'.>[A-Z]{1}.',
                                                     page_courses_json[course_title]["short_description"])
                    index_end_tag = page_courses_json[course_title]["short_description"].find(
                        letter_near_end_tag[0])
                    index_end_string = page_courses_json[course_title]["short_description"].find('</p>')
                    page_courses_json[course_title]["short_description"] = \
                        page_courses_json[course_title]["short_description"][index_end_tag + 2: index_end_string]

            except IndexError:
                pass
            except KeyError:
                pass

            is_profession_skills_course_checker, skill_names_lst = is_profession_skills_course(
                course_title, title_profession)

            try:
                is_profession_skills_course_checker, skill_names_lst = is_profession_skills_course(page_courses_json[course_title]
                                                                                    ["short_description"], title_profession)
            # for udemy_result.json, which courses descriptions we do not have
            except KeyError:
                try:
                    # check if courses teach skills of title_profession in short_description
                    if not is_profession_skills_course_checker:
                        is_profession_skills_course_checker, skill_names_lst = is_profession_skills_course(
                            page_courses_json[course_title]["long_description"], title_profession)
                except KeyError:
                    pass
            else:
                pass
            #
            #     # check if courses teach skills of title_profession in long_description if not in short_description
            if not is_profession_skills_course_checker:
                continue

            # print(skill_names_lst)
            for skill_from_course in skill_names_lst:
                courses_skill_dict = dict_courses_for_profession.get(skill_from_course, [])
                page_courses_json2 = copy.deepcopy(page_courses_json)
                page_courses_json2[course_title]['course_title'] = course_title
                checker_not_english_course = 0
                for word in course_title.split():
                    for character in word:
                        if re.match(r'[^ A-z]', character) and re.match(r'[^ \d]', character) and re.match(
                                r'[^ \s]', character) and character not in '(I)&-:!.,?;_/™|+–\'“”#':
                            checker_not_english_course = 1
                            print(character)
                            print('course_title', course_title)
                            break

                    if checker_not_english_course == 1:
                        break

                if checker_not_english_course == 1:
                    continue

                courses_skill_dict.append(page_courses_json2[course_title])
                dict_courses_for_profession[skill_from_course] = courses_skill_dict

            if checker_break == 1:
                break

    dict_courses_for_profession = sort_courses_by_num_students(dict_courses_for_profession)
    print('here')
    copy_dict_courses_for_profession = copy.deepcopy(dict_courses_for_profession)
    for skill in copy_dict_courses_for_profession.keys():
        if not dict_courses_for_profession[skill]:
            dict_courses_for_profession.pop(skill)

    # save dict_courses_for_profession
    with open(os.path.join(temp_dir, 'user_data', title_profession + '2.json'), 'w', encoding='utf-8') as \
            user_profession_courses:
        json.dump(dict_courses_for_profession, user_profession_courses, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'static', 'filtered_skills_for_all_professions.json'), 'r',
              encoding='utf-8') as json_file:
        filtered_skills_for_professions = json.load(json_file)

    # i = 0
    for profession in filtered_skills_for_professions.keys():
        create_courses_json_for_profession(profession)
        print(profession)
        break
        # i += 1
        # if i == 4:
        #     break

    # to write skills which starts with big letter

    #     dict_profession_skills[profession] = []
    #     for skill in filtered_skills_for_professions[profession]:
    #         if re.match(r"[A-z]", skill[0]):
    #             dict_profession_skills[profession].append(skill)
    #
    # with open(os.path.join(os.getcwd(), 'static', 'filtered_skills_for_professions2.json'), 'w',
    #           encoding='utf-8') as json_file:
    #     json.dump(dict_profession_skills, json_file, ensure_ascii=False, indent=4)
