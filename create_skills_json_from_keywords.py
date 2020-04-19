import json
import os
import re

if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'static', 'skills.json'), 'r',
              encoding='utf-8') as json_file:
        filtered_skills_for_professions = json.load(json_file)

    # lst_professions = ['аналитик', "smm-менеджер", 'специалист+технической+поддержки', 'интернет-маркетолог',
    #                    'администратор', 'системный+администратор']

    dict_profession_skills = dict()

    # for profession in lst_professions:
    #     create_courses_json_for_profession(profession)
    #     print(profession)

    # to write skills which starts with big letter
    key_skill_words = ["володіння", "знання", "вміння", "робота з", "навичк", "здатність", "працюват",
                       "досвід",
                       "владение", "знание", "умение", "работа с", "навык", "способность", "работать",
                       "опыт", "работать в",
                       "possession", "knowledge", "ability", "work with", "skill"]

    for profession in filtered_skills_for_professions.keys():
        dict_profession_skills[profession] = []
        for skill in filtered_skills_for_professions[profession][:200]:
            # if re.match(r"[A-z]", skill[0]):
            #     dict_profession_skills[profession].append(skill)
            if re.match(r"[A-z]", skill) and skill.lower() not in dict_profession_skills[profession]:
                dict_profession_skills[profession].append(skill)

            elif skill.lower() not in dict_profession_skills[profession]:
                for keyword in key_skill_words:
                    if keyword in skill.lower():
                        dict_profession_skills[profession].append(skill)
                        break

    with open(os.path.join(os.getcwd(), 'static', 'filtered_skills_for_all_professions.json'), 'w',
              encoding='utf-8') as json_file:
        json.dump(dict_profession_skills, json_file, ensure_ascii=False, indent=4)
