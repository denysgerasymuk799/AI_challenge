import json
import os
import re

temp_dir = os.getcwd()
update_courses_dir = os.path.join(temp_dir, 'courses_jsons', '28.03.2020')


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
        if re.match(r"[A-z]", skill[0]):
            # for word_in_skill in skill.split():
            if len(skill.split()) > 1:
                flag_similar = 0
                for word in description.strip().split():
                    if word.lower() in [item.lower() for item in skill.split()]:
                        flag_similar += 1

                    if flag_similar > 2:
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

    # from dir courses_jsons//28.03.2020 extract all courses
    for file in os.listdir(update_courses_dir):
        print("file--------------------------------------------", file)
        with open(os.path.join(update_courses_dir, file), 'r', encoding='utf-8') as json_file:
            page_courses_json = json.load(json_file)

            # get description from all courses
            for course_title in page_courses_json.keys():
                # print()
                # print('number of course', i + 1)
                # print('course_title --', course_title)
                # i += 1
                # if i == 100:
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
                # for udemy_result.json - does not have description
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
                    courses_skill_dict = dict_courses_for_profession.get(skill_from_course, {})
                    courses_skill_dict[course_title] = page_courses_json[course_title]
                    dict_courses_for_profession[skill_from_course] = courses_skill_dict

                # save dict_courses_for_profession
                with open(os.path.join(temp_dir, 'user_data', title_profession + '.json'), 'w', encoding='utf-8') as \
                        user_profession_courses:
                    json.dump(dict_courses_for_profession, user_profession_courses, indent=4, ensure_ascii=False)

        # if checker_break == 1:
        #     break


if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'static', 'filtered_skills_for_professions2.json'), 'r',
              encoding='utf-8') as json_file:
        filtered_skills_for_professions = json.load(json_file)

    lst_professions = ['аналитик', "smm-менеджер", 'специалист+технической+поддержки', 'интернет-маркетолог',
                       'администратор', 'системный+администратор']

    dict_profession_skills = dict()

    for profession in lst_professions:
        create_courses_json_for_profession(profession)
        print(profession)

    # to write skills which starts with big letter

    #     dict_profession_skills[profession] = []
    #     for skill in filtered_skills_for_professions[profession]:
    #         if re.match(r"[A-z]", skill[0]):
    #             dict_profession_skills[profession].append(skill)
    #
    # with open(os.path.join(os.getcwd(), 'static', 'filtered_skills_for_professions2.json'), 'w',
    #           encoding='utf-8') as json_file:
    #     json.dump(dict_profession_skills, json_file, ensure_ascii=False, indent=4)
