import json
import os

temp_dir = os.getcwd()
update_courses_dir = os.path.join(temp_dir, 'courses_jsons', '28.03.2020')


def is_profession_skills_course(description, title_profession):
    """

    :param description: str
    :param title_profession: str
    :return: if description teach a skill from skill set of profession - True and name_skills_list,
     else - False and None
    """
    if title_profession == "2":
        return True, ['skill_name1', 'skill_name2']


def create_courses_json_for_profession(title_profession):
    dict_courses_for_profession = {}
    i = 0

    # from dir courses_jsons//28.03.2020 extract all courses
    for file in os.listdir(update_courses_dir):
        print("file--------------------------------------------", file)
        with open(os.path.join(update_courses_dir, file), 'r', encoding='utf-8') as json_file:
            page_courses_json = json.load(json_file)

            # get description from all courses
            for course_title in page_courses_json.keys():
                print('number of course', i + 1)
                print(course_title)
                print()
                i += 1
                if i == 100:
                    checker_break = 1
                    break
                try:
                    is_profession_skills_course_checker, skill_names_lst = is_profession_skills_course(page_courses_json[course_title]
                                                                                        ["short_description"], title_profession)
                # for udemy_result.json - does not have description
                except KeyError:
                    is_profession_skills_course_checker, skill_names_lst = is_profession_skills_course(
                        course_title, title_profession)

                # check if courses teach skills of title_profession in short_description
                if not is_profession_skills_course_checker:
                    is_profession_skills_course_checker, skill_names_lst = is_profession_skills_course(
                        page_courses_json[course_title]
                        ["long_description"], title_profession)

                    # check if courses teach skills of title_profession in long_description if not in short_description
                    if not is_profession_skills_course_checker:
                        continue

                for skill_from_course in skill_names_lst:
                    courses_skill_dict = dict_courses_for_profession.get(skill_from_course, {})
                    courses_skill_dict[course_title] = page_courses_json[course_title]
                    dict_courses_for_profession[skill_from_course] = courses_skill_dict

                # save dict_courses_for_profession
                with open(os.path.join(temp_dir, 'user_data', title_profession + '.json'), 'w', encoding='utf-8') as\
                        user_profession_courses:
                    json.dump(dict_courses_for_profession, user_profession_courses, indent=4, ensure_ascii=False)

        if checker_break == 1:
            break


if __name__ == '__main__':
    create_courses_json_for_profession("2")
