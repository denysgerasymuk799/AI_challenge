import json
import os

from googletrans import Translator


translator = Translator()


def translate_on_en():
    mycwd = os.getcwd()
    os.chdir("..")
    with open(os.path.join(os.getcwd(), 'static', 'filtered_skills_for_professions.json'), 'r', encoding='utf-8') as json_file:
        filtered_skills_for_professions = json.load(json_file)

    translator.translate(text, dest='en')
    with open(os.path.join(os.getcwd(), 'static', 'filtered_skills_for_professions.json'), 'w', encoding='utf-8') as \
            filtered_skills_for_professions:
        json.dump(dict_skills_for_professions, filtered_skills_for_professions, indent=4, ensure_ascii=False)