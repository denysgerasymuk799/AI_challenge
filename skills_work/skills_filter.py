import json
import os
import re

from googletrans import Translator

translator = Translator()


def find_key_words():
    dict_skills_for_professions = {}
    mycwd = os.getcwd()
    os.chdir("..")
    with open(os.path.join(os.getcwd(), 'static', 'skills.json'), 'r', encoding='utf-8') as json_file:
        skills_for_professions_file = json.load(json_file)

        key_words = ['умение', 'умения', 'навыки', 'вміння', 'требования',
                     'рівень', 'уровень',
                     'работать', 'работа',
                     'знания', 'знання',
                     'опыт', 'досвід', 'працювати', 'специалист', 'спеціаліст', 'обязанности', 'обов\'язки']

        for name_profession in skills_for_professions_file.keys():
            dict_skills_for_professions[name_profession] = []
            for skill in skills_for_professions_file[name_profession]:
                for word in skill.split():
                    if re.search(r'.[a-z].', word.lower()):
                        print(skill)
                        # try:
                        #     skill = translator.translate(skill, dest='en')
                        # except:
                        #     pass
                        dict_skills_for_professions[name_profession].append(word)
                        break

    # save dict_courses_for_profession
    with open(os.path.join(os.getcwd(), 'static', 'filtered_skills_for_professions.json'), 'w', encoding='utf-8') as \
            filtered_skills_for_professions:
        json.dump(dict_skills_for_professions, filtered_skills_for_professions, indent=4, ensure_ascii=False)

    os.chdir(mycwd)


if __name__ == '__main__':
    find_key_words()
