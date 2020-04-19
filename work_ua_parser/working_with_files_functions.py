import json
import os
from pathlib import Path


def save_json_name_profession(n_save_page, json_page_professions, name_profession_json_save):
    mycwd = os.getcwd()
    os.chdir("..")
    vacancy_pages_path = os.path.join(os.getcwd(), 'vacancy_work_ua_jsons')

    temp_directory = Path(os.path.join(os.getcwd(), 'vacancy_work_ua_jsons'))
    print('temp_directory', temp_directory)
    temp_directory.mkdir(exist_ok=True)
    profession_directory = Path(os.path.join(os.getcwd(), 'vacancy_work_ua_jsons',
                                             name_profession_json_save + '_work_ua_jsons'))
    profession_directory.mkdir(exist_ok=True)
    print('profession_directory', profession_directory)
    os.chdir(mycwd)

    with open(os.path.join(profession_directory,
                           name_profession_json_save + '_work_ua_vacancy_page{}.json'.format(str(n_save_page))),
              "w", encoding="utf-8") as f:
        json.dump(json_page_professions, f, indent=4, ensure_ascii=True)
